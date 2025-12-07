class ProblemeCarte:
    def __init__(self, id, type, description, date, status):
        self.id = id
        self.type = type
        self.description = description
        self.date = date
        self.status = status  # "nouveau", "technicien", "admin"

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "description": self.description,
            "date": self.date,
            "status": self.status
        }
