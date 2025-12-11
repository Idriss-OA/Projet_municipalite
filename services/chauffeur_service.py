import xml.etree.ElementTree as ET
from models.chauffeur import chauffeur
from services.indent_xml import indent
from services.xml_validator import XMLValidator

FILE = "data/chauffeurs.xml"

class chauffeurservice:

    @staticmethod
    def load_all():
        tree = ET.parse(FILE)
        root = tree.getroot()

        chauffeurs = []

        for ch in root.findall("chauffeur"):
            chauffeurs.append(chauffeur(
                ch.find("cin").text.strip(),
                ch.find("nom").text.strip(),
                ch.find("prenom").text.strip(),
                ch.find("email").text.strip(),
                ch.find("adresse").text.strip(),
                ch.find("telephone").text.strip(),
                ch.find("poste").text.strip(),
                ch.find("salaire").text.strip()
            ))

        return chauffeurs

    @staticmethod
    def add(c: chauffeur):
        tree = ET.parse(FILE)
        root = tree.getroot()

        el = ET.Element("chauffeur")
        for k, v in c.to_dict().items():
            ET.SubElement(el, k).text = str(v)

        root.append(el)
        indent(root)
        tree.write(FILE, encoding="UTF-8", xml_declaration=True)
        ok, error = XMLValidator.validate(FILE)

        if not ok:
            root.remove(el)
            tree.write(FILE, encoding="UTF-8", xml_declaration=True)
            return False, error  # ← message renvoyé
        return True, ""


    @staticmethod
    def delete(cin):
        tree = ET.parse(FILE)
        root = tree.getroot()
        cin = str(cin).strip()

        for ch in root.findall("chauffeur"):
            if ch.find("cin").text.strip() == cin:
                root.remove(ch)
                indent(root)
                tree.write(FILE, encoding="UTF-8", xml_declaration=True)
                return True

        return False

    @staticmethod
    def update(old_cin, new_ch: chauffeur):
        tree = ET.parse(FILE)
        root = tree.getroot()

        for ch in root.findall("chauffeur"):
            if ch.find("cin").text.strip() == old_cin.strip():

                for k, v in new_ch.to_dict().items():
                    node = ch.find(k)
                    if node is not None:
                        node.text = str(v)

                indent(root)
                tree.write(FILE, encoding="UTF-8", xml_declaration=True)
                return True

        return False
