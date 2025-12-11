import xml.etree.ElementTree as ET
from services.indent_xml import indent
from models.probleme_carte import ProblemeCarte
from services.xml_validator import XMLValidator

FILE = "data/problemes_carte.xml"

class ProblemeCarteService:

    @staticmethod
    def load_all():
        tree = ET.parse(FILE)
        root = tree.getroot()
        problemes = []

        for p in root.findall("probleme"):
            problemes.append(ProblemeCarte(
                id=p.find("id").text,
                type=p.find("type").text,
                description=p.find("description").text,
                date=p.find("date").text,
                status=p.find("status").text
            ))
        return problemes

    @staticmethod
    def add(pb):
        tree = ET.parse(FILE)
        root = tree.getroot()

        el = ET.SubElement(root, "probleme")
        ET.SubElement(el, "id").text = pb.id
        ET.SubElement(el, "type").text = pb.type
        ET.SubElement(el, "description").text = pb.description
        ET.SubElement(el, "date").text = pb.date
        ET.SubElement(el, "status").text = pb.status

        indent(root)
        tree.write(FILE, encoding="UTF-8", xml_declaration=True)

    @staticmethod
    def update_status(id, new_status):
        tree = ET.parse(FILE)
        root = tree.getroot()

        for p in root.findall("probleme"):
            if p.find("id").text == id:
                p.find("status").text = new_status
                indent(root)
                tree.write(FILE, encoding="UTF-8", xml_declaration=True)
                return True
        return False
