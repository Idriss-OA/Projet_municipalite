import xmlschema

XSD_FILE = "data/validation.xsd"

class XMLValidator:

    @staticmethod
    def validate(xml_file):
        try:
            schema = xmlschema.XMLSchema(XSD_FILE)
            schema.validate(xml_file)
            return True, ""
        except xmlschema.XMLSchemaException as e:
            return False, str(e)
