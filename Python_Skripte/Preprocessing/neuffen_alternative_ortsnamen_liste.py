import pandas as pd
import warnings
from fuzzywuzzy import fuzz

'''
Band_1.xlsx ist der Export der gesetzen Tags in Transkribus.
Die Datei besteht aus den Tabs "Overview", "ort", "person", "berufsbezeichnung", "amt", und "ereignis".
Schlussendlich wurden für diese Untersuchung nur die Tabs "ort" und "person" verwendet.
Mit diesem Script kann ein Eindruck gewonnen werden, wie unterschiedlich die Schreibweisen der in den 
Amtsversammlungsprotokollen von Neuffen auftauchenden Orte waren.
'''

# Warnungen unterdrücken
warnings.simplefilter("ignore", UserWarning)

# Datei einlesen
df = pd.read_excel("Band_1.xlsx", sheet_name="ort")

# Filtern der Orte
# Wir nehmen alle Werte aus der Spalte "Value"
df_orte = df['Value'].dropna().unique()

# Orte aus der Orte.txt laden, dabei die Varianten ausklammern
with open("Orte.txt", "r", encoding="utf-8") as file:
    orts_liste = [line.strip() for line in file.readlines()]

# Funktion, um ähnliche Namen zu gruppieren und Alternativen zu speichern
def group_similar_names(df_orte, orts_liste, threshold=80):
    grouped_counts = {}

    for name in df_orte:
        best_match = None
        best_ratio = 0

        # Versuche, den besten Match aus den Orten zu finden
        for ort in orts_liste:
            ratio = fuzz.ratio(name.lower(), ort.lower())  # Fuzzy Matching, um ähnliche Schreibweisen zu finden
            if ratio > best_ratio and ratio >= threshold:
                best_match = ort
                best_ratio = ratio

        # Falls ein passender Hauptname gefunden wurde, füge den alternativen Namen hinzu
        if best_match:
            if best_match not in grouped_counts:
                grouped_counts[best_match] = {"Alternativen": [name]}
            else:
                grouped_counts[best_match]["Alternativen"].append(name)

    # Rückgabe der gruppierten Orte mit Alternativen (nur als Liste der Alternativen)
    grouped_list = [
        {"Value": key, "Alternativen": ", ".join(sorted(set(value["Alternativen"])))}
        for key, value in grouped_counts.items()
    ]
    return pd.DataFrame(grouped_list)

# Gruppierte Orte berechnen
grouped_counts = group_similar_names(df_orte, orts_liste)

# Sortiere nach Häufigkeit
grouped_counts_sorted = grouped_counts.sort_values(by="Alternativen", ascending=False)

# Speichern der Ergebnisse in einer Textdatei
with open("zaehlung_gruppiert_inkl_alternativen_orte.txt", "w", encoding="utf-8") as file:
    for index, row in grouped_counts_sorted.iterrows():
        file.write(f"{row['Value']}: (Alternativen: {row['Alternativen']})\n")

print("Fertig :)")
