from flask import Flask, render_template, request, jsonify, session, redirect, url_for, abort
import xml.etree.ElementTree as ET

# =============== XML indentation helper ===================
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
app = Flask(__name__)
app.secret_key = "super_secret_key_123"


# ===========================================================
# USERS
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


def get_client(username, password):
    tree = ET.parse("data/clients.xml")
    root = tree.getroot()

    for c in root.findall("client"):
        if c.find("username").text == username and c.find("password").text == password:
            return {
                "username": username,
                "role": "client"
            }
    return None


def ajouter_client(username, email, password, lieu, postal, cin):
    tree = ET.parse("data/clients.xml")
    root = tree.getroot()

    # check duplicate
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
# ROUTES LOGIN / REGISTER
# ===========================================================
@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    user_info = get_user(username, password)

    if not user_info:
        user_info = get_client(username, password)

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

    if ajouter_client(data["username"], data["email"], data["password"],
                      data["lieu"], data["postal"], data["cin"]):
        return jsonify({"status": "ok"})
    else:
        return jsonify({"status": "exists"})


# ===========================================================
# ROLE PROTECTION
# ===========================================================
def role_required(role):
    if "role" not in session or session["role"] != role:
        abort(403)


# ===========================================================
# DASHBOARD ROUTES
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
# POINTS MAP (Leaflet)
# ===========================================================
@app.route("/points")
def points_page():
    role_required("admin")
    return render_template("points.html")


@app.route("/api/points")
def api_points():
    tree = ET.parse("data/Points.xml")
    root = tree.getroot()

    arr = []
    for p in root.findall("point"):
        arr.append({
            "lat": float(p.find("lat").text),
            "lng": float(p.find("lng").text),
            "type": p.find("type").text,
            "capacite": p.find("capacite").text,
            "niveau": p.find("niveau").text
        })

    return jsonify({"points": arr})



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
    ET.SubElement(new, "niveau").text = "0"   # <-- AUTOMATIQUE

    root.append(new)
    indent(root)

    tree.write("data/Points.xml", encoding="UTF-8", xml_declaration=True)
    return jsonify({"status": "ok"})



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


# ===========================================================
# LOGOUT
# ===========================================================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


# ===========================================================
# START SERVER
# ===========================================================
if __name__ == "__main__":
    app.run(debug=True)
