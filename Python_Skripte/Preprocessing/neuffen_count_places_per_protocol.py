import pandas as pd
import re

'''
Band_1.xlsx ist der Export der gesetzen Tags in Transkribus.
Die Tabelle besteht aus den Tabs "Overview", "ort", "person", "berufsbezeichnung", "amt", und "ereignis".
Schlussendlich wurden für diese Untersuchung nur die Tabs "ort" und "person" verwendet.
Mit diesem Script sollten die Daten für eine Kante der Netzwerkanalyse der Amtsversammlungsprotokolle von Neuffen 
gefiltert werden. Schlussendlich konnte die Filterung nicht in eine Kante umgewandelt werden, da sie zu 
unzuverlässige Ergebnisse liefert. Dies ist vor allem auf die deutlich voneinander abweichenden 
Schreibweisen zurückzuführen, aber auch auf Probleme beim Tagging mit Transkribus und den daraus entstandenen Daten.
Es wurde daher entschieden, keine auf prozentuale Werte basierende Kante in die Netzwerkanalyse einzubauen,
sondern ausschließlich "faktische" Zählungen aufzunehmen.
'''

# Pfade zu den Dateien
daten_datei = "Band_1.xlsx"  # Hauptdaten, generiert mit Transkribus
alternative_namen_datei = "grouped_with_alternatives_orte.txt"  # Datei mit alternativen Schreibweisen

# Gesamtzahl der Seiten im Dokument
gesamt_seiten = 240

# Liste der Orte, die in der Analyse berücksichtigt werden sollen
orte_liste = [
    "Hohen Neufen", "Vestung", "Neuffen", "Beuren", "Frickenhausen", "Grabenstetten", "Großbettlingen", "Linsenhofen",
    "Weyler", "Erkenbrechtsweiler", "Balzholz", "Kleinbettlingen", "Tischardt", "Urach", "Schorndorf", "Ettlingen",
    "Philippsburg", "Stuttgart", "Nürtingen", "Mömpelgard", "Grafenberg", "Münsingen", "Asperg", "Kohlberg",
    "Schwarzwald", "Freudenstadt", "Cannstatt", "Owen", "Kirchheim", "Bietigheim", "Ludwigsburg",
    "Pfullingen", "Neuenbürg", "Göppingen", "Neuler", "Neidling", "Köngen", "Denkendorf", "Seeburg", "Weiltingen",
    "Wolfschlugen", "Dettingen", "Ebersbach", "Metzingen", "Böblingen", "Herrenberg", "Waldenbuch",
    "Blaubeuren", "Adelberg", "Waiblingen", "Winnenden", "Kappishäusern", "Kabishäusern", "Schlotheim", "Templin",
    "Schwäbisch Gmünd", "Grafeneck", "Eglingen", "Schlierbach", "Kornwestheim", "Esslingen", "Nagold", "Tuttlingen",
    "Maulbronn", "Dornstetten", "Sindelfingen", "Gomadingen", "Upfingen", "Salzburg", "Heidenheim",
    "Ulm", "Freiburg", "Donauwörth", "Reichenbach"
]

# Funktion, um die alternativen Ortsnamen aus einer Textdatei zu laden
def lade_alternativen_namen(dateipfad):
    alternativen_dict = {}
    with open(dateipfad, "r", encoding="utf-8") as datei:
        for zeile in datei:
            treffer = re.match(r"(\w+): \(Alternativen: (.+)\)", zeile)
            if treffer:
                standard_name = treffer.group(1)
                alternativen = treffer.group(2).split(", ")
                # Alternative Schreibweisen sowie den Standardnamen in das Dictionary eintragen
                for name in alternativen:
                    alternativen_dict[name.strip()] = standard_name
                alternativen_dict[standard_name] = standard_name
    return alternativen_dict

# Laden der alternativen Schreibweisen
alternativen_dict = lade_alternativen_namen(alternative_namen_datei)

# Überprüfen, dass alle Orte in der Liste auch im Dictionary enthalten sind
for ort in orte_liste:
    if ort not in alternativen_dict.values():
        alternativen_dict[ort] = ort

# Excel-Datei mit den Ortsnamen und den dazugehörigen Seiten laden
df = pd.read_excel(daten_datei, sheet_name="ort")

# **Erster Schritt**: Filtern nach alternativen Schreibweisen
# Die Ortsnamen im Datensatz auf die Standardnamen mappen
df['Standardname_alt'] = df['Value'].map(alternativen_dict)
df_filtered_alt = df.dropna(subset=['Standardname_alt'])

# Zählen, wie oft die Orte mit alternativen Schreibweisen in den Seiten vorkommen
orte_haeufigkeit_alt = df_filtered_alt.groupby('Standardname_alt')['Page'].nunique()

# Umwandeln in ein DataFrame und den Prozentsatz berechnen
orte_df_alt = orte_haeufigkeit_alt.reset_index()
orte_df_alt.columns = ['Ortsname', 'Anzahl Seiten mit Nennung']
orte_df_alt['Prozent der Seiten'] = (orte_df_alt['Anzahl Seiten mit Nennung'] / gesamt_seiten) * 100

# **Zweiter Schritt**: Filtern nach der Ziel-Orte-Liste
df['Standardname_target'] = df['Value'].apply(lambda x: x if x in orte_liste else None)
df_filtered_target = df.dropna(subset=['Standardname_target'])

# Zählen, wie oft die Orte aus der Ziel-Liste in den Seiten vorkommen
orte_haeufigkeit_target = df_filtered_target.groupby('Standardname_target')['Page'].nunique()

# Umwandeln in ein DataFrame und den Prozentsatz berechnen
orte_df_target = orte_haeufigkeit_target.reset_index()
orte_df_target.columns = ['Ortsname', 'Anzahl Seiten mit Nennung']
orte_df_target['Prozent der Seiten'] = (orte_df_target['Anzahl Seiten mit Nennung'] / gesamt_seiten) * 100

# Sortieren nach Häufigkeit der Nennungen
orte_df_alt = orte_df_alt.sort_values(by='Anzahl Seiten mit Nennung', ascending=False)
orte_df_target = orte_df_target.sort_values(by='Anzahl Seiten mit Nennung', ascending=False)

# Ergebnisse in einer Excel-Datei mit zwei Sheets speichern
with pd.ExcelWriter("ort_protokollanalyse_mit_zwei_filterungen.xlsx") as writer:
    orte_df_alt.to_excel(writer, sheet_name="Filterung_Alternative_Namen", index=False)
    orte_df_target.to_excel(writer, sheet_name="Filterung_Zielliste", index=False)     # leider nicht hilfreich

print("Fertig :)")

