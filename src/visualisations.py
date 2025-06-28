import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime, timedelta
from matplotlib.figure import Figure


from matplotlib.figure import Figure

def courbe_emprunts(fichier_historique="../data/historique.csv"):
    dates = []

    with open(fichier_historique, "r", encoding="utf-8") as f:
        for ligne in f:
            parts = ligne.strip().split(",")
            if len(parts) >= 4 and parts[3].strip() == "emprunt":
                try:
                    date_obj = datetime.strptime(parts[0], "%Y-%m-%d %H:%M:%S")
                    dates.append(date_obj.date())
                except:
                    continue

    aujourd_hui = datetime.today().date()
    jours = [aujourd_hui - timedelta(days=i) for i in range(29, -1, -1)]
    activite = [dates.count(jour) for jour in jours]

    fig = Figure(figsize=(4, 3))
    ax = fig.add_subplot(111)
    ax.plot(jours, activite, marker='o')
    ax.set_title("Emprunts des 30 derniers jours")
    ax.set_xlabel("Date")
    ax.set_ylabel("Nombre d'emprunts")
    fig.autofmt_xdate()  # Pour incliner les dates

    return fig


def livre_par_genre(fichier_source = "../data/livres.txt"):
    genres = []
    with open(fichier_source, "r", encoding="utf-8") as f:
        for ligne in f:
            # "strip()" enlève les espaces ou retours à la ligne en début , fin
            # "split(";")" découpe la ligne en morceaux à chaque ";"
            parts = ligne.strip().split(";")
            if(len(parts) >= 5):
                genres.append(parts[3])
    compteur = Counter(genres)
    genre = list(compteur.keys())
    valeurs = list(compteur.values())

    fig = Figure(figsize=(6, 3))
    ax = fig.add_subplot(111)
    ax.pie(valeurs, labels=genre, autopct="%1.1f%%", startangle=90)
    ax.set_title("Répartition des livres par genre")
    ax.axis("equal")
    return fig

def livre_par_statut(fichier_source = "../data/livres.txt"):
    statuts = []
    with open(fichier_source, "r", encoding="utf-8") as f:
        for ligne in f:
            parts = ligne.strip().replace(".", "").split(";")
            if len(parts) == 6:
                statuts.append(parts[5].strip())  # ✅ Ajout correct

    compteur = Counter(statuts)
    statut = list(compteur.keys())
    valeurs = list(compteur.values())

    fig = Figure(figsize=(4, 3))
    ax = fig.add_subplot(111)
    ax.pie(valeurs, labels=statut, autopct="%1.1f%%", startangle=90)
    ax.set_title("Répartition des livres : disponibles vs empruntés")
    ax.axis("equal")  # ✅ Garder le cercle rond
    return fig

def histogramme(fichier_source = "../data/livres.txt"):
    auteurs = []
    with open(fichier_source, "r", encoding="utf-8") as f:
        for ligne in f:
            parts = ligne.strip().split(";")
            if len(parts) >= 3:
                auteurs.append(parts[2])

    compteur = Counter(auteurs)
    top_auteurs = compteur.most_common(10)

    auteur = [a[0] for a in top_auteurs]
    nombres = [a[1] for a in top_auteurs]

    fig = Figure(figsize=(8, 3))
    ax = fig.add_subplot(111)
    ax.bar(auteur, nombres)
    ax.set_xlabel("Auteurs")
    ax.set_ylabel("Nombres de livres")
    ax.set_title("Top 10 des auteurs par nombre de livres")

    return fig

