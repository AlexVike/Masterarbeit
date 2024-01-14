import pandas as pd
import scipy.stats as stats
import os
import numpy as np

def calculate_differences(file_path):
    # Einlesen der Datei
    df = pd.read_excel(file_path)

    # Berechnung des Mittelwerts für jede Zeile ab der dritten Spalte
    means = df.iloc[:, 2:].mean(axis=1)

    # Umwandlung der Mittelwerte in ein Numpy-Array
    data = means.values

    return data


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
    results_output_path = os.path.join(base_path, dir, 'independent_ttest_results.txt')
    with open(results_output_path, 'w') as file:
        print_and_write(file, f"Verarbeite Ordner: {dir}")

        # Pfade zu den Pretest und Posttest Excel-Dateien für LC und NC
        pretest_path_lc = os.path.join(base_path, dir, 'Pretest_LC_Group.xlsx')
        posttest_path_lc = os.path.join(base_path, dir, 'Posttest_LC_Group.xlsx')
        pretest_path_nc = os.path.join(base_path, dir, 'Pretest_NC_Group.xlsx')
        posttest_path_nc = os.path.join(base_path, dir, 'Posttest_NC_Group.xlsx')

        # Berechnung der Differenzen
        pretest_lc = calculate_differences(pretest_path_lc)
        posttest_lc = calculate_differences(posttest_path_lc)
        pretest_nc = calculate_differences(pretest_path_nc)
        posttest_nc = calculate_differences(posttest_path_nc)

        differences_lc = posttest_lc - pretest_lc
        
        differences_nc = posttest_nc - pretest_nc
       

        # Durchführung des unabhängigen T-Tests
        result = stats.ttest_ind(differences_lc, differences_nc)
        t_stat = result.statistic
        p_value = result.pvalue
        df = result.df

        # Drucken und Speichern der Ergebnisse
        result_text = f"Unabhängiger T-Test für {dir}: Statistik = {t_stat}, p-Wert = {p_value}, df = {df}"
        print_and_write(file, result_text)

        # Hinzufügen der Ergebnisse zur Liste
        results.append({'Category': dir, 'Statistic': t_stat, 'P-value': p_value, 'df': df})

# Umwandeln der Liste in einen DataFrame und Speichern in einer Excel-Datei
results_df = pd.DataFrame(results)
excel_output_path = os.path.join(base_path, 'Gesamte_unabhängige_ttest_Ergebnisse.xlsx')
results_df.to_excel(excel_output_path, index=False)

print("Alle Ergebnisse wurden in der Excel-Datei gespeichert.")
