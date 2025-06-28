from datetime import datetime
from exceptions import *
from visualisations import *

class Livre:
    def __init__(self, ISBN, titre, auteur, annee, genre, statut= "disponible" ):
        self.ISBN = ISBN
        self.titre = titre
        self.auteur = auteur
        self.annee = annee
        self.genre = genre
        self.statut = statut

    def __str__(self):
        return f"{self.ISBN} - {self.titre} ({self.auteur}, {self.annee}) [{self.genre}] - {self.statut}"

class Membre:
    def __init__(self, ID, nom):
        self.ID = ID
        self.nom = nom
        self.livres_empruntee = []

class Bibliotheque:
    def __init__(self):
        self.livres = []
        self.membres = []
        self.charger_livres()
        self.charger_membres()

    def ajouter_livre(self,livre:Livre):
        if any(l.ISBN == livre.ISBN for l in self.livres):
            print(f"Le livre avec ISBN {livre.ISBN} existe déjà.")
        else:
            self.livres.append(livre)
            print(f"le livre {livre.titre} a été ajouter")
            self.sauvegarder_livre()

    def supprimer_livre(self,livre:Livre):
        if livre not in self.livres:
            raise LivreInexistantError()
        self.livres.remove(livre)
        print(f"{livre.titre} supprimer avec succées")
        self.sauvegarder_livre()


    def enregistrer_membre(self,membre:Membre):
        if membre not in self.membres:
            self.membres.append(membre)
            print(f"{membre.nom} a été enregistré")
            self.sauvegarder_membre()
        else:
            print(f"{membre.nom} est déjà enregistré")

    def supprimer_membre(self,membre:Membre):
        if membre in self.membres:
            self.membres.remove(membre)
            for livre in membre.livres_empruntee:
                livre.statut = "disponible"
            self.sauvegarder_livre()
            print(f"{membre.nom} a été supprimé")
            self.sauvegarder_membre()
        else:
            print(f"{membre.nom} n'est pas enregidtrer")

    def emprunter(self,livre:Livre,membre:Membre):
        if livre not in self.livres :
            raise LivreInexistantError()
        if livre in self.livres and livre.statut != "disponible":
            raise LivreIndisponibleError()
        if membre not in self.membres:
            raise MembreInexistantError()
        else:
            if len(membre.livres_empruntee)>= 3 :
                raise QuotaEmpruntDepasseError()
            membre.livres_empruntee.append(livre)
            livre.statut = "emprunte"
            print(f"{membre.nom} a emprunté '{livre.titre}'.")
            self.enregistrer_historique(livre.ISBN, membre.ID, "emprunt")
            self.sauvegarder_livre()
            self.sauvegarder_membre()

    def retours(self, livre: Livre, membre: Membre):
        if livre not in self.livres:
            raise LivreInexistantError()
        if membre not in self.membres:
            raise MembreInexistantError()
        if livre not in membre.livres_empruntee:
            raise Exception(f"{membre.nom} n'a pas emprunté ce livre.")

        membre.livres_empruntee.remove(livre)
        livre.statut = "disponible"
        print(f"{livre.titre} a été retourné par {membre.nom}.")
        self.enregistrer_historique(livre.ISBN, membre.ID, "retour")
        self.sauvegarder_livre()
        self.sauvegarder_membre()

    def sauvegarder_livre(self):
        with open("../data/livres.txt", "w", encoding="utf-8") as f:
            for livre in self.livres:
                ligne = f"{livre.ISBN};{livre.titre};{livre.auteur};{livre.genre};{livre.annee};{livre.statut}\n"
                f.write(ligne)

    def sauvegarder_membre(self):
        print("Nombre de membres :", len(self.membres))
        with open("../data/membres.txt", "w", encoding="utf-8") as f:
            for membre in self.membres:
                livres_empruntes = ",".join([livre.titre for livre in membre.livres_empruntee])
                ligne = f"{membre.ID};{membre.nom};{livres_empruntes}.\n"
                f.write(ligne)

    def charger_livres(self):
        try:
            with open("../data/livres.txt", "r", encoding="utf-8") as f:
                for ligne in f:
                    ligne = ligne.strip()
                    if ligne.endswith("."):
                        ligne = ligne[:-1]
                    parts = ligne.split(";")
                    if len(parts) >= 6:
                        isbn = int(parts[0])
                        titre = parts[1]
                        auteur = parts[2]
                        genre = parts[3]
                        annee = int(parts[4])
                        statut = parts[5]
                        livre = Livre(isbn, titre, auteur, annee, genre, statut)
                        self.livres.append(livre)
        except FileNotFoundError:
            print("⚠️ Aucun fichier livres.txt trouvé.")

    def charger_membres(self):
        try:
            with open("../data/membres.txt", "r", encoding="utf-8") as f:
                for ligne in f:
                    parts = ligne.strip().split(";")
                    if len(parts) >= 2:
                        ID = int(parts[0])
                        nom = parts[1]
                        membre = Membre(ID, nom)

                        # Ajouter les livres empruntés (si précisés)
                        if len(parts) == 3:
                            isbn_list = parts[2].split(",")
                            for isbn in isbn_list:
                                livre = next((l for l in self.livres if str(l.ISBN) == isbn.strip()), None)
                                if livre:
                                    membre.livres_empruntee.append(livre)

                        self.membres.append(membre)
        except FileNotFoundError:
            print("⚠️ Aucun fichier membres.txt trouvé.")

    def enregistrer_historique(self,ISBN,ID_membre,action):
        try:
            with open("../data/historique.csv", "a", encoding="utf-8") as f:
                date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"{date},{ISBN},{ID_membre},{action}\n")
                print(f"[Historique] Action enregistrée : {action} par membre {ID_membre}")
        except Exception as e:
            print("Erreur lors de l'enregistrement historique :", e)

