"""
Extract  informations from run result files and then
plot precision/recall and ROC curves for each run.
"""
import os
import json
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt


ROOT_DIR = './results'

def extract_columns(dir, fname):
    res = {
        'AgP': {},
        'gP': [],
        'gR': []
    }

    with open(f'{dir}/{fname}') as f:
        for line in f:

            line = line.split()

            if len(line) != 3:
                continue

            col, query, val = line

            if query not in res:
                res[query] = {}

            if col.startswith('gP'):
                res[query]['gP'].append(float(val))
            elif col.startswith('gR'):
                res[query]['gR'].append(float(val))
            else:
                res[query][col] = val

    return res


def parse_run_result_dir(dir_name:str) -> dict:
    res = {}

    for fname in os.listdir(dir_name):
        if fname.endswith('.txt'):
            res[fname] = extract_columns(dir_name, fname)

    return res


def compute_positif_rates(data):
    true_positive_rate = data['num_rel_ret'] / data['num_rel']

    false_positive_rate = (data['ret_size'] - data['rel_size']) / (data['ret_size'] - data['rel_ret_size'])

    return true_positive_rate, false_positive_rate


def compute_roc_curve(resultats, file_name):
    plt.figure(figsize=(8, 8))

    for query_result in resultats:
        num_rel = query_result['num_rel']
        num_rel_ret = query_result['num_rel_ret']
        ret_size = query_result['ret_size']
        rel_size = query_result['rel_size']
        rel_ret_size = query_result['rel_ret_size']

        true_positive_rate, false_positive_rate = compute_positif_rates(num_rel, num_rel_ret, ret_size, rel_size, rel_ret_size)

        # Calcul de la courbe ROC
        fpr, tpr, _ = roc_curve([0, 1], [false_positive_rate, true_positive_rate])
        roc_auc = auc(fpr, tpr)

        # Affichage de la courbe ROC pour chaque requête
        plt.plot(fpr, tpr, label=f'Requête {len(resultats)} (AUC = {roc_auc:.2f})')

    plt.plot([0, 1], [0, 1], linestyle='--', color='grey', label='Aléatoire')
    plt.xlabel('Taux de Faux Positif (False Positive Rate)')
    plt.ylabel('Taux de Vrai Positif (True Positive Rate)')
    plt.title('Courbe ROC pour plusieurs requêtes')
    plt.legend()

    plt.savefig(file_name)
    plt.show()



def tracer_courbe_precision_recall(data, file_name):
    """
    Example of data format
    donnees = [
        "gP[1]\t2009011\t0.0",
        "gR[1]\t2009011\t0.038461538461538464",
        "gP[2]\t2009011\t0.0",
        "gR[2]\t2009011\t0.07692307692307693",
        "gP[3]\t2009011\t0.0",
        "gR[3]\t2009011\t0.07692307692307693",
        "gP[5]\t2009011\t0.0",
        "gR[5]\t2009011\t0.07692307692307693",
        "gP[10]\t2009011\t0.0",
        "gR[10]\t2009011\t0.07692307692307693",
        "gP[25]\t2009011\t0.0",
        "gR[25]\t2009011\t0.19230769230769232",
        "gP[50]\t2009011\t0.01997986270022883",
        "gR[50]\t2009011\t0.2692307692307692",
        "AgP\t2009011\t0.015604691539409967"
    ]
    """
    precision = {}
    rappel = {}

    # Extraction des données de précision et de rappel
    for line in data:
        if line.startswith('gP'):
            _, k, value = line.split('\t')
            precision[int(k[2:])] = float(value)
        elif line.startswith('gR'):
            _, k, value = line.split('\t')
            rappel[int(k[2:])] = float(value)

    # Conversion des dictionnaires en listes triées
    k_values = sorted(precision.keys())
    precision_values = [precision[k] for k in k_values]
    rappel_values = [rappel[k] for k in k_values]

    # Tracé de la courbe précision-rappel
    plt.plot(rappel_values, precision_values, marker='o', linestyle='-', label='Courbe Precision-Recall')
    plt.xlabel('Rappel (Recall)')
    plt.ylabel('Précision (Precision)')
    plt.title('Courbe Precision-Recall pour différentes valeurs de k')
    plt.legend()

    plt.savefig(file_name)
    plt.show()




if __name__ == '__main__':
    results_run = []

    for i in range(1, 9):
        results_run += \
            [parse_run_result_dir(f'{ROOT_DIR}/results_runs{i}')]

    with open('parsed_results.json', 'w') as f:
        json.dump(results_run, f)