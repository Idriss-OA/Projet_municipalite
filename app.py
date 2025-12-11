from flask import Flask, render_template, request, jsonify, session, redirect, url_for, abort
import xml.etree.ElementTree as ET
from datetime import datetime
# ================================
# IMPORT DES SERVICES
# ================================
from services.employe_service import employeservice
from services.chauffeur_service import chauffeurservice
from services.vehicule_service import vehiculeservice
from services.point_service import pointservice
from services.indent_xml import indent
from services.tournee_service import tourneeservice
from services.probleme_carte_service import ProblemeCarteService
from services.temps_tournee_service import TempsTourneeService
from services.reclamation_service import ReclamationService


# ================================
# IMPORT DES MODELS
# ================================
from models.employe import employe
from models.chauffeur import chauffeur
from models.vehicule import vehicule
from models.point import point
from models.tournee import tournee
from models.temps_tournee import TempsTournee
from models.reclamation import Reclamation
import uuid
# ================================
# CONFIG FLASK
# ================================
app = Flask(__name__)
app.secret_key = "super_secret_key_123"


# ================================
# MIDDLEWARE
# ================================
def role_required(*roles):
    """Autorise un ou plusieurs rôles dans une page"""
    if "role" not in session or session["role"] not in roles:
        abort(403)


# ================================
# PAGE LOGIN
# ================================
@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    # --------- Vérification ADMIN (users.xml) ----------
    tree = ET.parse("data/users.xml")
    root = tree.getroot()

    for u in root.findall("user"):
        if u.find("username").text == username and u.find("password").text == password:
            session["username"] = username
            session["role"] = u.find("role").text
            return jsonify({"status": "ok", "role": session["role"]})

    # --------- Vérification CLIENT (clients.xml) ----------
    tree = ET.parse("data/clients.xml")
    root = tree.getroot()

    for c in root.findall("client"):
        if c.find("username").text == username and c.find("password").text == password:
            session["username"] = username
            session["role"] = "client"
            session["cin"] = c.find("cin").text   # <-- IMPORTANT !
            return jsonify({"status": "ok", "role": "client"})


    # --------- Vérification EMPLOYÉ ----------
    for emp in employeservice.load_all():
        if emp.prenom == username and emp.cin == password:
            session["username"] = username
            session["role"] = "employe"
            return jsonify({"status": "ok", "role": "employe"})

    # --------- Vérification CHAUFFEUR ----------
    for ch in chauffeurservice.load_all():
        if ch.prenom == username and ch.cin == password:
            session["username"] = ch.cin       # <-- CIN !
            session["role"] = "chauffeur"
            session["chauffeur_nom"] = ch.prenom
            return jsonify({"status": "ok", "role": "chauffeur"})


    return jsonify({"status": "error"})

# ================================
# PAGE REGISTER (CRÉATION COMPTE)
# ================================
@app.route("/register")
def register_page():
    return render_template("register.html")
# ================================
# REGISTER - CREATION DE COMPTE
# ================================
@app.route("/register", methods=["POST"])
def register_post():
    data = request.json

    username = data["username"]
    email = data["email"]
    password = data["password"]
    lieu = data["lieu"]
    postal = data["postal"]
    cin = data["cin"]

    tree = ET.parse("data/clients.xml")
    root = tree.getroot()

    # Vérifier si username existe déjà
    for c in root.findall("client"):
        if c.find("username").text == username:
            return jsonify({"status": "exists"})

    # Créer le client
    new_client = ET.SubElement(root, "client")
    ET.SubElement(new_client, "username").text = username
    ET.SubElement(new_client, "email").text = email
    ET.SubElement(new_client, "password").text = password
    ET.SubElement(new_client, "lieu").text = lieu
    ET.SubElement(new_client, "postal").text = postal
    ET.SubElement(new_client, "cin").text = cin
    indent(root)

    tree.write("data/clients.xml", encoding="UTF-8", xml_declaration=True)

    return jsonify({"status": "ok"})



    # ------------------- Admins (users.xml) -------------------
    tree = ET.parse("data/users.xml")
    root = tree.getroot()

    for u in root.findall("user"):
        if u.find("username").text == username and u.find("password").text == password:
            session["username"] = username
            session["role"] = u.find("role").text
            return jsonify({"status": "ok", "role": session["role"]})

    # ------------------- Clients (clients.xml) -------------------
    tree = ET.parse("data/clients.xml")
    root = tree.getroot()

    for c in root.findall("client"):
        if c.find("username").text == username and c.find("password").text == password:
            session["username"] = username
            session["role"] = "client"
            return jsonify({"status": "ok", "role": "client"})

    # ------------------- Employés -------------------
    for emp in employeservice.load_all():
        if emp.prenom == username and emp.cin == password:
            session["username"] = username
            session["role"] = "employe"
            return jsonify({"status": "ok", "role": "employe"})

