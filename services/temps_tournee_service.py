import xml.etree.ElementTree as ET
from services.indent_xml import indent
from models.temps_tournee import TempsTournee
from services.xml_validator import XMLValidator

FILE = "data/temps_tournee.xml"

class TempsTourneeService:

    @staticmethod
    def load_all():
        tree = ET.parse(FILE)
        root = tree.getroot()
        records = []

        for t in root.findall("temps"):
            records.append(TempsTournee(
                t.find("id_tournee").text,
                t.find("chauffeur").text,
                t.find("start_time").text,
                t.find("end_time").text,
                t.find("temps_total").text
            ))
        return records

    @staticmethod
    def start(id_tournee, chauffeur, start_time):
        tree = ET.parse(FILE)
        root = tree.getroot()

        el = ET.SubElement(root, "temps")

        ET.SubElement(el, "id_tournee").text = id_tournee
        ET.SubElement(el, "chauffeur").text = chauffeur
        ET.SubElement(el, "start_time").text = start_time
        ET.SubElement(el, "end_time").text = ""
        ET.SubElement(el, "temps_total").text = ""

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
    def finish(id_tournee, end_time, temps_total):
        tree = ET.parse(FILE)
        root = tree.getroot()

        for t in root.findall("temps"):
            if t.find("id_tournee").text == id_tournee:
                t.find("end_time").text = end_time
                t.find("temps_total").text = str(temps_total)
                break

        indent(root)
        tree.write(FILE, encoding="UTF-8", xml_declaration=True)
        ok, error = XMLValidator.validate(FILE)

        if not ok:
            # On supprime l'élément invalide
            root.remove(el)
            tree.write(FILE, encoding="UTF-8", xml_declaration=True)
            return False, error

        return True, ""

