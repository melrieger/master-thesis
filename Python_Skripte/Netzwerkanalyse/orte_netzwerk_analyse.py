import os
import sys
import networkx as nx
import matplotlib.pyplot as plt


# Einlesen der GraphML-Datei
def load_graph(file_name):
    try:
        # Erstelle den Pfad relativ zum Skript
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, file_name)
        print(file_path)

        # Lade den Graphen
        graph = nx.read_graphml(file_path)
        print("Graph erfolgreich geladen!")
        return graph
    except Exception as e:
        print(f"Fehler beim Laden der Datei: {e}")
        sys.exit(1)


# Berechnung Metriken
def calculate_metrics(graph):
    if graph is None:
        print("Kein Graph vorhanden, Abbruch.")
        return

    print("\n--- Netzwerkanalyse ---")
    print(f"Anzahl der Knoten: {graph.number_of_nodes()}")
    print(f"Anzahl der Kanten: {graph.number_of_edges()}")

    # Erwartungsprüfung: Ist das Netzwerk stark verbunden?
    if nx.is_connected(graph):
        print("Das Netzwerk ist verbunden.")
    else:
        print("Das Netzwerk ist NICHT verbunden.")
        num_components = nx.number_connected_components(graph)
        print(f"Anzahl der verbundenen Komponenten: {num_components}")

    # Durchschnittlicher Grad
    avg_degree = sum(dict(graph.degree()).values()) / graph.number_of_nodes()
    print(f"Durchschnittlicher Grad: {avg_degree:.2f}")

    # Gradverteilung
    degree_distribution = [d for _, d in graph.degree()]
    print(f"Höchster Grad: {max(degree_distribution)}")

    # Komponentenanalyse (falls nicht verbunden)
    if not nx.is_connected(graph):
        largest_cc = max(nx.connected_components(graph), key=len)
        largest_subgraph = graph.subgraph(largest_cc)
        print(f"Größe der größten Komponente: {len(largest_cc)} Knoten")
    else:
        largest_subgraph = graph

    # Durchmesser und mittlere kürzeste Pfadlänge - Umwandlung in einfachen Graphen
    simple_graph_for_diameter = nx.Graph(largest_subgraph)  # Erstelle einfachen Graphen für Durchmesser
    try:
        diameter = nx.diameter(simple_graph_for_diameter)
        avg_shortest_path = nx.average_shortest_path_length(simple_graph_for_diameter)
        print(f"Durchmesser: {diameter}")
        print(f"Mittlere kürzeste Pfadlänge: {avg_shortest_path:.2f}")
    except Exception as e:
        print(f"Fehler bei der Berechnung von Durchmesser oder Pfadlänge: {e}")

    # Zentralitätsmetriken
    print("\n--- Zentralitätsmetriken ---")
    degree_centrality = nx.degree_centrality(graph)
    print(f"Höchster Grad-Zentralitätswert: {max(degree_centrality.values()):.2f}")
    betweenness_centrality = nx.betweenness_centrality(graph)
    print(f"Höchster Betweenness-Zentralitätswert: {max(betweenness_centrality.values()):.2f}")

    # Eigenvektor-Zentralität - Umwandlung in einfachen Graphen
    simple_graph_for_eigenvector = nx.Graph(graph)  # Erstelle einfachen Graphen für Eigenvektor-Zentralität
    eigenvector_centrality = nx.eigenvector_centrality(simple_graph_for_eigenvector, max_iter=1000)
    print(f"Höchster Eigenvektor-Zentralitätswert: {max(eigenvector_centrality.values()):.2f}")

    # Knoten mit außergewöhnlich hohen Werten ausgeben
    print("\n--- Knoten mit besonders hohen Metriken ---")

    # Knoten mit höchstem Grad
    max_degree_node = max(graph.degree(), key=lambda x: x[1])
    print(f"Knoten mit höchstem Grad: {max_degree_node[0]} (Grad: {max_degree_node[1]})")

    # Knoten mit höchster Grad-Zentralität
    max_degree_centrality_node = max(degree_centrality.items(), key=lambda x: x[1])
    print(f"Knoten mit höchster Grad-Zentralität: {max_degree_centrality_node[0]} (Zentralität: {max_degree_centrality_node[1]:.2f})")

    # Knoten mit höchster Betweenness-Zentralität
    max_betweenness_centrality_node = max(betweenness_centrality.items(), key=lambda x: x[1])
    print(f"Knoten mit höchster Betweenness-Zentralität: {max_betweenness_centrality_node[0]} (Zentralität: {max_betweenness_centrality_node[1]:.2f})")

    # Knoten mit höchster Eigenvektor-Zentralität
    max_eigenvector_centrality_node = max(eigenvector_centrality.items(), key=lambda x: x[1])
    print(f"Knoten mit höchster Eigenvektor-Zentralität: {max_eigenvector_centrality_node[0]} (Zentralität: {max_eigenvector_centrality_node[1]:.2f})")

    # Rückgabe der Daten für die Visualisierung
    return degree_distribution, degree_centrality, betweenness_centrality, eigenvector_centrality


