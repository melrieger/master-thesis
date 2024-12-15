import pandas as pd
import warnings
from fuzzywuzzy import fuzz

''' 
Band_1.xlsx ist der Export der gesetzen Tags in Transkribus.
Die Datei besteht aus den Tabs "Overview", "ort", "person", "berufsbezeichnung", "amt", und "ereignis".
Schlussendlich wurden für diese Untersuchung nur die Tabs "ort" und "person" verwendet.
Mit diesem Script wurde die Basis für "numerische" Kanten für die Netzwerkanalyse der Amtsversammlungsprotokolle
von Neuffen gelegt - wie oft kommt welche Person/welcher Ort in den Protokollen vor?
Zusätzlich wird verdeutlicht, wie variabel die Schreibweisen von Orts-/Personennamen ist und wie eine eindeutige
Zuordnung/Zählung so erschwert wird. 
'''

# Warnungen unterdrücken
warnings.simplefilter("ignore", UserWarning)

# Excel-Datei laden
df = pd.read_excel("Band_1.xlsx")

# Häufigkeit der Werte in der Spalte "Value" zählen
value_counts = df['Value'].value_counts().reset_index()
value_counts.columns = ['Value', 'Count']


# Funktion, um ähnliche Namen zu gruppieren und Alternativen zu speichern
def group_similar_names(value_counts, threshold=80):
    grouped_counts = {}

    # Iteriere durch alle Namen
    for name, count in zip(value_counts['Value'], value_counts['Count']):
        # Finde den besten Match innerhalb der bereits gruppierten Namen
        best_match = None
        best_ratio = 0
        for grouped_name in grouped_counts:
            ratio = fuzz.ratio(name, grouped_name)
            if ratio > best_ratio and ratio >= threshold:
                best_match = grouped_name
                best_ratio = ratio

        # Wenn ein ähnlicher Name gefunden wurde, füge die Häufigkeit und den Namen als Alternative hinzu
        if best_match:
            grouped_counts[best_match]["Count"] += count
            grouped_counts[best_match]["Alternativen"].append(name)
        else:
            # Falls kein Match gefunden wurde, neuen Eintrag anlegen
            grouped_counts[name] = {"Count": count, "Alternativen": [name]}

    # DataFrame für Ausgabe vorbereiten
    grouped_list = [
        {"Value": key, "Count": value["Count"], "Alternativen": ", ".join(value["Alternativen"])}
        for key, value in grouped_counts.items()
    ]
    return pd.DataFrame(grouped_list)


# Namen gruppieren und DataFrame sortieren
grouped_counts = group_similar_names(value_counts)

# Sortieren der gruppierten Namen nach Häufigkeit in absteigender Reihenfolge
grouped_counts_sorted = grouped_counts.sort_values(by="Count", ascending=False)

# Speichern der ursprünglichen Häufigkeit in einer Datei
with open("zaehlung_allgemein.txt", "w", encoding="utf-8") as file:
    for index, row in value_counts.iterrows():
        file.write(f"{row['Value']}: {row['Count']}\n")

# Speichern der gruppierten und sortierten Häufigkeit ohne Alternativen in einer neuen Datei
with open("zaehlung_gruppiert.txt", "w", encoding="utf-8") as file:
    for index, row in grouped_counts_sorted.iterrows():
        file.write(f"{row['Value']}: {row['Count']}\n")

# Speichern der gruppierten und sortierten Häufigkeit mit Alternativen in einer dritten Datei
with open("zaehlung_gruppiert_inkl_alternativen.txt", "w", encoding="utf-8") as file:
    for index, row in grouped_counts_sorted.iterrows():
        file.write(f"{row['Value']}: {row['Count']} (Alternativen: {row['Alternativen']})\n")

print("Fertig :)")
