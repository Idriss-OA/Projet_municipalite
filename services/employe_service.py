import xml.etree.ElementTree as ET
from models.Employe import Employe   # ✔ Import corrigé

FILE = "data/employes.xml"

class EmployeService:

    @staticmethod
    def load_all():
        tree = ET.parse(FILE)
        root = tree.getroot()

        employes = []
        for emp in root.findall("employe"):
            employes.append(Employe(
                emp.find("cin").text,
                emp.find("nom").text,
                emp.find("prenom").text,
                emp.find("email").text,
                emp.find("adresse").text,
                emp.find("telephone").text,
                emp.find("poste").text,
                emp.find("salaire").text
            ))
        return employes

    @staticmethod
    def add(employe: Employe):
        tree = ET.parse(FILE)
        root = tree.getroot()

        e = ET.Element("employe")
        for k, v in employe.to_dict().items():
            ET.SubElement(e, k).text = str(v)

        root.append(e)
        tree.write(FILE, encoding="UTF-8", xml_declaration=True)

    @staticmethod
    def delete(cin):
        tree = ET.parse(FILE)
        root = tree.getroot()

        for emp in root.findall("employe"):
            if emp.find("cin").text == cin:
                root.remove(emp)
                tree.write(FILE, encoding="UTF-8", xml_declaration=True)
                return True
        return False

    @staticmethod
    def update(old_cin, new_employe: Employe):
        tree = ET.parse(FILE)
        root = tree.getroot()

        for emp in root.findall("employe"):
            if emp.find("cin").text == old_cin:
                for k, v in new_employe.to_dict().items():
                    emp.find(k).text = str(v)
                tree.write(FILE, encoding="UTF-8", xml_declaration=True)
                return True

        return False
