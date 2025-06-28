import tkinter as tk
from tkinter import messagebox
from bibliotheque import Bibliotheque, Livre, Membre
from visualisations import livre_par_genre, livre_par_statut, histogramme, courbe_emprunts

# Créer une instance de la bibliothèque
biblio = Bibliotheque()

# Créer la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Gestion de Bibliothèque")
fenetre.geometry("900x300")
fenetre.configure(bg="#f0f0f0")

# ============ FONCTIONS ============
def ajouter_livre():
    def valider():
        try:
            isbn = int(entry_isbn.get())
            if any(l.ISBN == isbn for l in biblio.livres):
                messagebox.showerror("Erreur", f"Le livre avec ISBN {isbn} existe déjà.")
                return
            livre = Livre(
                isbn,
                entry_titre.get(),
                entry_auteur.get(),
                int(entry_annee.get()),
                entry_genre.get()
            )
            biblio.ajouter_livre(livre)
            messagebox.showinfo("Succès", f"Le livre '{livre.titre}' a été ajouté avec succès.")
            top.destroy()
        except ValueError:
            messagebox.showerror("Erreur", "Entrées invalides")

    top = tk.Toplevel(fenetre)
    top.title("Ajouter un livre")
    champs = ["ISBN", "Titre", "Auteur", "Année", "Genre"]
    entries = {}
    for champ in champs:
        tk.Label(top, text=champ).pack()
        entry = tk.Entry(top)
        entry.pack()
        entries[champ.lower()] = entry

    entry_isbn = entries["isbn"]
    entry_titre = entries["titre"]
    entry_auteur = entries["auteur"]
    entry_annee = entries["année"]
    entry_genre = entries["genre"]

    tk.Button(top, text="Valider", command=valider).pack(pady=5)



def inscrire_membre():
    def valider():
        try:
            ID = int(entry_id.get())
            if any(m.ID == ID for m in biblio.membres):
                messagebox.showerror("Erreur", f"Un membre avec l'ID {ID} existe déjà.")
                return
            membre = Membre(ID, entry_nom.get())
            biblio.enregistrer_membre(membre)
            messagebox.showinfo("Succès", f"Membre {membre.nom} inscrit avec succès !")
            top.destroy()
        except ValueError:
            messagebox.showerror("Erreur", "Entrées invalides")

    top = tk.Toplevel(fenetre)
    top.title("Inscrire un membre")

    tk.Label(top, text="ID").pack()
    entry_id = tk.Entry(top)
    entry_id.pack()

    tk.Label(top, text="Nom").pack()
    entry_nom = tk.Entry(top)
    entry_nom.pack()

    tk.Button(top, text="Valider", command=valider).pack(pady=5)



def supprimer_livre():
    def valider():
        try:
            isbn = int(entry_isbn.get())
            livre = next((l for l in biblio.livres if l.ISBN == isbn), None)
            if livre:
                biblio.supprimer_livre(livre)
                messagebox.showinfo("Succès", f"Le livre '{livre.titre}' a été supprimé avec succès.")
                top.destroy()
            else:
                messagebox.showerror("Erreur", "Livre introuvable")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un ISBN valide.")

    top = tk.Toplevel(fenetre)
    top.title("Supprimer un livre")

    tk.Label(top, text="ISBN").pack()
    entry_isbn = tk.Entry(top)
    entry_isbn.pack()

    tk.Button(top, text="Supprimer", command=valider).pack(pady=5)


def supprimer_membre():
    def valider():
        try:
            ID = int(entry_id.get())
            membre = next((m for m in biblio.membres if m.ID == ID), None)
            if membre:
                livres_empruntes = len(membre.livres_empruntee)
                biblio.supprimer_membre(membre)
                if livres_empruntes > 0:
                    messagebox.showinfo("Succès", f"Le membre a été supprimé.\nSes {livres_empruntes} livres sont maintenant disponibles.")
                else:
                    messagebox.showinfo("Succès", "Le membre a été supprimé avec succès.")
                top.destroy()
            else:
                messagebox.showerror("Erreur", "Membre introuvable")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un ID valide.")

    top = tk.Toplevel(fenetre)
    top.title("Supprimer un membre")

    tk.Label(top, text="ID").pack()
    entry_id = tk.Entry(top)
    entry_id.pack()

    tk.Button(top, text="Supprimer", command=valider).pack(pady=5)


