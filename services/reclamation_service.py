import xml.etree.ElementTree as ET
from services.indent_xml import indent
from services.xml_validator import XMLValidator

FILE = "data/reclamations.xml"

class ReclamationService:

    @staticmethod
    def add(rec_type, cin, date, motif):
        tree = ET.parse(FILE)
        root = tree.getroot()

        el = ET.SubElement(root, "reclamation")

        ET.SubElement(el, "type").text = rec_type
        ET.SubElement(el, "cin").text = cin
        ET.SubElement(el, "date").text = date
        ET.SubElement(el, "motif").text = motif

        indent(root)
        tree.write(FILE, encoding="UTF-8", xml_declaration=True)

        # Validation XSD
        ok, error = XMLValidator.validate(FILE)
        if not ok:
            root.remove(el)
            tree.write(FILE, encoding="UTF-8", xml_declaration=True)
            return False, error

        return True, ""
    @staticmethod
    def update_status(index, new_status):
        tree = ET.parse("data/reclamations.xml")
        root = tree.getroot()

        recs = root.findall("reclamation")

        if index >= len(recs):
            return False

        recs[index].set("status", new_status)

        indent(root)
        tree.write("data/reclamations.xml", encoding="utf-8", xml_declaration=True)

        return True
    @staticmethod
    def load_all():
        tree = ET.parse(FILE)
        root = tree.getroot()
        recls = []

        for el in root.findall("reclamation"):
            rec = {
                "type": el.find("type").text,
                "cin": el.find("cin").text,
                "date": el.find("date").text,
                "motif": el.find("motif").text,
                "status": el.get("status", "pending")
            }
            recls.append(rec)

        return recls


