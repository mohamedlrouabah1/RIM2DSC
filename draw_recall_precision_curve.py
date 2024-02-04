import matplotlib.pyplot as plt

# Vos données
data = {
    '2009011': {'gP': [0.0, 0.0, 0.0, 0.0, 0.0, 0.01997986270022883], 'gR': [0.038461538461538464, 0.07692307692307693, 0.07692307692307693, 0.07692307692307693, 0.19230769230769232, 0.2692307692307692]},
    '2009036': {'gP': [0.0, 0.49984214087048034, 0.6663872112191124, 0.42986065534336537, 0.21493032767168269, 0.11956844744373131], 'gR': [0.0, 0.007352941176470588, 0.014705882352941176, 0.022058823529411766, 0.051470588235294115, 0.08823529411764706]},
    # Ajoutez plus de données ici...
}

# Tracer les courbes
for run_id, metrics in data.items():
    plt.plot(metrics['gR'], metrics['gP'], label=run_id)

plt.xlabel('Rappel')
plt.ylabel('Précision')
plt.title('Courbe Rappel-Précision')
plt.legend()
plt.show()



OU

import matplotlib.pyplot as plt
import numpy as np

# Remplacez ceci par le code pour lire vos données à partir de votre fichier de résultats
data = {
    '2009011': {'gP': [0.0, 0.0, 0.0, 0.0, 0.0, 0.01997986270022883], 'gR': [0.038461538461538464, 0.07692307692307693, 0.07692307692307693, 0.07692307692307693, 0.19230769230769232, 0.2692307692307692]},
    # Ajoutez plus de données ici...
}

# Tracer les courbes
for run_id, metrics in data.items():
    plt.figure(figsize=(10, 6))

    # Courbe de rappel-précision
    plt.subplot(2, 2, 1)
    plt.plot(metrics['gR'], metrics['gP'], label=run_id)
    plt.xlabel('Rappel')
    plt.ylabel('Précision')
    plt.title('Courbe Rappel-Précision')
    plt.legend()

    # Courbe ROC
    # Vous aurez besoin de calculer le taux de vrais positifs (TPR) et le taux de faux positifs (FPR) pour cela
    # TPR = TP / (TP + FN)
    # FPR = FP / (FP + TN)
    # plt.subplot(2, 2, 2)
    # plt.plot(FPR, TPR, label=run_id)
    # plt.xlabel('Taux de faux positifs')
    # plt.ylabel('Taux de vrais positifs')
    # plt.title('Courbe ROC')
    # plt.legend()

    plt.tight_layout()
    plt.show()
