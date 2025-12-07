class tournee:
    def __init__(self, id, chauffeur, vehicule, date, points):
        self.id = id
        self.chauffeur = chauffeur
        self.vehicule = vehicule
        self.date = date
        self.points = points  # liste de lat,lng

    def to_dict(self):
        return {
            "id": self.id,
            "chauffeur": self.chauffeur,
            "vehicule": self.vehicule,
            "date": self.date,
            "points": self.points
        }