# Grafische Darstellung der Ergebnisse, Visualisierungen werden gespeichert
def plot_metrics(degree_distribution, degree_centrality, betweenness_centrality, eigenvector_centrality, graph):

    # Ordner für die gespeicherten Visualisierungen erstellen
    output_dir = os.path.join(os.path.dirname(__file__), "visualisierungen_orte")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 1. Visualisierung der Gradverteilung
    plt.figure(figsize=(10, 5))
    plt.hist(degree_distribution, bins=range(1, max(degree_distribution) + 2), color='skyblue', edgecolor='black')
    plt.title("Gradverteilung")
    plt.xlabel("Grad (Anzahl der Verbindungen)")
    plt.ylabel("Anzahl der Knoten")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(os.path.join(output_dir, "gradverteilung.png"))  # Speichern der Grafik
    plt.close()

    # 2. Visualisierung der Grad-Zentralität
    plt.figure(figsize=(10, 5))
    plt.bar(degree_centrality.keys(), degree_centrality.values(), color='lightgreen')
    plt.xticks(color='w')
    plt.title("Grad-Zentralität der Knoten")
    plt.xlabel("Knoten")
    plt.ylabel("Grad-Zentralität")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(os.path.join(output_dir, "grad_zentralitaet.png"))  # Speichern der Grafik
    plt.close()

    # 3. Visualisierung der Betweenness-Zentralität
    plt.figure(figsize=(10, 5))
    plt.bar(betweenness_centrality.keys(), betweenness_centrality.values(), color='salmon')
    plt.xticks(color='w')
    plt.title("Betweenness-Zentralität der Knoten")
    plt.xlabel("Knoten")
    plt.ylabel("Betweenness-Zentralität")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(os.path.join(output_dir, "betweenness_zentralitaet.png"))  # Speichern der Grafik
    plt.close()

    # 4. Visualisierung der Eigenvektor-Zentralität
    plt.figure(figsize=(10, 5))
    plt.bar(eigenvector_centrality.keys(), eigenvector_centrality.values(), color='lightcoral')
    plt.xticks(color='w')
    plt.title("Eigenvektor-Zentralität der Knoten")
    plt.xlabel("Knoten")
    plt.ylabel("Eigenvektor-Zentralität")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(os.path.join(output_dir, "eigenvektor_zentralitaet.png"))  # Speichern der Grafik
    plt.close()

    # 5. Visualisierung des Netzwerks mit hervorgehobenen Knoten
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(graph)  # Positionsbestimmung der Knoten
    node_colors = ['lightblue' if degree_centrality[node] < max(degree_centrality.values()) * 0.75 else 'red' for node in graph.nodes()]
    nx.draw(graph, pos, with_labels=True, node_color=node_colors, node_size=500, font_size=10, font_weight='bold', edge_color='gray')
    plt.title("Visualisierung des Netzwerks mit hervorgehobenen zentralen Knoten (Grad-Zentralität)")
    plt.savefig(os.path.join(output_dir, "netzwerk_hervorgehobene_knoten.png"))
    plt.close()


# Hauptfunktion
def main():
    """Hauptfunktion des Skripts."""
    file_name = "Orte.graphml"
    graph = load_graph(file_name)

    # Metriken berechnen
    degree_distribution, degree_centrality, betweenness_centrality, eigenvector_centrality = calculate_metrics(graph)

    # Ergebnisse visualisieren und speichern
    if graph is not None:
        plot_metrics(degree_distribution, degree_centrality, betweenness_centrality, eigenvector_centrality, graph)


if __name__ == "__main__":
    main()
