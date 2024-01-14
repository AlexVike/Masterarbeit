import pandas as pd
import os

def calculate_descriptive_stats(file_path):
    # Einlesen der Datei
    df = pd.read_excel(file_path)

    # Berechnung des Mittelwerts für jede Zeile ab der dritten Spalte
    row_means = df.iloc[:, 2:].mean(axis=1)

    # Berechnung des Gesamtmittelwerts und der Gesamtstandardabweichung der Zeilenmittelwerte
    overall_mean = row_means.mean()
    overall_std = row_means.std()

    return f"{overall_mean:.2f}, {overall_std:.2f}"


# Basispfad zu den Ordnern
base_path = 'Auswertung'

# Verzeichnisnamen der Ordner
directories = ['1. Motivation', '2. Intrinsic Goal Orientation', '3. Extrinsic Goal Orientation', '4. Task Value', '5. Control of Learning Beliefs', '6. Self-Efficacy', '7. Test Anxiety']

# Leere Tabelle erstellen
table = pd.DataFrame(columns=['Strategien', 'LC Pretest:Mean,SD', 'LC Posttest:Mean,SD', 'NC Pretest:Mean,SD', 'NC Posttest:Mean,SD'])

# Iteration über jeden Ordner
for dir in directories:
    strategy = dir.split('. ')[1]  # Strategienamen extrahieren
    row = [strategy]

    for group_type in ['LC', 'NC']:
        for time in ['Pretest', 'Posttest']:
            file_path = os.path.join(base_path, dir, f'{time}_{group_type}_Group.xlsx')
            stats = calculate_descriptive_stats(file_path)
            row.append(stats)

    # Erweiterung des DataFrames
    table.loc[len(table)] = row

# Tabelle anzeigen
print(table)

# Optional: Tabelle in eine Excel-Datei speichern
output_path = os.path.join(base_path, 'zusammenfassende_deskriptive_statistiken.xlsx')
table.to_excel(output_path, index=False)
