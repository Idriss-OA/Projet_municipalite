import xml.etree.ElementTree as ET
from models.chauffeur import Chauffeur
from services.indent_xml import indent

FILE = "data/chauffeurs.xml"

class ChauffeurService:

    @staticmethod
    def load_all():
        tree = ET.parse(FILE)
        root = tree.getroot()

        chauffeurs = []

        for ch in root.findall("chauffeur"):
            chauffeurs.append(Chauffeur(
                ch.find("cin").text,
                ch.find("nom").text,
                ch.find("prenom").text,
                ch.find("email").text,
                ch.find("adresse").text,
                ch.find("telephone").text,
                ch.find("poste").text,
                ch.find("salaire").text
            ))

        return chauffeurs

    @staticmethod
    def add(ch: Chauffeur):
        tree = ET.parse(FILE)
        root = tree.getroot()

        el = ET.Element("chauffeur")

        for k, v in ch.to_dict().items():
            ET.SubElement(el, k).text = str(v)

        root.append(el)
        indent(root)
        tree.write(FILE, encoding="UTF-8", xml_declaration=True)

    @staticmethod
    def delete(cin):
        tree = ET.parse(FILE)
        root = tree.getroot()

        for ch in root.findall("chauffeur"):
            if ch.find("cin").text == cin:
                root.remove(ch)
                indent(root)
                tree.write(FILE, encoding="UTF-8", xml_declaration=True)
                return True

        return False

    @staticmethod
    def update(old_cin, new_ch: Chauffeur):
        tree = ET.parse(FILE)
        root = tree.getroot()

        for ch in root.findall("chauffeur"):
            if ch.find("cin").text == old_cin:

                for k, v in new_ch.to_dict().items():
                    ch.find(k).text = str(v)

                indent(root)
                tree.write(FILE, encoding="UTF-8", xml_declaration=True)
                return True

        return False
