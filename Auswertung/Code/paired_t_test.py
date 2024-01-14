import pandas as pd
import scipy.stats as stats
import os
import numpy as np  # Importieren Sie numpy für die Verwendung von np.concatenate

def print_and_write(file, text):
    print(text)
    file.write(text + "\n")

# Basispfad zu den Ordnern
base_path = 'Auswertung'

# Verzeichnisnamen der Ordner
directories = ['1. Motivation', '2. Intrinsic Goal Orientation', '3. Extrinsic Goal Orientation', '4. Task Value','5. Control of Learning Beliefs', '6. Self-Efficacy', '7. Test Anxiety']  

# Liste für die Speicherung der Ergebnisse
results = []

# Funktion zur Berechnung der kombinierten Daten
def calculate_combined_data(pretest_path, posttest_path):
    # Einlesen der Dateien für LC und NC Gruppen
    pretest_lc_df = pd.read_excel(pretest_path.replace('Group_Type', 'LC'))
    posttest_lc_df = pd.read_excel(posttest_path.replace('Group_Type', 'LC'))
    pretest_nc_df = pd.read_excel(pretest_path.replace('Group_Type', 'NC'))
    posttest_nc_df = pd.read_excel(posttest_path.replace('Group_Type', 'NC'))

    # Berechnung der Mittelwerte jeder Zeile nach dem Ausschluss der ersten beiden Spalten
    pretest_lc_means = pretest_lc_df.iloc[:, 2:].mean(axis=1)
    posttest_lc_means = posttest_lc_df.iloc[:, 2:].mean(axis=1)
    pretest_nc_means = pretest_nc_df.iloc[:, 2:].mean(axis=1)
    posttest_nc_means = posttest_nc_df.iloc[:, 2:].mean(axis=1)

    # Kombinieren der Mittelwerte aus beiden Gruppen
    pretest_combined = np.concatenate((pretest_lc_means.values, pretest_nc_means.values))
    print(pretest_combined)
    posttest_combined = np.concatenate((posttest_lc_means.values, posttest_nc_means.values))
    print(posttest_combined)

    # Berechnung von Mittelwert und Standardabweichung der kombinierten Mittelwerte
    pretest_mean = np.mean(pretest_combined)
    pretest_std = np.std(pretest_combined, ddof=1) # ddof=1 für Stichprobenstandardabweichung
    posttest_mean = np.mean(posttest_combined)
    posttest_std = np.std(posttest_combined, ddof=1)

    return pretest_combined, posttest_combined, pretest_mean, pretest_std, posttest_mean, posttest_std


# Iteration über jeden Ordner
for dir in directories:
    results_output_path = os.path.join(base_path, dir, 'ttest_results.txt')
    with open(results_output_path, 'w') as file:
        print_and_write(file, f"Verarbeite Ordner: {dir}")

        for group_type in ['NC', 'LC']:
            # Pfade zu den Pretest und Posttest Excel-Dateien
            pretest_path = os.path.join(base_path, dir, f'Pretest_{group_type}_Group.xlsx')
            posttest_path = os.path.join(base_path, dir, f'Posttest_{group_type}_Group.xlsx')

            # Einlesen der Dateien und Berechnung des gepaarten t-Tests
            pretest_df = pd.read_excel(pretest_path)
            posttest_df = pd.read_excel(posttest_path)
            pretest_combined, posttest_combined, pretest_mean, pretest_std, posttest_mean, posttest_std = calculate_combined_data(pretest_path, posttest_path)
            result = stats.ttest_rel(pretest_combined, posttest_combined)

            # Drucken und Speichern der Ergebnisse
            result_text = f"Ergebnis für {group_type}-Gruppe in {dir}: {result}"
            print_and_write(file, result_text)

            # Hinzufügen der Ergebnisse zur Liste
            results.append({'Category': dir, 'Group': group_type, 'Statistic': result.statistic, 'P-value': result.pvalue, 'Degrees of Freedom': result.df})

# Umwandeln der Liste in einen DataFrame und Speichern in einer Excel-Datei
results_df = pd.DataFrame(results)
excel_output_path = os.path.join(base_path, 'Gesamte_ttest_Ergebnisse.xlsx')
results_df.to_excel(excel_output_path, index=False)

print("Alle Ergebnisse wurden in der Excel-Datei gespeichert.")