# --------- Vérification CHAUFFEUR ----------
        for ch in chauffeurservice.load_all():
            if ch.prenom == username and ch.cin == password:
                session["username"] = ch.cin            # ← CIN enregistré dans la session
                session["chauffeur_nom"] = ch.prenom    # optionnel
                session["role"] = "chauffeur"
                print("Connexion chauffeur : CIN =", ch.cin)
                return jsonify({"status": "ok", "role": "chauffeur"})



@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


# ================================
# DASHBOARDS
# ================================
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

@app.route("/tournees")
def tournees_page():
    role_required("employe")
    return render_template("gestion_tournees.html")
@app.route("/tournees/liste")
def tournees_liste_page():
    role_required("employe")
    return render_template("liste_tournees.html")

# ================================
# EMPLOYÉS
# ================================
@app.route("/employes")
def employes_page():
    role_required("admin")
    return render_template("gestion_employes.html")


@app.route("/api/employes")
def api_employes():
    data = [e.to_dict() for e in employeservice.load_all()]
    return jsonify({"employes": data})


@app.route("/api/add_employe", methods=["POST"])
def api_add_employe():
    e = employe(**request.json)
    employeservice.add(e)
    return jsonify({"status": "ok"})


@app.route("/api/delete_employe", methods=["POST"])
def api_delete_employe():
    ok = employeservice.delete(request.json["cin"])
    return jsonify({"status": "ok" if ok else "not_found"})


@app.route("/api/update_employe", methods=["POST"])
def api_update_employe():
    data = request.json

    old_cin = data["old_cin"]

    # Retirer old_cin avant de construire l'objet employe
    new_data = {k: v for k, v in data.items() if k != "old_cin"}

    updated = employe(**new_data)

    ok = employeservice.update(old_cin, updated)

    return jsonify({"status": "ok" if ok else "not_found"})



# ================================
# CHAUFFEURS
# ================================
@app.route("/chauffeurs")
def chauffeurs_page():
    role_required("admin")
    return render_template("gestion_chauffeurs.html")


@app.route("/api/chauffeurs")
def api_chauffeurs():
    data = [c.to_dict() for c in chauffeurservice.load_all()]
    return jsonify({"chauffeurs": data})


@app.route("/api/add_chauffeur", methods=["POST"])
def api_add_chauffeur():
    ch = chauffeur(**request.json)
    chauffeurservice.add(ch)
    return jsonify({"status": "ok"})


@app.route("/api/delete_chauffeur", methods=["POST"])
def api_delete_chauffeur():
    ok = chauffeurservice.delete(request.json["cin"])
    return jsonify({"status": "ok" if ok else "not_found"})


@app.route("/api/update_chauffeur", methods=["POST"])
def api_update_chauffeur():
    data = request.json

    old_cin = data["old_cin"]

    # Supprimer old_cin avant création de l'objet chauffeur
    new_data = {k: v for k, v in data.items() if k != "old_cin"}

    updated = chauffeur(**new_data)

    ok = chauffeurservice.update(old_cin, updated)

    return jsonify({"status": "ok" if ok else "not_found"})


# ================================
# VÉHICULES
# ================================
@app.route("/vehicules")
def vehicules_page():
    role_required("admin")
    return render_template("gestion_vehicules.html")


@app.route("/api/vehicules")
def api_vehicules():
    data = [v.to_dict() for v in vehiculeservice.load_all()]
    return jsonify({"vehicules": data})


@app.route("/api/add_vehicule", methods=["POST"])
def api_add_vehicule():
    v = vehicule(**request.json)
    vehiculeservice.add(v)
    return jsonify({"status": "ok"})


@app.route("/api/delete_vehicule", methods=["POST"])
def api_delete_vehicule():
    ok = vehiculeservice.delete(request.json["matricule"])
    return jsonify({"status": "ok" if ok else "not_found"})


@app.route("/api/update_vehicule", methods=["POST"])
def api_update_vehicule():
    data = request.json
    updated = vehicule(
        data["matricule"],
        data["marque"],
        data["capacite"],
        data["prix"],
        data["age"]
    )

    ok = vehiculeservice.update(data["old_matricule"], updated)
    return jsonify({"status": "ok" if ok else "not_found"})



# ================================
# POINTS DE COLLECTE
# ================================
@app.route("/points")
def points_page():
    role_required("admin", "employe")  # ✔ les deux peuvent gérer
    return render_template("points.html", role=session["role"])


@app.route("/points/table")
def points_table():
    role_required("admin")
    return render_template("points_table.html", role=session["role"])


@app.route("/api/points")
def api_points():
    data = [p.to_dict() for p in pointservice.load_all()]
    return jsonify({"points": data})


