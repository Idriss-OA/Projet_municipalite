class point:
    def __init__(self, lat, lng, type, capacite, niveau="0"):
        self.lat = float(lat)
        self.lng = float(lng)
        self.type = type
        self.capacite = capacite
        self.niveau = niveau  # niveau actuel de remplissage

    def to_dict(self):
        return {
            "lat": self.lat,
            "lng": self.lng,
            "type": self.type,
            "capacite": self.capacite,
            "niveau": self.niveau
        }
