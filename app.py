from flask import Flask, render_template, request, jsonify, session, redirect, url_for, abort
import xml.etree.ElementTree as ET

# ===========================================================
# 🔧 Beautifier XML (indentation propre)
# ===========================================================
def indent(elem, level=0):
    i = "\n" + level * "    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        for child in elem:
            indent(child, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


# ===========================================================
# 🛠️ CONFIG FLASK
# ===========================================================
app = Flask(__name__)
app.secret_key = "super_secret_key_123"


# ===========================================================
# 📌 CHARGER UTILISATEURS (admin/employé/chauffeur)
# ===========================================================
def get_user(username, password):
    tree = ET.parse("data/users.xml")
    root = tree.getroot()

    for user in root.findall("user"):
        if user.find("username").text == username and user.find("password").text == password:
            return {
                "username": username,
                "role": user.find("role").text
            }
    return None


# ===========================================================
# 📌 CHARGER CLIENTS
# ===========================================================
def get_client(username, password):
    tree = ET.parse("data/clients.xml")
    root = tree.getroot()

    for c in root.findall("client"):
        if c.find("username").text == username and c.find("password").text == password:
            return {"username": username, "role": "client"}

    return None


def ajouter_client(username, email, password, lieu, postal, cin):
    tree = ET.parse("data/clients.xml")
    root = tree.getroot()

    # Check duplicate
    for c in root.findall("client"):
        if c.find("username").text == username:
            return False

    new = ET.Element("client")
    ET.SubElement(new, "username").text = username
    ET.SubElement(new, "email").text = email
    ET.SubElement(new, "password").text = password
    ET.SubElement(new, "lieu").text = lieu
    ET.SubElement(new, "postal").text = postal
    ET.SubElement(new, "cin").text = cin

    root.append(new)
    indent(root)

    tree.write("data/clients.xml", encoding="UTF-8", xml_declaration=True)
    return True


# ===========================================================
# 🔐 AUTHENTIFICATION
# ===========================================================
@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    # Chercher dans users.xml puis clients.xml
    user_info = (
    get_user(username, password) or
    get_client(username, password) or
    get_employe(username, password) or
    get_chauffeur(username, password)
)



    if not user_info:
        return jsonify({"status": "error"})

    session["username"] = user_info["username"]
    session["role"] = user_info["role"]

    return jsonify({"status": "ok", "role": user_info["role"]})


@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register_client_route():
    data = request.json

    ok = ajouter_client(
        data["username"], data["email"], data["password"],
        data["lieu"], data["postal"], data["cin"]
    )

    return jsonify({"status": "ok" if ok else "exists"})


# ===========================================================
# 🔐 VERIFICATION DES ROLES
# ===========================================================
def role_required(role):
    if "role" not in session or session["role"] != role:
        abort(403)


# ===========================================================
# 🖥️ DASHBOARD SELON ROLE
# ===========================================================
@app.route("/admin")
def admin_dashboard():
    role_required("admin")
    return render_template("admin.html")


@app.route("/employe")
def employe_dashboard():
    role_required("employe")
    return render_template("employe.html")


@app.route("/chauffeur")
def chauffeur_dashboard():
    role_required("chauffeur")
    return render_template("chauffeur.html")


@app.route("/client")
def client_dashboard():
    role_required("client")
    return render_template("client.html")


# ===========================================================
# 🗺️ MAP DES POINTS DE COLLECTE (ADMIN / EMPLOYÉ)
# ===========================================================
@app.route("/points")
def points_page():
    role_required("admin")
    return render_template("points.html", role=session["role"])


@app.route("/points/table")
def points_table():
    role_required("admin")
    return render_template("points_table.html")


# -------- API : Lister les points --------
@app.route("/api/points")
def api_points():
    tree = ET.parse("data/Points.xml")
    root = tree.getroot()

    result = []
    for p in root.findall("point"):
        result.append({
            "lat": float(p.find("lat").text),
            "lng": float(p.find("lng").text),
            "type": p.find("type").text,
            "capacite": p.find("capacite").text,
            "niveau": p.find("niveau").text
        })

    return jsonify({"points": result})


# -------- API : Ajouter un point --------
@app.route("/api/add_point", methods=["POST"])
def api_add_point():
    data = request.json

    tree = ET.parse("data/Points.xml")
    root = tree.getroot()

    new = ET.Element("point")
    ET.SubElement(new, "lat").text = str(data["lat"])
    ET.SubElement(new, "lng").text = str(data["lng"])
    ET.SubElement(new, "type").text = data["type"]
    ET.SubElement(new, "capacite").text = str(data["capacite"])
    ET.SubElement(new, "niveau").text = "0"  # automatique

    root.append(new)
    indent(root)

    tree.write("data/Points.xml", encoding="UTF-8", xml_declaration=True)
    return jsonify({"status": "ok"})


# -------- API : Supprimer un point --------
@app.route("/api/delete_point", methods=["POST"])
def api_delete_point():
    data = request.json
    lat = str(data["lat"])
    lng = str(data["lng"])

    tree = ET.parse("data/Points.xml")
    root = tree.getroot()

    for p in root.findall("point"):
        if p.find("lat").text == lat and p.find("lng").text == lng:
            root.remove(p)
            indent(root)
            tree.write("data/Points.xml", encoding="UTF-8", xml_declaration=True)
            return jsonify({"status": "ok"})

    return jsonify({"status": "not_found"})
#----------------employe,admin-----------------------
@app.route("/employes")
def employes_dashboard():
    role_required("admin")
    return render_template("gestion_employes.html")
@app.route("/employes/liste")
def liste_employes_page():
    role_required("admin")
    return render_template("liste_employes.html")
@app.route("/api/employes")
def api_employes():
    tree = ET.parse("data/employes.xml")
    root = tree.getroot()

    arr = []
    for emp in root.findall("employe"):
        arr.append({
            "cin": emp.find("cin").text,
            "nom": emp.find("nom").text,
            "prenom": emp.find("prenom").text,
            "email": emp.find("email").text,
            "adresse": emp.find("adresse").text,
            "telephone": emp.find("telephone").text,
            "poste": emp.find("poste").text,
            "salaire": emp.find("salaire").text

        })

    return jsonify({"employes": arr})



@app.route("/employes/add")
def employes_add_page():
    role_required("admin")  # admin seulement
    return render_template("ajouter_employe.html")
@app.route("/api/add_employe", methods=["POST"])
def api_add_employe():
    data = request.json

    tree = ET.parse("data/employes.xml")
    root = tree.getroot()

    emp = ET.Element("employe")
    ET.SubElement(emp, "cin").text = data["cin"]
    ET.SubElement(emp, "nom").text = data["nom"]
    ET.SubElement(emp, "prenom").text = data["prenom"]
    ET.SubElement(emp, "email").text = data["email"]
    ET.SubElement(emp, "adresse").text = data["adresse"]
    ET.SubElement(emp, "telephone").text = data["telephone"]
    ET.SubElement(emp, "poste").text = data["poste"]
    ET.SubElement(emp, "salaire").text = data["salaire"]

    root.append(emp)
    indent(root)
    tree.write("data/employes.xml", encoding="UTF-8", xml_declaration=True)

    return jsonify({"status": "ok"})




@app.route("/employes/delete")
def employes_delete_page():
    role_required("admin")
    return render_template("delete_employe.html")

@app.route("/api/delete_employe", methods=["POST"])
def api_delete_employe():
    data = request.json
    cin = data["cin"]

    tree = ET.parse("data/employes.xml")
    root = tree.getroot()

    for emp in root.findall("employe"):
        if emp.find("cin").text == cin:
            root.remove(emp)
            indent(root)
            tree.write("data/employes.xml", encoding="UTF-8", xml_declaration=True)
            return jsonify({"status": "ok"})

    return jsonify({"status": "not_found"})
@app.route("/api/update_employe", methods=["POST"])
def api_update_employe():
    data = request.json

    old_cin = data["old_cin"]   # ancien CIN
    new_cin = data["cin"]       # nouveau CIN

    tree = ET.parse("data/employes.xml")
    root = tree.getroot()

    for emp in root.findall("employe"):
        if emp.find("cin").text == old_cin:  # on cherche AVEC ancien CIN

            emp.find("cin").text = new_cin   # NOUVEAU CIN
            emp.find("nom").text = data["nom"]
            emp.find("prenom").text = data["prenom"]
            emp.find("email").text = data["email"]
            emp.find("adresse").text = data["adresse"]
            emp.find("telephone").text = data["telephone"]
            emp.find("poste").text = data["poste"]
            emp.find("salaire").text = data["salaire"]

            indent(root)
            tree.write("data/employes.xml", encoding="UTF-8", xml_declaration=True)

            return jsonify({"status": "ok"})

    return jsonify({"status": "not_found"})

def get_employe(username, password):
    tree = ET.parse("data/employes.xml")
    root = tree.getroot()

    for emp in root.findall("employe"):
        prenom = emp.find("prenom").text
        cin = emp.find("cin").text

        if prenom == username and cin == password:
            return {
                "username": prenom,
                "role": "employe"
            }

    return None
#-----------------chauffeur,admin------------------------
@app.route("/chauffeurs")
def chauffeurs_dashboard():
    role_required("admin")
    return render_template("gestion_chauffeurs.html")
@app.route("/api/chauffeurs")
def api_chauffeurs():
    tree = ET.parse("data/chauffeurs.xml")
    root = tree.getroot()

    arr = []
    for ch in root.findall("chauffeur"):
        arr.append({
            "cin": ch.find("cin").text,
            "nom": ch.find("nom").text,
            "prenom": ch.find("prenom").text,
            "email": ch.find("email").text,
            "adresse": ch.find("adresse").text,
            "telephone": ch.find("telephone").text,
            "poste": ch.find("poste").text,
            "salaire": ch.find("salaire").text
        })

    return jsonify({"chauffeurs": arr})
@app.route("/api/delete_chauffeur", methods=["POST"])
def api_delete_chauffeur():
    data = request.json
    cin = data["cin"]

    tree = ET.parse("data/chauffeurs.xml")
    root = tree.getroot()

    for ch in root.findall("chauffeur"):
        if ch.find("cin").text == cin:
            root.remove(ch)
            indent(root)
            tree.write("data/chauffeurs.xml", encoding="UTF-8", xml_declaration=True)
            return jsonify({"status": "ok"})

    return jsonify({"status": "not_found"})
@app.route("/api/update_chauffeur", methods=["POST"])
def api_update_chauffeur():
    data = request.json
    old = data["old_cin"]   # ancien CIN
    new = data["cin"]       # nouveau CIN

    tree = ET.parse("data/chauffeurs.xml")
    root = tree.getroot()

    for ch in root.findall("chauffeur"):
        if ch.find("cin").text == old:

            ch.find("cin").text = new
            ch.find("nom").text = data["nom"]
            ch.find("prenom").text = data["prenom"]
            ch.find("email").text = data["email"]
            ch.find("adresse").text = data["adresse"]
            ch.find("telephone").text = data["telephone"]
            ch.find("poste").text = data["poste"]
            ch.find("salaire").text = data["salaire"]

            indent(root)
            tree.write("data/chauffeurs.xml", encoding="UTF-8", xml_declaration=True)

            return jsonify({"status": "ok"})

    return jsonify({"status": "not_found"})

@app.route("/api/add_chauffeur", methods=["POST"])
def api_add_chauffeur():
    data = request.json

    tree = ET.parse("data/chauffeurs.xml")
    root = tree.getroot()

    ch = ET.Element("chauffeur")
    ET.SubElement(ch, "cin").text = data["cin"]
    ET.SubElement(ch, "nom").text = data["nom"]
    ET.SubElement(ch, "prenom").text = data["prenom"]
    ET.SubElement(ch, "email").text = data["email"]
    ET.SubElement(ch, "adresse").text = data["adresse"]
    ET.SubElement(ch, "telephone").text = data["telephone"]
    ET.SubElement(ch, "poste").text = data["poste"]
    ET.SubElement(ch, "salaire").text = data["salaire"]

    root.append(ch)
    indent(root)

    tree.write("data/chauffeurs.xml", encoding="UTF-8", xml_declaration=True)

    return jsonify({"status": "ok"})
def get_chauffeur(username, password):
    tree = ET.parse("data/chauffeurs.xml")
    root = tree.getroot()

    for ch in root.findall("chauffeur"):
        if ch.find("prenom").text == username and ch.find("cin").text == password:
            return {"username": username, "role": "chauffeur"}

    return None
#------------vehicules,admin-------------------
@app.route("/vehicules")
def vehicules_dashboard():
    role_required("admin")
    return render_template("gestion_vehicules.html")


@app.route("/api/vehicules")
def api_vehicules():
    tree = ET.parse("data/vehicules.xml")
    root = tree.getroot()

    arr = []
    for v in root.findall("vehicule"):
        arr.append({
            "matricule": v.find("matricule").text,
            "marque": v.find("marque").text,
            "capacite": v.find("capacite").text,
            "prix": v.find("prix").text,
            "age": v.find("age").text
        })

    return jsonify({"vehicules": arr})


@app.route("/api/add_vehicule", methods=["POST"])
def api_add_vehicule():
    data = request.json

    tree = ET.parse("data/vehicules.xml")
    root = tree.getroot()

    new = ET.Element("vehicule")
    ET.SubElement(new, "matricule").text = data["matricule"]
    ET.SubElement(new, "marque").text = data["marque"]
    ET.SubElement(new, "capacite").text = data["capacite"]
    ET.SubElement(new, "prix").text = data["prix"]
    ET.SubElement(new, "age").text = data["age"]

    root.append(new)
    indent(root)
    tree.write("data/vehicules.xml", encoding="UTF-8", xml_declaration=True)

    return jsonify({"status": "ok"})


@app.route("/api/delete_vehicule", methods=["POST"])
def api_delete_vehicule():
    data = request.json
    matricule = data["matricule"]

    tree = ET.parse("data/vehicules.xml")
    root = tree.getroot()

    for v in root.findall("vehicule"):
        if v.find("matricule").text == matricule:
            root.remove(v)
            indent(root)
            tree.write("data/vehicules.xml", encoding="UTF-8", xml_declaration=True)
            return jsonify({"status": "ok"})

    return jsonify({"status": "not_found"})


@app.route("/api/update_vehicule", methods=["POST"])
def api_update_vehicule():
    data = request.json
    old = data["matricule"]          # ancienne matricule
    new = data["new_matricule"]      # nouvelle matricule

    tree = ET.parse("data/vehicules.xml")
    root = tree.getroot()

    for v in root.findall("vehicule"):
        if v.find("matricule").text == old:

            v.find("matricule").text = new
            v.find("marque").text = data["marque"]
            v.find("capacite").text = data["capacite"]
            v.find("prix").text = data["prix"]
            v.find("age").text = data["age"]

            indent(root)
            tree.write("data/vehicules.xml", encoding="UTF-8", xml_declaration=True)
            return jsonify({"status": "ok"})

    return jsonify({"status": "not_found"})





# ===========================================================
# 🚪 LOGOUT
# ===========================================================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


# ===========================================================
# ▶️ LANCER LE SERVEUR
# ===========================================================
if __name__ == "__main__":
    app.run(debug=True)
