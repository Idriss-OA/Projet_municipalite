class vehicule:
    def __init__(self, matricule, marque, capacite, prix, age):
        self.matricule = matricule
        self.marque = marque
        self.capacite = capacite
        self.prix = prix
        self.age = age

    def to_dict(self):
        return {
            "matricule": self.matricule,
            "marque": self.marque,
            "capacite": self.capacite,
            "prix": self.prix,
            "age": self.age
        }