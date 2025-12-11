class Reclamation:
    def __init__(self, type, cin, date, motif):
        self.type = type
        self.cin = cin
        self.date = date
        self.motif = motif

    def to_dict(self):
        return {
            "type": self.type,
            "cin": self.cin,
            "date": self.date,
            "motif": self.motif
        }
