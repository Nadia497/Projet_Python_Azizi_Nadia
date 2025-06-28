class Livre:
    def __init__(self, ISBN, titre, auteur, annee, genre, statut= "disponible" ):
        self.ISBN = ISBN
        self.titre = titre
        self.auteur = auteur
        self.annee = annee
        self.genre = genre
        self.statut = statut

class Membre:
    def __init__(self, ID, nom):
        self.ID = ID
        self.nom = nom
        self.livres_empruntee = []

class Bibliotheque:
    def __init__(self):
        self.livres = []
        self.membres = []

    def ajouter_livre(self,livre:Livre):
        if livre.statut == "disponible" or livre.statut == "emprunte":
            print(f"le livre {livre.titre} est déjà disponible")
        else:
            self.livres.append(livre)
            print(f"le livre {livre.titre} a été ajouter")

    def supprimer_livre(self,livre:Livre):
        if livre in self.livres:
            self.livres.remove(livre)
            print(f"{livre.titre} supprimer avec succées")
        else:
            print(f"{livre.titre} n'existe pas dans la bibliotheque")

    def enregistrer_member(self,member:Member):
        if member not in self.membres:
            self.members.append(member)
            print(f"{member.nom} a été enregistré")
        else:
            print(f"{member.nom} est déjà enregistré")

    def emprunter(self,livre:Livre,member:Membre):
        if livre in self.livres and livre.statut == "disponible":
            if membre in self.membres:
                membre.livres_empruntee.append(livre)
                livre.statut = "emprunte"
                print(f"{member.nom} a emprunté '{livre.titre}'.")
            else :
                print(f"{membre.nom} n'est pas enregistré")
        else:
            print(f"Le livre '{livre.titre}' n'est pas disponible.")


    def retours(self, livre:Livre, membre:Membre):
        if livre in membre.livres_empruntee:
            membre.livres_empruntee.remove(livre)
            livre.statut = "disponible"
            print(f"{livre.titre} a été retourné par {membre.nom} .")
        else:
            print(f"{membre.nom} n'a pas emprunté {livre.titre} .")

    def sauvegarder