def emprunter_livre():
    def valider():
        try:
            isbn = int(entry_isbn.get())
            ID = int(entry_id.get())
            livre = next((l for l in biblio.livres if l.ISBN == isbn), None)
            membre = next((m for m in biblio.membres if m.ID == ID), None)
            if livre and membre:
                try:
                    biblio.emprunter(livre, membre)
                    messagebox.showinfo("Succès", f"Le livre '{livre.titre}' a été emprunté par {membre.nom}.")
                    top.destroy()
                except Exception as e:
                    messagebox.showerror("Erreur", str(e))
            else:
                messagebox.showerror("Erreur", "Livre ou membre introuvable")
        except ValueError:
            messagebox.showerror("Erreur", "Entrées invalides")

    top = tk.Toplevel(fenetre)
    top.title("Emprunter un livre")

    tk.Label(top, text="ISBN du livre").pack()
    entry_isbn = tk.Entry(top)
    entry_isbn.pack()

    tk.Label(top, text="ID du membre").pack()
    entry_id = tk.Entry(top)
    entry_id.pack()

    tk.Button(top, text="Valider", command=valider).pack(pady=5)

def retour_livre():
    def valider():
        try:
            isbn = int(entry_isbn.get())
            ID = int(entry_id.get())
            livre = next((l for l in biblio.livres if l.ISBN == isbn), None)
            membre = next((m for m in biblio.membres if m.ID == ID), None)
            if livre and membre:
                if livre not in membre.livres_empruntee:
                    messagebox.showerror("Erreur", f"{membre.nom} n'a pas emprunté ce livre.")
                else:
                    biblio.retours(livre, membre)
                    messagebox.showinfo("Succès", f"Le livre '{livre.titre}' a été retourné par {membre.nom}.")
                    top.destroy()
            else:
                messagebox.showerror("Erreur", "Livre ou membre introuvable")
        except ValueError:
            messagebox.showerror("Erreur", "Entrées invalides")

    top = tk.Toplevel(fenetre)
    top.title("Retour d'un livre")

    tk.Label(top, text="ISBN du livre").pack()
    entry_isbn = tk.Entry(top)
    entry_isbn.pack()

    tk.Label(top, text="ID du membre").pack()
    entry_id = tk.Entry(top)
    entry_id.pack()

    tk.Button(top, text="Valider", command=valider).pack(pady=5)



def afficher_livres():
    top = tk.Toplevel(fenetre)
    top.title("Liste des livres")
    for livre in biblio.livres:
        tk.Label(top, text=str(livre)).pack()

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def afficher_statistiques():
    top = tk.Toplevel(fenetre)
    top.title("Statistiques")
    top.geometry("1200x800")

    figures = [
        livre_par_genre(),
        livre_par_statut(),
        histogramme(),
        courbe_emprunts()
    ]

    for i, fig in enumerate(figures):
        canvas = FigureCanvasTkAgg(fig, master=top)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.grid(row=i // 2, column=i % 2, padx=10, pady=10)


def quitter():
    if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter ?"):
        fenetre.destroy()

# ============ INTERFACE ============
titre = tk.Label(fenetre, text="Bienvenue dans la Bibliothèque", font=("Arial", 16), bg="#f0f0f0")
titre.pack(pady=10)

btn_frame = tk.Frame(fenetre, bg="#f0f0f0")
btn_frame.pack(pady=10)

# Taille standard pour tous les boutons
btn_width = 25

# Liste des boutons à créer
btns = [
    ("Ajouter un livre", ajouter_livre),
    ("Inscrire un membre", inscrire_membre),
    ("Supprimer un livre", supprimer_livre),
    ("Supprimer un membre", supprimer_membre),
    ("Emprunter un livre", emprunter_livre),
    ("Retour d'un livre", retour_livre),
    ("Afficher les livres", afficher_livres),
    ("Afficher les statistiques", afficher_statistiques),
    ("Quitter", quitter)
]

# Organiser les boutons dans une grille 3x3
for i, (text, cmd) in enumerate(btns):
    row = i // 3
    col = i % 3
    tk.Button(btn_frame, text=text, command=cmd, width=btn_width, bg="#e0e0e0",
              relief="raised", font=("Arial", 12)).grid(row=row, column=col, padx=5, pady=5)

fenetre.mainloop()