@app.route("/api/add_point", methods=["POST"])
def api_add_point():
    p = point(**request.json)
    pointservice.add(p)
    return jsonify({"status": "ok"})


@app.route("/api/delete_point", methods=["POST"])
def api_delete_point():
    ok = pointservice.delete(request.json["lat"], request.json["lng"])
    return jsonify({"status": "ok" if ok else "not_found"})

@app.route("/api/create_tournee", methods=["POST"])
def api_create_tournee():
    data = request.json

    chauffeur = data["chauffeur"]
    vehicule = data["vehicule"]
    date = data["date"]
    points = data["points"]

    # --- Vérification des champs ---
    if not chauffeur or not vehicule or not date or len(points) == 0:
        return jsonify({"status": "error", "msg": "Champs manquants !"})

    # --- Vérifier disponibilité chauffeur ---
    if tourneeservice.chauffeur_busy(chauffeur, date):
        return jsonify({
            "status": "busy",
            "msg": f"❌ Chauffeur {chauffeur} est déjà occupé à cette date"
        })

    # --- Vérifier disponibilité véhicule ---
    if tourneeservice.vehicule_busy(vehicule, date):
        return jsonify({
            "status": "busy",
            "msg": f"❌ Véhicule {vehicule} est déjà utilisé à cette date"
        })

    # --- Tout est OK → Créer tournée ---
    new_t = tournee(
        id=str(uuid.uuid4()),
        chauffeur=chauffeur,
        vehicule=vehicule,
        date=date,
        points=points
    )

    tourneeservice.add(new_t)

    return jsonify({"status": "ok", "msg": "✔ Tournée créée avec succès"})
@app.route("/api/tournees")
def api_tournees():
    data = [t.to_dict() for t in tourneeservice.load_all()]
    return jsonify({"tournees": data})
@app.route("/api/update_tournee", methods=["POST"])
def api_update_tournee():
    data = request.json

    id = data["id"]
    chauffeur = data["chauffeur"]
    vehicule = data["vehicule"]
    date = data["date"]

    tourneeservice.update(id, chauffeur, vehicule, date)

    return jsonify({"status": "ok"})

@app.route("/api/delete_tournee", methods=["POST"])
def api_delete_tournee():
    id = request.json["id"]
    ok = tourneeservice.delete(id)
    return jsonify({"status": "ok" if ok else "error"})
@app.route("/problemes_carte")
def probleme_carte_page():
    role_required("employe")
    return render_template("liste_problemes_carte.html")
@app.route("/api/problemes_carte")
def api_problemes_carte():
    data = [p.to_dict() for p in ProblemeCarteService.load_all()]
    return jsonify({"problemes": data})
@app.route("/api/probleme_carte/technicien", methods=["POST"])
def api_pb_technicien():
    id = request.json["id"]
    ProblemeCarteService.update_status(id, "technicien")
    return jsonify({"status": "ok"})
@app.route("/api/probleme_carte/admin", methods=["POST"])
def api_pb_admin():
    id = request.json["id"]
    ProblemeCarteService.update_status(id, "admin")
    return jsonify({"status": "ok"})
@app.route("/gestion_reclamations")
def gestion_reclamations_page():
    role_required("admin")   # seul admin peut voir
    return render_template("gestion_reclamations.html")
@app.route("/chauffeur/tournee")
def chauffeur_tournee_page():
    role_required("chauffeur")     # sécurité
    return render_template("chauffeur_tournee.html")
@app.route("/api/chauffeur/tournee")
def api_chauffeur_tournee():
    role_required("chauffeur")

    chauffeur_cin = session["username"]  # maintenant c’est le CIN 👍

    toutes = tourneeservice.load_all()

    mes_tournees = [
        t.to_dict() for t in toutes
        if t.chauffeur == chauffeur_cin
    ]

    return jsonify({"tournees": mes_tournees})
@app.route("/chauffeur/rapport")
def chauffeur_rapport_page():
    role_required("chauffeur")
    return render_template("rapport_fin_tournee.html")
@app.route("/api/chauffeur/rapport")
def api_chauffeur_rapport():
    role_required("chauffeur")

    cin = session["username"]  # CIN chauffeur

    all_records = TempsTourneeService.load_all()

    my_records = [
        r.to_dict() for r in all_records if r.chauffeur_cin == cin
    ]

    return jsonify({"rapport": my_records})

@app.route("/api/tournee/start", methods=["POST"])
def api_tournee_start():
    data = request.json
    id_tournee = data["id_tournee"]
    start = str(data["start"])
    chauffeur = session["username"]

    TempsTourneeService.start(id_tournee, chauffeur, start)
    return jsonify({"status": "ok"})