#exemple de main
def menu():
    biblio = Bibliotheque()
    while True:
        print("=== GESTION BIBLIOTHEQUE ===")
        print("1. Ajouter un livre")
        print("2. Inscrire un membre ")
        print("3. Emprunter un livre ")
        print("4. Rendre un livre ")
        print("5. Lister tous les livres ")
        print("6. Afficher les statistiques")
        print("7. Supprimer un livre ")
        print("8. Supprimer un membre ")
        print("9. Sauvegarder et quitter ")

        try:
            n = int(input("Quel action vous voulez faire : "))
        except ValueError:
            print("Saisie invalide. Entrez un nombre.")
            continue
        if n == 1 :
            isbn = int(input("Entrez l'ISBN du livre : "))
            title = input("Entrez le titre du livre : ")
            auteur =  input("L'auteur du livre : ")
            genre = input("Genre du livre : ")
            annee = int(input("Année de publicité : "))
            livre_ajouter = Livre(isbn, title, auteur, annee, genre)
            biblio.ajouter_livre(livre_ajouter)

        elif n == 2 :
            id = int(input("ID du membre : "))
            nom = input("Nom complet : ")

            # Vérifie si le membre existe déjà
            existe = any(m.ID == id for m in biblio.membres)

            if existe:
                print("Ce ID existe déjà. Choisissez un autre.")
            else:
                nv_membre = Membre(id, nom)
                biblio.enregistrer_membre(nv_membre)

        elif n == 3 :
            id_membre = int(input("Entrez l'id du membre : "))
            isbn_livre = int(input("Enrez l'isbn du livre a emprunter : "))

            livre = next((l for l in biblio.livres if l.ISBN == isbn_livre), None)
            membre = next((m for m in biblio.membres if m.ID == id_membre), None)
            if membre and livre:
                biblio.emprunter(livre, membre)
            else:
                print("Livre ou membre introuvable")

        elif n == 4 :
            id_membre = int(input("Entrez l'id du membre : "))
            isbn_livre = int(input("Enrez l'isbn du livre a emprunter : "))

            livre = next((l for l in biblio.livres if l.ISBN == isbn_livre), None)
            membre = next((m for m in biblio.membres if m.ID == id_membre), None)
            if membre and livre:
                biblio.retours(livre, membre)
                biblio.enregistrer_historique(isbn_livre, id_membre, "retour")
            else:
                print("livre ou membre introuvable")

        elif n == 5:
            print("Les livres existent dans la bibliotheque sont : \n")
            for livre in biblio.livres :
             print("-", livre)

        elif n == 6:
            print("affichage des statistiques: ")
            livre_par_genre()
            livre_par_statut()
            histogramme()
            courbe_emprunts()

        elif n == 7:
            isbn = int(input("Entrez l'ISBN du livre à supprimer : "))

            livre = next((l for l in biblio.livres if l.ISBN == isbn), None)
            if livre:
                biblio.supprimer_livre(livre)
            else:
                print("Livre introuvable")

        elif n == 8:
            id_membre = int(input("entrez l'id du membre à supprimer : "))

            membre = next((m for m in biblio.membres if m.ID == id_membre), None)
            if membre:
                biblio.supprimer_membre(membre)
            else:
                print("Membre introuvable")

        elif n == 9:
            print("Fermeture du programme.")
            break

        else:
            print("Choix invalide. Réessaye.")


#menu()

