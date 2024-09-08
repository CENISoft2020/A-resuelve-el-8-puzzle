import heapq
import numpy as np
import time
import os
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# Heurísticas: Hamming y Manhattan
def hamming(state, goal):
    return np.sum(state != goal) - 1

def manhattan(state, goal):
    dist = 0
    for i in range(1, 9):
        ix, iy = np.where(state == i)
        gx, gy = np.where(goal == i)
        dist += abs(ix - gx) + abs(iy - gy)
    return dist[0]

# Verifica si un estado es la solución
def is_goal(state, goal):
    return np.array_equal(state, goal)

# Encuentra las posiciones vecinas (posibles movimientos)
def neighbors(state):
    neighbor_states = []
    zero_pos = np.where(state == 0)
    x, y = zero_pos[0][0], zero_pos[1][0]
    
    # Posibles movimientos
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            new_state = np.copy(state)
            new_state[x, y], new_state[new_x, new_y] = new_state[new_x, new_y], new_state[x, y]
            neighbor_states.append(new_state)
    
    return neighbor_states

# Algoritmo A* con la opción de elegir entre Hamming y Manhattan
def a_star(initial_state, goal_state, heuristic):
    pq = []
    heapq.heappush(pq, (0, initial_state.tobytes()))
    came_from = {initial_state.tobytes(): None}
    cost_so_far = {initial_state.tobytes(): 0}
    
    while pq:
        _, current = heapq.heappop(pq)
        current = np.frombuffer(current, dtype=initial_state.dtype).reshape(initial_state.shape)
        
        if is_goal(current, goal_state):
            return came_from, cost_so_far
        
        for neighbor in neighbors(current):
            new_cost = cost_so_far[current.tobytes()] + 1
            if neighbor.tobytes() not in cost_so_far or new_cost < cost_so_far[neighbor.tobytes()]:
                cost_so_far[neighbor.tobytes()] = new_cost
                priority = new_cost + heuristic(neighbor, goal_state)
                heapq.heappush(pq, (priority, neighbor.tobytes()))
                came_from[neighbor.tobytes()] = current
            
    return None, None

# Función para reconstruir el camino
def reconstruct_path(came_from, start, goal):
    if came_from is None:
        print("No se encontró una solución para el puzzle.")
        return []

    current = goal
    path = [current]
    while not np.array_equal(current, start):
        current = came_from.get(current.tobytes())
        path.append(current)
    path.reverse()
    return path

# Función para limpiar la consola (simulación de animación en la consola)
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Función para mostrar la cuadrícula en la consola
def display_grid(state):
    for row in state:
        print("+---+---+---+")
        print("| " + " | ".join(f"{num if num != 0 else ' '}" for num in row) + " |")
    print("+---+---+---+")

# Función para animar la solución en la consola
def animate_console_solution(solution, delay=1):
    for state in solution:
        clear_console()
        display_grid(state)
        time.sleep(delay)

# Función para ingresar el estado inicial manualmente
def input_puzzle():
    print("Ingresa 8 números para el puzzle (0 representa el espacio vacío). El espacio restante se rellenará con 0:")
    puzzle = []
    entered_numbers = []
    
    for i in range(3):
        while True:
            row = input(f"Fila {i + 1} (3 números, separados por espacios): ").split()
            if len(row) == 3 and all(num.isdigit() for num in row):
                puzzle.append([int(num) for num in row])
                entered_numbers.extend([int(num) for num in row])
                break
            else:
                print("Error: Debes ingresar exactamente 3 números por fila.")

    # Validar que hay exactamente 8 números
    if len(entered_numbers) == 8:
        puzzle[-1].append(0)  # Añadir el 0 en la posición faltante
    elif len(entered_numbers) != 9:
        raise ValueError("Debe haber exactamente 9 números en el puzzle.")

    return np.array(puzzle)

# Función para crear el árbol del puzzle (en formato binario)
def create_puzzle_tree(path):
    G = nx.DiGraph()

    # Crear nodos
    for i in range(len(path)):
        node_label = f"Estado {i+1}\n{format_state(path[i])}"
        G.add_node(node_label)

    # Agregar aristas para formar un árbol binario
    for i in range(1, len(path)):
        parent_idx = (i - 1) // 2
        parent_label = f"Estado {parent_idx+1}\n{format_state(path[parent_idx])}"
        child_label = f"Estado {i+1}\n{format_state(path[i])}"
        G.add_edge(parent_label, child_label)

    return G

