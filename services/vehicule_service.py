import xml.etree.ElementTree as ET
from models.Vehicule import Vehicule
from services.indent_xml import indent

FILE = "data/vehicules.xml"

class VehiculeService:

    @staticmethod
    def load_all():
        tree = ET.parse(FILE)
        root = tree.getroot()
        vehicules = []
        for v in root.findall("vehicule"):
            vehicules.append(Vehicule(
                v.find("matricule").text,
                v.find("marque").text,
                int(v.find("capacite").text),
                float(v.find("prix").text),
                int(v.find("age").text)
            ))
        return vehicules

    @staticmethod
    def add(v: Vehicule):
        tree = ET.parse(FILE)
        root = tree.getroot()
        el = ET.Element("vehicule")
        for k, val in v.to_dict().items():
            ET.SubElement(el, k).text = str(val)
        root.append(el)
        indent(root)
        tree.write(FILE, encoding="UTF-8", xml_declaration=True)

    @staticmethod
    def delete(matricule):
        tree = ET.parse(FILE)
        root = tree.getroot()
        for v in root.findall("vehicule"):
            if v.find("matricule").text == matricule:
                root.remove(v)
                indent(root)
                tree.write(FILE, encoding="UTF-8", xml_declaration=True)
                return True
        return False

    @staticmethod
    def update(old_mat, new_v: Vehicule):
        tree = ET.parse(FILE)
        root = tree.getroot()
        for v in root.findall("vehicule"):
            if v.find("matricule").text == old_mat:
                for k, val in new_v.to_dict().items():
                    v.find(k).text = str(val)
                indent(root)
                tree.write(FILE, encoding="UTF-8", xml_declaration=True)
                return True
        return False

# ⚠️ Créer l’instance ici
vehicule_service = VehiculeService()
