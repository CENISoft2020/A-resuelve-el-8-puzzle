import heapq
import numpy as np

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
    if zero_pos[0].size == 0 or zero_pos[1].size == 0:
        raise ValueError("No se encontró el espacio vacío (0) en el estado actual.")
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
        if current is None:
            print("Error: El camino no se pudo reconstruir completamente.")
            return []
        path.append(current)
    path.reverse()
    return path

# Función para ingresar el estado inicial manualmente
def input_puzzle():
    print("Ingresa 8 números para el puzzle (0 representa el espacio vacío). El espacio restante se rellenará con 0:")
    puzzle = []
    entered_numbers = []
    for i in range(3):
        while True:
            row = input(f"Fila {i + 1} (max 3 números, separados por espacios): ").split()
            if len(row) <= 3 and all(num.isdigit() for num in row):
                puzzle.append([int(num) for num in row])
                entered_numbers.extend(puzzle[-1])
                break
            else:
                print("Por favor, ingresa un máximo de 3 números por fila, separados por espacios.")
    
    # Verifica que solo se hayan ingresado 8 números
    if len(entered_numbers) != 8:
        raise ValueError("Debes ingresar exactamente 8 números.")
    
    # Añade el 0 automáticamente en la posición restante
    flat_puzzle = sum(puzzle, [])
    if len(flat_puzzle) < 9:
        flat_puzzle.append(0)
    
    return np.array(flat_puzzle).reshape((3, 3))

# Configuración del puzzle inicial y el objetivo
initial_state = input_puzzle()

goal_state = np.array([[1, 2, 3], 
                       [4, 5, 6], 
                       [7, 8, 0]])

# Selección de la heurística
heuristic_choice = input("Elige la heurística: 1 para Hamming, 2 para Manhattan: ")
if heuristic_choice == '1':
    heuristic = hamming
else:
    heuristic = manhattan

# Ejecutar A* y mostrar el resultado
came_from, cost_so_far = a_star(initial_state, goal_state, heuristic)
path = reconstruct_path(came_from, initial_state, goal_state)

# Mostrar cada movimiento
if path:
    print("Solución encontrada:")
    for state in path:
        print(state)
        print()
else:
    print("No se pudo encontrar una solución para el puzzle dado.")