# Función para formatear el estado en una cadena
def format_state(state):
    return "\n".join(" ".join(str(cell) for cell in row) for row in state)

# Función para reorganizar el árbol en un formato binario
def organize_binary_tree(G, pos):
    new_pos = {}
    for node in G.nodes:
        idx = int(node.split()[1]) - 1
        level = (idx + 1).bit_length() - 1
        pos_x = (idx - (1 << level) + 1) * 2 ** (1 - level)
        pos_y = -level
        new_pos[node] = (pos_x, pos_y)
    return new_pos

# Función para graficar el árbol con un layout Spring y mover nodos con el mouse
def plot_tree(G):
    pos = nx.spring_layout(G, seed=42)  # Inicializa el layout
    fig, ax = plt.subplots(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=10, font_weight='bold', arrows=True, ax=ax)
    plt.title("Árbol de Solución del Puzzle")

    # Crear el botón para reorganizar el árbol
    ax_button = plt.axes([0.75, 0.05, 0.2, 0.075])
    button = Button(ax_button, 'Organizar Binario')

    def on_button_click(event):
        new_pos = organize_binary_tree(G, pos)
        ax.clear()
        nx.draw(G, new_pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=10, font_weight='bold', arrows=True, ax=ax)
        plt.title("Árbol de Solución del Puzzle")
        plt.draw()

    button.on_clicked(on_button_click)

    # Funciones para mover los nodos
    def on_click(event):
        if event.inaxes != ax:
            return
        # Verificar si el clic fue en un nodo
        for node, (x, y) in pos.items():
            if abs(event.xdata - x) < 0.05 and abs(event.ydata - y) < 0.05:
                moving_nodes[node] = (event.xdata, event.ydata)
                break

    def on_drag(event):
        if event.inaxes != ax:
            return
        # Actualizar la posición del nodo en movimiento
        if moving_nodes:
            for node in moving_nodes.keys():
                pos[node] = (event.xdata, event.ydata)
            ax.clear()
            nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=10, font_weight='bold', arrows=True, ax=ax)
            plt.title("Árbol de Solución del Puzzle")
            plt.draw()

    def on_release(event):
        moving_nodes.clear()

    moving_nodes = {}
    fig.canvas.mpl_connect('button_press_event', on_click)
    fig.canvas.mpl_connect('motion_notify_event', on_drag)
    fig.canvas.mpl_connect('button_release_event', on_release)
    
    plt.show()

# Función principal para el menú
def main():
    print("Bienvenido al solver de 8-Puzzle con el algoritmo A*")
    initial_state = input_puzzle()

    goal_state = np.array([[1, 2, 3],
                           [4, 5, 6], 
                           [7, 8, 0]])

    print("\nOpciones:")
    print("1. Resolver con la heurística Hamming.")
    print("2. Resolver con la heurística Manhattan.")
    print("3. Resolver con A* y mostrar animación en consola.")
    option = input("Elige una opción (1/2/3): ")

    if option == '1':
        heuristic = hamming
        print("\nResolviendo con Hamming...")
    elif option == '2':
        heuristic = manhattan
        print("\nResolviendo con Manhattan...")
    elif option == '3':
        heuristic_choice = input("Elige la heurística para A* (1 para Hamming, 2 para Manhattan): ")
        heuristic = hamming if heuristic_choice == '1' else manhattan
        print("\nResolviendo con A* y mostrando animación en consola...")
    else:
        print("Opción inválida.")
        return

    # Ejecutar A* y mostrar el resultado
    came_from, cost_so_far = a_star(initial_state, goal_state, heuristic)
    path = reconstruct_path(came_from, initial_state, goal_state)

    if path:
        print("\nSolución encontrada:")
        for state in path:
            print(state)
            print()
        if option == '3':
            animate_console_solution(path)
        
        # Crear el árbol y mostrarlo
        G = create_puzzle_tree(path)
        plot_tree(G)
    else:
        print("\nNo se pudo encontrar una solución para el puzzle dado.")

# Ejecutar el programa principal
if __name__ == "__main__":
    main()
