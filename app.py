from flask import Flask, render_template, request, jsonify, session, redirect, url_for, abort
import xml.etree.ElementTree as ET

# Services POO
from services.employe_service import EmployeService
from services.chauffeur_service import ChauffeurService
from services.vehicule_service import VehiculeService
from services.point_service import PointService

from models.employe import Employe
from models.chauffeur import Chauffeur
from models.vehicule import Vehicule
from models.point import Point

# -------------------------------------------
# CONFIG FLASK
# -------------------------------------------
app = Flask(__name__)
app.secret_key = "super_secret_key_123"


# -------------------------------------------
# MIDDLEWARE : ROLE REQUIRED
# -------------------------------------------
def role_required(role):
    if "role" not in session or session["role"] != role:
        abort(403)


# -------------------------------------------
# LOGIN / LOGOUT
# -------------------------------------------
@app.route("/")
def home():
    return render_template("login.html")


# ---------------- LOGIN --------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    # 1️⃣ admin/user (dans users.xml)
    user_info = get_user(username, password)

    # 2️⃣ client
    if not user_info:
        user_info = get_client(username, password)

    # 3️⃣ employé
    if not user_info:
        user_info = get_employe(username, password)

    # 4️⃣ chauffeur
    if not user_info:
        user_info = get_chauffeur(username, password)

    if not user_info:
        return jsonify({"status": "error"})

    session["username"] = user_info["username"]
    session["role"] = user_info["role"]

    return jsonify({"status": "ok", "role": user_info["role"]})


# ---------------- LOGOUT -------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


# ==================================================================
#  AUTH HELPERS  (lecture XML admin / clients)
# ==================================================================
def get_user(username, password):
    tree = ET.parse("data/users.xml")
    root = tree.getroot()

    for u in root.findall("user"):
        if u.find("username").text == username and u.find("password").text == password:
            return {"username": username, "role": u.find("role").text}

    return None


def get_client(username, password):
    tree = ET.parse("data/clients.xml")
    root = tree.getroot()

    for c in root.findall("client"):
        if c.find("username").text == username and c.find("password").text == password:
            return {"username": username, "role": "client"}

    return None


def get_employe(username, password):
    for emp in EmployeService.load_all():
        if emp.prenom == username and emp.cin == password:
            return {"username": username, "role": "employe"}

    return None


def get_chauffeur(username, password):
    for ch in ChauffeurService.load_all():
        if ch.prenom == username and ch.cin == password:
            return {"username": username, "role": "chauffeur"}

    return None


# ==================================================================
#  DASHBOARDS
# ==================================================================
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


# ==================================================================
#  EMPLOYES (admin only)
# ==================================================================
@app.route("/employes")
def employes_page():
    role_required("admin")
    return render_template("gestion_employes.html")


@app.route("/api/employes")
def api_employes():
    employes = EmployeService.load_all()
    return jsonify({"employes": [e.to_dict() for e in employes]})


@app.route("/api/add_employe", methods=["POST"])
def api_add_employe():
    data = request.json
    e = Employe(**data)
    EmployeService.add(e)
    return jsonify({"status": "ok"})


@app.route("/api/delete_employe", methods=["POST"])
def api_delete_employe():
    cin = request.json["cin"]
    ok = EmployeService.delete(cin)
    return jsonify({"status": "ok" if ok else "not_found"})


@app.route("/api/update_employe", methods=["POST"])
def api_update_employe():
    data = request.json
    old = data["old_cin"]
    updated = Employe(
        data["cin"],
        data["nom"],
        data["prenom"],
        data["email"],
        data["adresse"],
        data["telephone"],
        data["poste"],
        data["salaire"]
    )
    ok = EmployeService.update(old, updated)
    return jsonify({"status": "ok" if ok else "not_found"})


# ==================================================================
#  CHAUFFEURS (admin only)
# ==================================================================
@app.route("/chauffeurs")
def chauffeurs_page():
    role_required("admin")
    return render_template("gestion_chauffeurs.html")


@app.route("/api/chauffeurs")
def api_chauffeurs():
    ch = ChauffeurService.load_all()
    return jsonify({"chauffeurs": [c.to_dict() for c in ch]})


@app.route("/api/add_chauffeur", methods=["POST"])
def api_add_chauffeur():
    c = Chauffeur(**request.json)
    ChauffeurService.add(c)
    return jsonify({"status": "ok"})


@app.route("/api/delete_chauffeur", methods=["POST"])
def api_delete_chauffeur():
    ok = ChauffeurService.delete(request.json["cin"])
    return jsonify({"status": "ok" if ok else "not_found"})


@app.route("/api/update_chauffeur", methods=["POST"])
def api_update_chauffeur():
    data = request.json
    old_cin = data["old_cin"]
    updated = Chauffeur(
        data["cin"],
        data["nom"],
        data["prenom"],
        data["email"],
        data["adresse"],
        data["telephone"],
        data["poste"],
        data["salaire"]
    )
    ok = ChauffeurService.update(old_cin, updated)
    return jsonify({"status": "ok" if ok else "not_found"})


# ==================================================================
#  VEHICULES
# ==================================================================
@app.route("/vehicules")
def vehicules_page():
    role_required("admin")
    return render_template("gestion_vehicules.html")


@app.route("/api/vehicules")
def api_vehicules():
    v = VehiculeService.load_all()
    return jsonify({"vehicules": [x.to_dict() for x in v]})


@app.route("/api/add_vehicule", methods=["POST"])
def api_add_vehicule():
    v = Vehicule(**request.json)
    VehiculeService.add(v)
    return jsonify({"status": "ok"})


@app.route("/api/delete_vehicule", methods=["POST"])
def api_delete_vehicule():
    ok = VehiculeService.delete(request.json["matricule"])
    return jsonify({"status": "ok" if ok else "not_found"})


@app.route("/api/update_vehicule", methods=["POST"])
def api_update_vehicule():
    data = request.json
    old = data["old_matricule"]
    updated = Vehicule(
        data["matricule"],
        data["marque"],
        data["capacite"],
        data["prix"],
        data["age"]
    )
    ok = VehiculeService.update(old, updated)
    return jsonify({"status": "ok" if ok else "not_found"})


# ==================================================================
#  POINTS DE COLLECTE (admin)
# ==================================================================
@app.route("/points")
def points_page():
    role_required("admin")
    return render_template("points.html")


@app.route("/api/points")
def api_points():
    pts = PointService.load_all()
    return jsonify({"points": [p.to_dict() for p in pts]})


@app.route("/api/add_point", methods=["POST"])
def api_add_point():
    p = Point(**request.json)
    PointService.add(p)
    return jsonify({"status": "ok"})


@app.route("/api/delete_point", methods=["POST"])
def api_delete_point():
    ok = PointService.delete(request.json["lat"], request.json["lng"])
    return jsonify({"status": "ok" if ok else "not_found"})


# ==================================================================
# START SERVER
# ==================================================================
if __name__ == "__main__":
    app.run(debug=True)
