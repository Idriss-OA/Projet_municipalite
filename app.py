from flask import Flask, render_template, request, jsonify, session, redirect, url_for, abort
import xml.etree.ElementTree as ET
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


app = Flask(__name__)
app.secret_key = "super_secret_key_123"


# ---------------------------------------------------------
# 🔵 1. Chargement utilisateur (depuis users.xml)
# ---------------------------------------------------------
def get_user(username, password):
    tree = ET.parse("data/users.xml")
    root = tree.getroot()

    for user in root.findall("user"):
        u = user.find("username").text
        p = user.find("password").text
        r = user.find("role").text

        if u == username and p == password:
            return {"username": u, "role": r}

    return None


# ---------------------------------------------------------
# 🔵 2. Ajouter un client dans clients.xml
# ---------------------------------------------------------
def ajouter_client(username, email, password, lieu, postal, cin):

    tree = ET.parse("data/clients.xml")
    root = tree.getroot()

    # Vérifier doublon username
    for c in root.findall("client"):
        if c.find("username").text == username:
            return False

    new_client = ET.Element("client")

    ET.SubElement(new_client, "username").text = username
    ET.SubElement(new_client, "email").text = email
    ET.SubElement(new_client, "password").text = password
    ET.SubElement(new_client, "lieu").text = lieu
    ET.SubElement(new_client, "postal").text = postal
    ET.SubElement(new_client, "cin").text = cin

    root.append(new_client)

    # 🔥 Rendre le XML joli et bien indenté
    indent(root)

    tree.write("data/clients.xml", encoding="UTF-8", xml_declaration=True)

    return True



# ---------------------------------------------------------
# 🔵 3. Page principale = login
# ---------------------------------------------------------
@app.route("/")
def home():
    return render_template("login.html")


# ---------------------------------------------------------
# 🔵 4. API Login (POST)
# ---------------------------------------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    # Vérifier dans users.xml (admin / employe / chauffeur)
    user_info = get_user(username, password)

    # Si pas trouvé → vérifier dans clients.xml
    if not user_info:
        user_info = get_client(username, password)

    # Aucun utilisateur trouvé
    if not user_info:
        return jsonify({"status": "error"})

    # Si trouvé → stocker session
    session["username"] = user_info["username"]
    session["role"] = user_info["role"]

    return jsonify({
        "status": "ok",
        "role": user_info["role"]
    })


# ---------------------------------------------------------
# 🔵 5. Page création de compte HTML
# ---------------------------------------------------------
@app.route("/register")
def register_page():
    return render_template("register.html")


# ---------------------------------------------------------
# 🔵 6. API inscription client (POST)
# ---------------------------------------------------------
@app.route("/register", methods=["POST"])
def register_client():


    data = request.json

    username = data["username"]
    email = data["email"]
    password = data["password"]
    lieu = data["lieu"]
    postal = data["postal"]
    cin = data["cin"]

    if ajouter_client(username, email, password, lieu, postal, cin):
        return jsonify({"status": "ok"})
    else:
        return jsonify({"status": "exists"})


# ---------------------------------------------------------
# 🔵 7. Bloquer accès si mauvais rôle
# ---------------------------------------------------------
def role_required(role):
    if "role" not in session or session["role"] != role:
        abort(403)


# ---------------------------------------------------------
# 🔵 8. Pages protégées selon rôle
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# 🔵 9. Déconnexion
# ---------------------------------------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

def get_client(username, password):
    tree = ET.parse("data/clients.xml")
    root = tree.getroot()

    for c in root.findall("client"):
        u = c.find("username").text
        p = c.find("password").text
        
        if u == username and p == password:
            return {
                "username": u,
                "role": "client"
            }

    return None


# ---------------------------------------------------------
# 🔵 10. Démarrer serveur Flask
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
