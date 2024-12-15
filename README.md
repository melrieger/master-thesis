# Vom Papier zum Pixel: Digitale Analyse von Amtsversammlungsprotokollen des 18. Jahrhunderts
Die Masterarbeit beschäftigt sich mit der Frage, wie digitale Methoden zur Erschließung und Analyse historischer Quellen eingesetzt werden können. Als Untersuchungsgegenstand werden dabei die Amtsversammlungsprotokolle aus Neuffen aus den Jahren 1734 bis 1746 herangezogen. Im Fokus stehen die Nutzung von Handwritten Text Recognition (HTR) und Durchführung einer Netzwerkanalyse, um neue Erkenntnisse über die soziale und administrative Struktur einer Amtsstadt im 18. Jahrhunderts zu gewinnen. Für die Erschließung der Daten wird die Plattform Transkribus zur automatisierten Transkription genutzt, während die Visualisierung der Daten mit Gephi erfolgt. Ziel ist es, aufzuzeigen, wie digitale Werkzeuge traditionelle historiographische Methoden unterstützen und erweitern können. Die Arbeit macht dabei nicht nur die Potenziale, sondern auch die Grenzen solcher Ansätze deutlich und bietet Anknüpfungspunkte für interdisziplinäre Forschung im Bereich der Digital Humanities.

## Struktur des Repositories:

Die Original-Scans der Amtsversammlungsprotokolle sind im Ordner "Amtsversammlungsprotokolle_Neuffen_Bd1" abgelegt.

Die Transkriptionen wurden in verschiedenen Datei-Formaten aus Transkribus exportiert und sind im Ordner "Transkription" abgelegt.

Alle Dateien, die aus der Netzwerkanalyse mit Gephi entstanden sind, inkl. Knoten/Kanten etc. sind im Ordner "Netzwerkanalyse" abgelegt und in die Unterkategorien "Netzwerkanalyse_Personen" und -"_Orte" eingeteilt. Auch verschiedene Visualisierungen der Netzwerke, sowie die Visualisierungen und Ergebnisse der Metrik-Berechnungen durch Gephi sind dort enthalten.

Die für die Vor- und Nachbereitung der Netzwerkanalyse erstellten Python-Skripte finden sich im Ordner "Python_Skripte". Für das Einlesen der Transkriptionen/Annotationen muss der Pfad vor Ausführung des Skripts angepasst werden.

Alle Abbildungen, die in der Thesis aufgeführt werden, sind im Ordner "Abbildungen_in_Thesis" hinterlegt.

Im Ordner "Sonstige_Dateien" ist die umfangreiche Excel-Datei abgelegt, die Basis für Knoten/Kanten der Netzwerkanalyse war, sowie die Exportierten Daten der DARIAHGeobrowser-Visualisierung.
