from collections import Counter

def compter_apparitions_colonne(nom_fichier):
    try:
        with open(nom_fichier, 'r') as fichier:
            lignes = fichier.readlines()

            # Extraire les valeurs de la troisième colonne
            valeurs_colonne = [ligne.split()[2] for ligne in lignes if len(ligne.split()) >= 3 and ligne.split()[2] != ""]

            # Utiliser Counter pour compter les occurrences de chaque valeur
            compteur = Counter(valeurs_colonne)

            # Afficher le résultat
            for valeur, nombre_apparitions in compteur.items():
                print(f"La valeur '{valeur}' apparaît {nombre_apparitions} fois dans la troisième colonne.")

    except FileNotFoundError:
        print(f"Le fichier '{nom_fichier}' est introuvable.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

# Exemple d'utilisation
fichier_a_compter = 'tmp.txt'
compter_apparitions_colonne(fichier_a_compter)
