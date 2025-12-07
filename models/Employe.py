class employe:
    def __init__(self, cin, nom, prenom, email, adresse, telephone, poste, salaire):
        self.cin = cin
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.adresse = adresse
        self.telephone = telephone
        self.poste = poste
        self.salaire = salaire

    def to_dict(self):
        return {
            "cin": self.cin,
            "nom": self.nom,
            "prenom": self.prenom,
            "email": self.email,
            "adresse": self.adresse,
            "telephone": self.telephone,
            "poste": self.poste,
            "salaire": self.salaire
        }