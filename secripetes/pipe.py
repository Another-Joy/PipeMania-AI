# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2
from timeit import default_timer as timer
import sys
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)



nodes = 0

class Board:
    """Representação interna de um tabuleiro de PipeMania."""


    def __init__(self, grid):
        self.grid = grid
        self.width, self.height = len(grid[0]), len(grid)
    def __str__(self):
        s = ""
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])-1):
                s += (self.grid[r][c][0] + "\t")
            s += self.grid[r][-1][0]
            s += "\n"
        return s

    def get_value(self, row: int, col: int) -> str:
        if row <0 or col<0:
            return None
        try:
            return self.grid[row][col][0]
        except:
            return None    
        
    def get_lock(self, row: int, col: int) -> int:
        if row <0 or col<0:
            return True
        try:
            return self.grid[row][col][1]
        except:
            return True

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str): # type: ignore
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        return  (self.get_value(row-1, col)[0], self.get_value(row+1, col)[0])

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str): # type: ignore
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return  (self.get_value(row, col-1)[0], self.get_value(row, col+1)[0])

    @staticmethod
    def parse_instance():
        """Lê a instância do problema do standard input (stdin) e retorna uma instância da classe Board."""
        input_lines = sys.stdin.read().strip().split('\n')
        grid= []
        
        # As linhas subsequentes contêm o grid
        for line in input_lines:
            grid.append(list((val, False) for val in line.strip().split("\t")))

        
        # Cria e retorna uma instância de Board
        return Board(grid)

    # TODO: outros metodos da classe


