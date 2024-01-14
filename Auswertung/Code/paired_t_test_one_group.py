import pandas as pd
import scipy.stats as stats
import os
import numpy as np

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




def print_and_write(file, text):
    print(text)
    file.write(text + "\n")

# Basispfad zu den Ordnern
base_path = 'Auswertung'

# Verzeichnisnamen der Ordner
directories = ['1. Motivation', '2. Intrinsic Goal Orientation', '3. Extrinsic Goal Orientation', '4. Task Value', '5. Control of Learning Beliefs', '6. Self-Efficacy', '7. Test Anxiety']

# Liste für die Speicherung der Ergebnisse
results = []

# Iteration über jeden Ordner
for dir in directories:
    results_output_path = os.path.join(base_path, dir, 'combined_ttest_results.txt')
    with open(results_output_path, 'w') as file:
        print_and_write(file, f"Verarbeite Ordner: {dir}")

        # Pfade zu den Pretest und Posttest Excel-Dateien mit einem Platzhalter für die Gruppenart
        pretest_path = os.path.join(base_path, dir, 'Pretest_Group_Type_Group.xlsx')
        posttest_path = os.path.join(base_path, dir, 'Posttest_Group_Type_Group.xlsx')

        # Berechnung des gepaarten t-Tests für die kombinierte Gruppe
        pretest_combined, posttest_combined, pretest_mean, pretest_std, posttest_mean, posttest_std = calculate_combined_data(pretest_path, posttest_path)
        result = stats.ttest_rel(pretest_combined, posttest_combined)

        # Drucken und Speichern der Mittelwerte, Standardabweichungen und Cohens d
        stats_text = f"Mittelwert (Pretest): {pretest_mean}, Standardabweichung (Pretest): {pretest_std}, Mittelwert (Posttest): {posttest_mean}, Standardabweichung (Posttest): {posttest_std}"
        print_and_write(file, stats_text)

        # Drucken und Speichern der Ergebnisse
        result_text = f"Kombinierter Ergebnis in {dir}: {result}"
        print_and_write(file, result_text)

        # Hinzufügen der Ergebnisse zur Liste
        results.append({'Category': dir, 'Statistic': result.statistic, 'P-value': result.pvalue, 'Degrees of Freedom': result.df, 'Pretest Mean': pretest_mean, 'Pretest SD': pretest_std, 'Posttest Mean': posttest_mean, 'Posttest SD': posttest_std})

# Umwandeln der Liste in einen DataFrame und Speichern in einer Excel-Datei
results_df = pd.DataFrame(results)
excel_output_path = os.path.join(base_path, 'Gesamte_kombinierte_ttest_Ergebnisse.xlsx')
results_df.to_excel(excel_output_path, index=False)

print("Alle kombinierten Ergebnisse wurden in der Excel-Datei gespeichert.")
