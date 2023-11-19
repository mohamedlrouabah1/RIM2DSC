import sys
import os

# Obtenir le chemin absolu du dossier "src"
src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")

# Ajouter le chemin du dossier "src" dans sys.path
sys.path.insert(0, src_dir)