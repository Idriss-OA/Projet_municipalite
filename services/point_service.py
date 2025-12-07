import xml.etree.ElementTree as ET
from models.point import point
from services.indent_xml import indent

FILE = "data/points.xml"

class pointservice:

    @staticmethod
    def load_all():
        tree = ET.parse(FILE)
        root = tree.getroot()
        points = []

        for p in root.findall("point"):
            points.append(point(
                p.find("lat").text,
                p.find("lng").text,
                p.find("type").text,
                p.find("capacite").text,
                p.find("niveau").text
            ))
        return points

    @staticmethod
    def add(p: point):
        tree = ET.parse(FILE)
        root = tree.getroot()

        el = ET.Element("point")
        for k, v in p.to_dict().items():
            ET.SubElement(el, k).text = str(v)

        root.append(el)
        indent(root)
        tree.write(FILE, encoding="UTF-8", xml_declaration=True)

    @staticmethod
    def delete(lat, lng):
        tree = ET.parse(FILE)
        root = tree.getroot()

        for p in root.findall("point"):
            if p.find("lat").text == str(lat) and p.find("lng").text == str(lng):
                root.remove(p)
                indent(root)
                tree.write(FILE, encoding="UTF-8", xml_declaration=True)
                return True
        return False
