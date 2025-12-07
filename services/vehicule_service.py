import xml.etree.ElementTree as ET
from models.vehicule import vehicule
from services.indent_xml import indent

FILE = "data/vehicules.xml"

class vehiculeservice:

    @staticmethod
    def load_all():
        tree = ET.parse(FILE)
        root = tree.getroot()
        vehicules = []

        for v in root.findall("vehicule"):
            vehicules.append(vehicule(
                v.find("matricule").text.strip(),
                v.find("marque").text.strip(),
                v.find("capacite").text.strip(),
                v.find("prix").text.strip(),
                v.find("age").text.strip()
            ))
        return vehicules

    @staticmethod
    def add(v: vehicule):
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
        matricule = str(matricule).strip()

        for v in root.findall("vehicule"):
            if v.find("matricule").text.strip() == matricule:
                root.remove(v)
                indent(root)
                tree.write(FILE, encoding="UTF-8", xml_declaration=True)
                return True
        return False

    @staticmethod
    def update(old_mat, new_v: vehicule):
        tree = ET.parse(FILE)
        root = tree.getroot()

        for v in root.findall("vehicule"):
            if v.find("matricule").text.strip() == old_mat.strip():
                for k, val in new_v.to_dict().items():
                    node = v.find(k)
                    if node is not None:
                        node.text = str(val)

                indent(root)
                tree.write(FILE, encoding="UTF-8", xml_declaration=True)
                return True

        return False
