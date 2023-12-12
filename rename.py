import os

# Chemin du répertoire contenant les fichiers
repertoire = "./results_coll_2000"
suffixe = "_2K"

# Parcourir tous les fichiers dans le répertoire
for nom_fichier in os.listdir(repertoire):
    chemin_complet = os.path.join(repertoire, nom_fichier)

    # Vérifier si c'est un fichier et s'il se termine par ".txt"
    if os.path.isfile(chemin_complet) and nom_fichier.endswith(".txt"):
        # Construire le nouveau nom de fichier avec "_2K" ajouté
        nouveau_nom = nom_fichier.replace(".txt", f"{suffixe}.txt")

        # Renommer le fichier
        os.rename(chemin_complet, os.path.join(repertoire, nouveau_nom))

print("Opération terminée.")
