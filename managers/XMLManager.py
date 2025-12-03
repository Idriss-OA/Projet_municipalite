import xml.etree.ElementTree as ET

from models.Employe import Employe        # ✔ Imports corrigés
from models.Chauffeur import Chauffeur
from models.Vehicule import Vehicule
from models.Client import Client
from models.Point import Point            # ✔ si ton fichier s’appelle Point.py
from models.User import User              # ✔ si ton fichier s’appelle User.py

class XMLManager:

    def __init__(self, path):
        self.path = path
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()

    def save(self):
        self.tree.write(self.path, encoding="UTF-8", xml_declaration=True)

    # ================================
    # EMPLOYES
    # ================================
    def get_employes(self):
        employes = []
        for e in self.root.findall("employe"):
            employes.append(
                Employe(
                    e.find("cin").text,
                    e.find("nom").text,
                    e.find("prenom").text,
                    e.find("email").text,
                    e.find("adresse").text,
                    e.find("telephone").text,
                    e.find("poste").text,
                    e.find("salaire").text
                )
            )
        return employes

    def add_employe(self, emp: Employe):
        elem = ET.Element("employe")
        ET.SubElement(elem, "cin").text = emp.cin
        ET.SubElement(elem, "nom").text = emp.nom
        ET.SubElement(elem, "prenom").text = emp.prenom
        ET.SubElement(elem, "email").text = emp.email
        ET.SubElement(elem, "adresse").text = emp.adresse
        ET.SubElement(elem, "telephone").text = emp.telephone
        ET.SubElement(elem, "poste").text = emp.poste
        ET.SubElement(elem, "salaire").text = emp.salaire

        self.root.append(elem)
        self.save()

    def delete_employe(self, cin):
        for e in self.root.findall("employe"):
            if e.find("cin").text == cin:
                self.root.remove(e)
                self.save()
                return True
        return False

    def update_employe(self, cin, data):
        for e in self.root.findall("employe"):
            if e.find("cin").text == cin:
                for key, value in data.items():
                    if e.find(key) is not None:
                        e.find(key).text = value
                self.save()
                return True
        return False

    # ================================
    # CHAUFFEURS
    # ================================
    def get_chauffeurs(self):
        chauffeurs = []
        for c in self.root.findall("chauffeur"):
            chauffeurs.append(
                Chauffeur(
                    c.find("cin").text,
                    c.find("nom").text,
                    c.find("prenom").text,
                    c.find("email").text,
                    c.find("adresse").text,
                    c.find("telephone").text,
                    c.find("poste").text,
                    c.find("salaire").text
                )
            )
        return chauffeurs

    def add_chauffeur(self, ch: Chauffeur):
        elem = ET.Element("chauffeur")
        ET.SubElement(elem, "cin").text = ch.cin
        ET.SubElement(elem, "nom").text = ch.nom
        ET.SubElement(elem, "prenom").text = ch.prenom
        ET.SubElement(elem, "email").text = ch.email
        ET.SubElement(elem, "adresse").text = ch.adresse
        ET.SubElement(elem, "telephone").text = ch.telephone
        ET.SubElement(elem, "poste").text = ch.poste
        ET.SubElement(elem, "salaire").text = ch.salaire

        self.root.append(elem)
        self.save()

    def delete_chauffeur(self, cin):
        for c in self.root.findall("chauffeur"):
            if c.find("cin").text == cin:
                self.root.remove(c)
                self.save()
                return True
        return False

    def update_chauffeur(self, cin, data):
        for c in self.root.findall("chauffeur"):
            if c.find("cin").text == cin:
                for key, value in data.items():
                    if c.find(key) is not None:
                        c.find(key).text = value
                self.save()
                return True
        return False

    # ================================
    # VEHICULES
    # ================================
    def get_vehicules(self):
        vehicules = []
        for v in self.root.findall("vehicule"):
            vehicules.append(
                Vehicule(
                    v.find("matricule").text,
                    v.find("marque").text,
                    v.find("capacite").text,
                    v.find("prix").text,
                    v.find("age").text
                )
            )
        return vehicules

    def add_vehicule(self, v: Vehicule):
        elem = ET.Element("vehicule")
        ET.SubElement(elem, "matricule").text = v.matricule
        ET.SubElement(elem, "marque").text = v.marque
        ET.SubElement(elem, "capacite").text = v.capacite
        ET.SubElement(elem, "prix").text = v.prix
        ET.SubElement(elem, "age").text = v.age

        self.root.append(elem)
        self.save()

    def delete_vehicule(self, matricule):
        for v in self.root.findall("vehicule"):
            if v.find("matricule").text == matricule:
                self.root.remove(v)
                self.save()
                return True
        return False

    def update_vehicule(self, matricule, data):
        for v in self.root.findall("vehicule"):
            if v.find("matricule").text == matricule:
                for key, value in data.items():
                    if v.find(key) is not None:
                        v.find(key).text = value
                self.save()
                return True
        return False
