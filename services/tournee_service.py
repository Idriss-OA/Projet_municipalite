import xml.etree.ElementTree as ET
from services.indent_xml import indent
from models.tournee import tournee
from services.xml_validator import XMLValidator

FILE = "data/tournees.xml"

class tourneeservice:

    @staticmethod
    def load_all():
        tree = ET.parse(FILE)
        root = tree.getroot()
        tournees = []

        for t in root.findall("tournee"):
            points = []
            for p in t.find("points").findall("point"):
                points.append({"lat": p.find("lat").text, "lng": p.find("lng").text})

            tournees.append(tournee(
                t.find("id").text,
                t.find("chauffeur").text,
                t.find("vehicule").text,
                t.find("date").text,
                points
            ))

        return tournees

    @staticmethod
    def add(t: tournee):
        tree = ET.parse(FILE)
        root = tree.getroot()

        el = ET.SubElement(root, "tournee")
        ET.SubElement(el, "id").text = str(t.id)
        ET.SubElement(el, "chauffeur").text = t.chauffeur
        ET.SubElement(el, "vehicule").text = t.vehicule
        ET.SubElement(el, "date").text = t.date

        pts = ET.SubElement(el, "points")
        for p in t.points:
            p_el = ET.SubElement(pts, "point")
            ET.SubElement(p_el, "lat").text = str(p["lat"])
            ET.SubElement(p_el, "lng").text = str(p["lng"])

        indent(root)
        tree.write(FILE, encoding="UTF-8", xml_declaration=True)
        ok, error = XMLValidator.validate(FILE)

        if not ok:
            # On supprime l'élément invalide
            root.remove(el)
            tree.write(FILE, encoding="UTF-8", xml_declaration=True)
            return False, error

        return True, ""


    @staticmethod
    def chauffeur_busy(chauffeur, date):
        for t in tourneeservice.load_all():
            if t.chauffeur == chauffeur and t.date == date:
                return True
        return False

    @staticmethod
    def vehicule_busy(vehicule, date):
        for t in tourneeservice.load_all():
            if t.vehicule == vehicule and t.date == date:
                return True
        return False
    @staticmethod
    def delete(id):
        tree = ET.parse(FILE)
        root = tree.getroot()

        for t in root.findall("tournee"):
            if t.find("id").text == id:
                root.remove(t)
                indent(root)
                tree.write(FILE, encoding="UTF-8", xml_declaration=True)
                return True

        return False
    @staticmethod
    def update(id, chauffeur, vehicule, date):
        tree = ET.parse(FILE)
        root = tree.getroot()

        for t in root.findall("tournee"):
            if t.find("id").text == id:
                t.find("chauffeur").text = chauffeur
                t.find("vehicule").text = vehicule
                t.find("date").text = date

                indent(root)
                tree.write(FILE, encoding="UTF-8", xml_declaration=True)
                return True

        return False
