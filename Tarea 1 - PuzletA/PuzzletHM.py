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
            break
        
        for neighbor in neighbors(current):
            new_cost = cost_so_far[current.tobytes()] + 1
            if neighbor.tobytes() not in cost_so_far or new_cost < cost_so_far[neighbor.tobytes()]:
                cost_so_far[neighbor.tobytes()] = new_cost
                priority = new_cost + heuristic(neighbor, goal_state)
                heapq.heappush(pq, (priority, neighbor.tobytes()))
                came_from[neighbor.tobytes()] = current
                
    return came_from, cost_so_far

# Función para reconstruir el camino
def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]
    while not np.array_equal(current, start):
        current = came_from[current.tobytes()]
        path.append(current)
    path.reverse()
    return path

# Configuración del puzzle inicial y el objetivo
initial_state = np.array([[1, 2, 3], 
                          [4, 0, 5], 
                          [6, 7, 8]])

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
print("Solución encontrada:")
for state in path:
    print(state)
    print()