class PipeManiaState:
    state_id = 0

    def __init__(self, board: Board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas. """
        return self.id < other.id

    # TODO: outros metodos da classe



class PipeMania(Problem):
    def __init__(self, initial_board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = self.preprocess(PipeManiaState(initial_board))
        # TODO
        pass

    def get_value(self,state: PipeManiaState, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if 0 <= row < state.board.height and 0 <= col < state.board.width:
            return state.board.get_value(row,col)
        else:
            raise IndexError("Position out of the board boundaries")

    def connects(self, piece1, piece2, dir):
        
        connections = {
            'FC': {'left': False, 'right': False, 'up': True, 'down': False},
            'FB': {'left': False, 'right': False, 'up': False, 'down': True},
            'FE': {'left': True, 'right': False, 'up': False, 'down': False},
            'FD': {'left': False, 'right': True, 'up': False, 'down': False},
            'LH': {'left': True, 'right': True, 'up': False, 'down': False},
            'LV': {'left': False, 'right': False, 'up': True, 'down': True},
            'BC': {'left': True, 'right': True, 'up': True, 'down': False},
            'BB': {'left': True, 'right': True, 'up': False, 'down': True},
            'BE': {'left': True, 'right': False, 'up': True, 'down': True},
            'BD': {'left': False, 'right': True, 'up': True, 'down': True},
            'VC': {'left': True, 'right': False, 'up': True, 'down': False},
            'VB': {'left': False, 'right': True, 'up': False, 'down': True},
            'VE': {'left': True, 'right': False, 'up': False, 'down': True},
            'VD': {'left': False, 'right': True, 'up': True, 'down': False},
            None: {'left': False, 'right': False, 'up': False, 'down': False},
            'All': {'left': True, 'right': True, 'up': True, 'down': True}
        }

        # Verificar se a peça está conectada a outra peça adjacente
        if dir == 'left':
                return connections[piece1]['left'] and connections[piece2]['right']
        elif dir == 'right':
                return connections[piece1]['right'] and connections[piece2]['left']
        elif dir == 'up':
                return connections[piece1]['up'] and connections[piece2]['down']
        elif dir == 'down':
                return connections[piece1]['down'] and connections[piece2]['up']
        


    def is_connected(self,state: PipeManiaState, x1, y1, x2, y2):
        """Verifica se as coordenadas (x1, y1) e (x2, y2) estão conectadas entre si."""
        if not (0 <= x1 < state.board.height and 0 <= y1 < state.board.width and 0 <= x2 < state.board.height and 0 <= y2 < state.board.width):
            return False
        
        piece1 = state.board.get_value(x1, y1)
        piece2 = state.board.get_value(x2, y2)
        

        # Verificar se a peça está conectada a outra peça adjacente
        if x1 == x2:
            if y1 == y2 + 1:  # (x1, y1) está à direita de (x2, y2)
                return self.connects(piece1, piece2, "left")
            if y1 == y2 - 1:  # (x1, y1) está à esquerda de (x2, y2)
                return self.connects(piece1, piece2, "right")
        elif y1 == y2:
            if x1 == x2 + 1:  # (x1, y1) está abaixo de (x2, y2)
                return self.connects(piece1, piece2, "up")
            if x1 == x2 - 1:  # (x1, y1) está acima de (x2, y2)
                return self.connects(piece1, piece2, "down")
        
        return False


    def max_connections(self, state: PipeManiaState):
        max_con = 0
        for x in range(state.board.height):
            for y in range(state.board.width):
                if state.board.grid[x][y][0][0] == "F": max_con +=1
                elif state.board.grid[x][y][0][0] == "L": max_con +=2
                elif state.board.grid[x][y][0][0] == "V": max_con +=2
                elif state.board.grid[x][y][0][0] == "B": max_con +=3
        return (max_con //2)


    def count_connections(self, state: PipeManiaState):
        """Conta o número total de conexões na grid."""
        total_connections = 0

        for x in range(state.board.height):
            for y in range(state.board.width):
                # Verifica a conexão com a célula à direita
                if y + 1 < state.board.width:
                    if self.is_connected(state, x, y, x, y + 1):
                        total_connections += 1
                # Verifica a conexão com a célula abaixo
                if x + 1 < state.board.height:
                    if self.is_connected(state,x, y, x + 1, y):
                        total_connections += 1

        return total_connections


    def count_groups(self, state: PipeManiaState):
        """Conta o número de grupos de células conectadas na grid."""
        visited = [[False] * state.board.width for _ in range(state.board.height)]
        
        def dfs(x, y):
            """Função auxiliar para realizar DFS e marcar todas as células conectadas."""
            stack = [(x, y)]
            while stack:
                cx, cy = stack.pop()
                if visited[cx][cy]:
                    continue
                visited[cx][cy] = True
                for nx, ny in [(cx-1, cy), (cx+1, cy), (cx, cy-1), (cx, cy+1)]:
                    if 0 <= nx < state.board.height and 0 <= ny < state.board.width and not visited[nx][ny] and self.is_connected(state ,cx, cy, nx, ny):
                        stack.append((nx, ny))
        
        group_count = 0
        for i in range(state.board.height):
            for j in range(state.board.width):
                if not visited[i][j]:
                    dfs(i, j)
                    group_count += 1
        
        return group_count

    def possible_moves(piece):
        
        """Retorna uma lista de todas as rotações possiveis da peça e que não inclui o estado atual da peça"""
        possibles = {"F": ("FC", "FB", "FE", "FD"),
                     "B": ("BC", "BB", "BE", "BD"),
                     "V": ("VC", "VB", "VE", "VD"),
                     "L": ("LH", "LV")}
        result = []
        for i in possibles[piece[0]]:
            if not i == piece:
                result.append(i)
        return result
        
    def evaluate_combinations(self, state: PipeManiaState, row: int, col: int):
        """
        Given a coordinate (row, col), evaluate possible pieces that can be placed
        based on the locked neighbor pieces.
        """
        if state.board.get_lock(row, col):
            return []  # If the current position is locked, no combinations are possible.

        possible_pieces = {
            'F': ['FC', 'FB', 'FE', 'FD'],
            'L': ['LH', 'LV'],
            'V': ['VC', 'VB', 'VE', 'VD'],
            'B': ['BC', 'BB', 'BE', 'BD']
        }

        # Get the locked neighbors and their connections
        neighbors = {
            'left': (row, col - 1),
            'right': (row, col + 1),
            'up': (row - 1, col),
            'down': (row + 1, col)
        }
        
        locked_neighbors = {
            direction: state.board.get_value(*pos) if state.board.get_lock(*pos) else "ignore" for direction, pos in neighbors.items()
        }
        
        # Determine valid pieces based on locked neighbors
        valid_pieces = []

        for piece in possible_pieces[(state.board.get_value(row, col))[0]]:
            valid = True
            for direction, neighbor_piece in locked_neighbors.items():
                if neighbor_piece == "ignore": continue
                elif neighbor_piece:
                    if self.connects(piece, "All", direction) and (not self.connects("All", neighbor_piece, direction)):
                        valid = False
                        break                 
                    elif (not self.connects(piece, "All", direction)) and self.connects("All", neighbor_piece, direction):
                        valid = False
                        break   
                else:
                    if self.connects(piece, "All", direction):
                        valid = False
                        break
            if valid:
                valid_pieces.append(piece)
        return valid_pieces


    def locks(self, state:PipeManiaState):
        sures = []
        for x in range(len(state.board.grid)):
            for y in range(len(state.board.grid[x])):
                if not state.board.grid[x][y][1]:
                    combs = self.evaluate_combinations(state, x, y)
                    if len(combs) == 1:
                        sures.append((x, y, combs[0]))
        return sures
    
    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        
        
        actions = []
        for x in range(len(state.board.grid)):
            for y in range(len(state.board.grid[x])):
                if not state.board.grid[x][y][1]:
                    combs = self.evaluate_combinations(state, x, y)
                    if len(combs) == 1:
                        return [(x, y, combs[0])]
                    # Only add moves that increase connectivity or are near locked pieces
                    if any(state.board.get_lock(nx, ny) for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]):
                        actions.extend((x, y, comb) for comb in combs)
        return actions



    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # Manually copy the current board grid
        new_grid = [[(cell[0], cell[1]) for cell in row] for row in state.board.grid]
        
        # Apply the action to the copied grid
        x, y, new_piece = action
        new_grid[x][y] = (new_piece, True)  # Set the new piece and lock it
        
        # Create a new Board and PipeManiaState with the modified grid
        new_board = Board(new_grid)
        return PipeManiaState(new_board)
        


    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        global nodes
        nodes += 1
        if self.count_groups(state) == 1:
            return True
        return False


    def fixes_border(self, state: PipeManiaState):
        """Try to lock the border pieces if they can only be in one position."""

        # Define border coordinates
        border_coordinates = []
        for col in range(state.board.width):
            border_coordinates.append((0, col))  # Top row
            border_coordinates.append((state.board.height - 1, col))  # Bottom row
        for row in range(1, state.board.height - 1):
            border_coordinates.append((row, 0))  # Left column
            border_coordinates.append((row, state.board.width - 1))  # Right column

        
        reuse = []
        # Try to lock each border piece
        for row, col in border_coordinates:
            if state.board.get_lock(row, col) == 0:  # If not already locked
                possible_pieces = self.evaluate_combinations(state, row, col)
                if len(possible_pieces) == 1:
                    state.board.grid[row][col] = (possible_pieces[0], True)  # Lock the piece
                else: reuse.append((row, col))
            

        
        rereuse = []
        for row, col in reuse:
            if state.board.get_lock(row, col) == 0:  # If not already locked
                possible_pieces = self.evaluate_combinations(state, row, col)
                if len(possible_pieces) == 1:
                    state.board.grid[row][col] = (possible_pieces[0], True)  # Lock the piece
                else: rereuse.append((row, col))
        
        reuse = []
        for row, col in reversed(rereuse):            
            if state.board.get_lock(row, col) == 0:  # If not already locked
                possible_pieces = self.evaluate_combinations(state, row, col)
                if len(possible_pieces) == 1:
                    state.board.grid[row][col] = (possible_pieces[0], True)  # Lock the piece

        return state

    def preprocess(self, state: PipeManiaState):
        state = self.fixes_border(state)
        
        todo = self.locks(state)
        while len(todo) > 0:
            for i in todo:
                state.board.grid[i[0]][i[1]] = (i[2], True)
            todo = self.locks(state)
            
            
        return state
            
        

    def h(self, node):
        state = node.state
        max_con = self.max_connections(state)
        total_con = self.count_connections(state)
        group_penalty = self.count_groups(state) - 1
        return (max_con - total_con) + group_penalty * 10
    

    # TODO: outros metodos da classe

if __name__ == "__main__":
    
    with open('in', 'r') as sys.stdin: 
        
        start = timer()


        board = Board.parse_instance()
        print(board)
        problem = PipeMania(board)
        if problem.goal_test(problem.initial):
            print(problem.initial.board, end="")
            print(f"{(timer() - start)*1000} miliseconds")
            exit()
        node = depth_first_tree_search(problem)
        print(node.state.board, end="")
        print(nodes)
        print(f"{(timer() - start)*1000} miliseconds")
    
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
