"""
Extract  AgP et MAgP des fichiers de résultats de run
"""
import os
import json


ROOT_DIR = './results'

def extract_columns(dir, fname, columns=['MAgP', 'AgP']):
    res = {
        'AgP': {}
    }

    with open(f'{dir}/{fname}') as f:
        for line in f:
            line = line.split()
            if len(line) != 3:
                continue
            col, query, val = line

            # if col == columns[0] and query == 'all':
            #     res[col] = val
            # elif col == columns[1]:
            #     res[col][query] = val
            if query not in res:
                res[query] = {}
            res[query][col] = val

    if res['AgP'] == {}:
        del res['AgP']

    return res


def parse_run_result_dir(dir_name):
    res = {}

    for fname in os.listdir(dir_name):
        if fname.endswith('.txt'):
            res[fname] = extract_columns(dir_name, fname)

    return res

if __name__ == '__main__':
    results_run = []

    for i in range(1, 9):
        results_run += \
            [parse_run_result_dir(f'{ROOT_DIR}/results_runs{i}')]

    with open('parsed_results.json', 'w') as f:
        json.dump(results_run, f)