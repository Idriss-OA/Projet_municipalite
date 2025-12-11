import xml.etree.ElementTree as ET
from models.employe import employe
from services.indent_xml import indent
from services.xml_validator import XMLValidator

FILE = "data/employes.xml"

class employeservice:

    @staticmethod
    def load_all():
        tree = ET.parse(FILE)
        root = tree.getroot()

        employes = []
        for emp in root.findall("employe"):
            employes.append(employe(
                emp.find("cin").text.strip(),
                emp.find("nom").text.strip(),
                emp.find("prenom").text.strip(),
                emp.find("email").text.strip(),
                emp.find("adresse").text.strip(),
                emp.find("telephone").text.strip(),
                emp.find("poste").text.strip(),
                emp.find("salaire").text.strip()
            ))
        return employes

    @staticmethod
    def add(e: employe):
        tree = ET.parse(FILE)
        root = tree.getroot()

        el = ET.Element("employe")
        for k, v in e.to_dict().items():
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

        for emp in root.findall("employe"):
            if emp.find("cin").text.strip() == cin:
                root.remove(emp)
                indent(root)
                tree.write(FILE, encoding="UTF-8", xml_declaration=True)
                return True
        return False

    @staticmethod
    def update(old_cin, new_e: employe):   # ✅ DANS LA CLASSE !
        tree = ET.parse(FILE)
        root = tree.getroot()

        old_cin = str(old_cin).strip()

        for emp in root.findall("employe"):
            if emp.find("cin").text.strip() == old_cin:

                for k, v in new_e.to_dict().items():
                    node = emp.find(k)
                    if node is not None:
                        node.text = str(v)

                indent(root)
                tree.write(FILE, encoding="UTF-8", xml_declaration=True)
                return True
        ok, error = XMLValidator.validate(FILE)

        if not ok:
            root.remove(el)
            tree.write(FILE, encoding="UTF-8", xml_declaration=True)
            return False, error  # ← message renvoyé
        return True, ""


        return False