@app.route("/api/tournee/end", methods=["POST"])
def api_tournee_end():
    data = request.json
    id_tournee = data["id_tournee"]
    end = str(data["end"])
    total = str(data["temps_total"])

    TempsTourneeService.finish(id_tournee, end, total)
    return jsonify({"status": "ok"})
#----------------chauffeur,absence-----------------
@app.route("/chauffeur/absence")
def chauffeur_absence_page():
    role_required("chauffeur")
    return render_template("chauffeur_absence.html")
@app.route("/api/chauffeur/incident", methods=["POST"])
def api_incident():
    role_required("chauffeur")

    data = request.json
    cin = session["username"]
    date = data["date"]
    motif = data["motif"]

    ReclamationService.add("incident", cin, date, motif)

    return jsonify({"status": "ok"})

@app.route("/api/chauffeur/absence", methods=["POST"])
def api_absence():
    role_required("chauffeur")

    data = request.json
    cin = session["username"]
    date = data["date"]
    motif = data["motif"]

    ok, msg = ReclamationService.add(
        rec_type="absence",
        cin=cin,
        date=date,
        motif=motif
    )

    if not ok:
        return jsonify({"status": "error", "message": msg})

    return jsonify({"status": "ok"})

#-------chauffeur,incident--------------
@app.route("/chauffeur/incident")
def chauffeur_incident_page():
    role_required("chauffeur")
    return render_template("chauffeur_incident.html")
@app.route("/api/reclamation/incident", methods=["POST"])
def api_reclamation_incident():
    role_required("chauffeur")

    data = request.json
    chauffeur = session["username"]  # CIN du chauffeur

    # Construire le motif
    motif = (
        f"Position: ({data['lat']}, {data['lng']}) — "
        f"Description: {data['description']}"
    )

    today = datetime.now().strftime("%Y-%m-%d")

    ok, msg = ReclamationService.add(
        rec_type=data["type"],     # ← type sélectionné par le chauffeur
        cin=chauffeur,
        date=today,
        motif=motif
    )

    if not ok:
        return jsonify({"status": "error", "message": msg})

    return jsonify({"status": "ok"})




#------------client carte------------------
@app.route("/client/carte")
def client_carte_page():
    role_required("client")
    return render_template("client_points.html")
@app.route("/client/signaler_probleme")
def client_signaler_page():
    role_required("client")
    return render_template("client_signaler_probleme.html")
@app.route("/api/client/signaler_probleme", methods=["POST"])
def api_client_probleme():
    role_required("client")

    data = request.json
    cin = session["cin"]

    date = datetime.now().strftime("%Y-%m-%d")

    motif = (
        f"Point: ({data['lat']}, {data['lng']}) — "
        f"Problème: {data['pb_type']} — "
        f"Description: {data['description']}"
    )

    ok, msg = ReclamationService.add(
        rec_type="probleme_client",
        cin=cin,
        date=date,
        motif=motif
    )

    if not ok:
        return jsonify({"status": "error", "message": msg})

    return jsonify({"status": "ok"})

@app.route("/client/nouveau_point")
def client_new_point_page():
    role_required("client")
    return render_template("client_new_point.html")
@app.route("/api/reclamation/nouveau_point", methods=["POST"])
def api_reclamation_nouveau_point():
    role_required("client")

    data = request.json
    cin = session["cin"]  # CIN du client !

    motif = (
        f"Demande de nouveau point : "
        f"type={data['type']}, capacite={data['capacite']}, "
        f"position=({data['lat']}, {data['lng']})"
    )

    ok, msg = ReclamationService.add(
        rec_type="nouveau_point",
        cin=cin,
        date=datetime.now().strftime("%Y-%m-%d"),
        motif=motif
    )

    if not ok:
        return jsonify({"status": "error", "message": msg})

    return jsonify({"status": "ok"})
#--------------employe,reclamation----------------------
@app.route("/employe/reclamations")
def employe_reclamations_page():
    role_required("employe")
    return render_template("reclamations_employe.html")
@app.route("/api/reclamations")
def api_all_reclamations():
    recs = ReclamationService.load_all()
    return jsonify({"reclamations": recs})

@app.route("/api/reclamations/update", methods=["POST"])
def api_reclamations_update():
    data = request.json
    index = data["id"]
    new_status = data["status"]

    ok = ReclamationService.update_status(index, new_status)

    return jsonify({"status": "ok" if ok else "error"})
@app.route("/api/reclamations_admin")
def api_reclamations_admin():
    all_recs = ReclamationService.load_all()

    # ne garder que celles dont le status est "admin"
    filtered = [r for r in all_recs if r["status"] == "admin"]

    return jsonify({"reclamations": filtered})

# ================================
# START SERVER
# ================================
if __name__ == "__main__":
    app.run(debug=True)