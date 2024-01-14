import pandas as pd
import os

def calculate_descriptive_statistics(base_path, dir, group_type):
    pretest_path = os.path.join(base_path, dir, f'Pretest_{group_type}_Group.xlsx')
    posttest_path = os.path.join(base_path, dir, f'Posttest_{group_type}_Group.xlsx')

    # Laden der Daten
    pretest_df = pd.read_excel(pretest_path)
    posttest_df = pd.read_excel(posttest_path)

    # Deskriptive Statistiken
    pretest_descriptive = pretest_df.iloc[:, 2:].describe()
    posttest_descriptive = posttest_df.iloc[:, 2:].describe()

    # Veränderungen über die Zeit
    change = posttest_df.iloc[:, 2:].values - pretest_df.iloc[:, 2:].values
    change_descriptive = pd.DataFrame(change).describe()

    # Speichern der deskriptiven Statistiken in einer Excel-Datei
    output_path = os.path.join(base_path, dir, f'deskriptive_statistiken_{group_type}.xlsx')
    with pd.ExcelWriter(output_path) as writer:
        pretest_descriptive.to_excel(writer, sheet_name='Pretest')
        posttest_descriptive.to_excel(writer, sheet_name='Posttest')
        change_descriptive.to_excel(writer, sheet_name='Veränderungen')

# Basispfad zu den Ordnern
base_path = 'Auswertung'

# Verzeichnisnamen der Ordner
directories = ['1. Motivation', '2. Intrinsic Goal Orientation', '3. Extrinsic Goal Orientation', '4. Task Value', '5. Control of Learning Beliefs', '6. Self-Efficacy', '7. Test Anxiety']

# Gruppentypen
group_types = ['LC', 'NC']

# Iteration über jeden Ordner und Gruppentyp
for dir in directories:
    for group_type in group_types:
        calculate_descriptive_statistics(base_path, dir, group_type)
        print(f"Deskriptive Statistiken für {dir}, Gruppe {group_type} wurden gespeichert.")
