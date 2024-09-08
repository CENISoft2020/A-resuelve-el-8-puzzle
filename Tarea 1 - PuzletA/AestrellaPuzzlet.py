import heapq
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Representación del tablero 8-Puzzle
class Puzzle:
    def __init__(self, board, parent=None, move="", depth=0, cost=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = cost
        self.blank_pos = self.find_blank()

    def find_blank(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return (i, j)

    def possible_moves(self):
        x, y = self.blank_pos
        moves = []
        if x > 0:
            moves.append((x-1, y, "up"))
        if x < 2:
            moves.append((x+1, y, "down"))
        if y > 0:
            moves.append((x, y-1, "left"))
        if y < 2:
            moves.append((x, y+1, "right"))
        return moves

    def apply_move(self, move):
        x, y = self.blank_pos
        new_board = [row[:] for row in self.board]
        nx, ny, direction = move
        new_board[x][y], new_board[nx][ny] = new_board[nx][ny], new_board[x][y]
        return Puzzle(new_board, parent=self, move=direction, depth=self.depth + 1)

    def is_goal(self, goal):
        return self.board == goal

    def __lt__(self, other):
        return self.cost < other.cost

# Heurística: Distancia Manhattan
def manhattan_distance(board, goal):
    distance = 0
    for i in range(9):  # La lista ya es unidimensional con 9 elementos
        if board[i] != 0:  # Ignorar el espacio vacío
            x, y = divmod(i, 3)  # Coordenadas actuales en la matriz 3x3
            goal_x, goal_y = divmod(goal.index(board[i]), 3)  # Coordenadas objetivo
            distance += abs(x - goal_x) + abs(y - goal_y)
    return distance

# Algoritmo A* para resolver el 8-Puzzle
def a_star(initial_board, goal_board):
    goal = sum(goal_board, [])
    start_puzzle = Puzzle(initial_board)
    start_puzzle.cost = manhattan_distance(sum(initial_board, []), goal)
    
    open_list = []
    heapq.heappush(open_list, start_puzzle)
    visited = set()

    while open_list:
        current_puzzle = heapq.heappop(open_list)
        visited.add(tuple(map(tuple, current_puzzle.board)))

        if current_puzzle.is_goal(goal_board):
            return current_puzzle

        for move in current_puzzle.possible_moves():
            new_puzzle = current_puzzle.apply_move(move)
            new_board_tuple = tuple(map(tuple, new_puzzle.board))

            if new_board_tuple not in visited:
                new_puzzle.cost = new_puzzle.depth + manhattan_distance(sum(new_puzzle.board, []), goal)
                heapq.heappush(open_list, new_puzzle)

    return None

# Función para reconstruir el camino de solución
def reconstruct_path(puzzle):
    path = []
    while puzzle:
        path.append(puzzle.board)
        puzzle = puzzle.parent
    return path[::-1]

# Función de animación
def animate_solution(solution):
    fig, ax = plt.subplots()
    ax.set_axis_off()
    puzzle_images = []

    for state in solution:
        img = ax.imshow(np.array(state), animated=True)
        puzzle_images.append([img])

    ani = animation.ArtistAnimation(fig, puzzle_images, interval=1000, repeat_delay=1000)
    plt.show()

# Estado inicial y objetivo
initial_board = [[1, 2, 3],
                 [4, 0, 5],
                 [6, 7, 8]]

goal_board = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]

# Resolver el puzzle
solution_puzzle = a_star(initial_board, goal_board)

# Si se encuentra una solución, animar el proceso
if solution_puzzle:
    solution_path = reconstruct_path(solution_puzzle)
    animate_solution(solution_path)
else:
    print("No se encontró solución.")
