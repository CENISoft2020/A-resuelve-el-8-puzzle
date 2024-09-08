import heapq
import numpy as np
import time
import os

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
    else:
        print("\nNo se pudo encontrar una solución para el puzzle dado.")

# Ejecutar el programa principal
if __name__ == "__main__":
    main()
