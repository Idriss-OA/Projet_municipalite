class TempsTournee:
    def __init__(self, id_tournee, chauffeur_cin, start_time="", end_time="", temps_total=""):
        self.id_tournee = id_tournee
        self.chauffeur_cin = chauffeur_cin
        self.start_time = start_time
        self.end_time = end_time
        self.temps_total = temps_total

    def to_dict(self):
        return {
            "id_tournee": self.id_tournee,
            "chauffeur": self.chauffeur_cin,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "temps_total": self.temps_total
        }
