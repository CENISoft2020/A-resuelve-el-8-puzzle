import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def create_puzzle_tree(path):
    # Crear un gráfico dirigido para representar el árbol
    G = nx.DiGraph()

    # Añadir nodos y aristas al gráfico
    for i in range(len(path)):
        node_label = f"Estado {i+1}\n{format_state(path[i])}"
        G.add_node(node_label)
        if i > 0:
            prev_node_label = f"Estado {i}\n{format_state(path[i-1])}"
            G.add_edge(prev_node_label, node_label)

    return G

def format_state(state):
    return "\n".join(" ".join(str(cell) for cell in row) for row in state)

def plot_tree(G):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(12, 8))

    # Dibujar nodos, aristas y etiquetas
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=10, font_weight='bold', arrows=True)
    plt.title("Árbol de Solución del Puzzle")
    plt.show()

# Simulación de una ruta de solución (ejemplo de estados)
example_path = [
    np.array([[1, 2, 3], [4, 0, 5], [6, 7, 8]]),
    np.array([[1, 2, 3], [4, 7, 5], [6, 0, 8]]),
    np.array([[1, 2, 3], [4, 7, 5], [6, 8, 0]]),
    np.array([[1, 2, 3], [4, 7, 0], [6, 8, 5]]),
    np.array([[1, 2, 3], [4, 0, 7], [6, 8, 5]]),
    np.array([[1, 2, 3], [0, 4, 7], [6, 8, 5]]),
    np.array([[1, 0, 3], [4, 2, 7], [6, 8, 5]])
]

# Crear y mostrar el árbol
G = create_puzzle_tree(example_path)
plot_tree(G)
