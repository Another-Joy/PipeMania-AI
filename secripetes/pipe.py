# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

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



class Board:
    """Representação interna de um tabuleiro de PipeMania."""


    def __init__(self, width, height, grid):
        self.width = width
        self.height = height
        self.grid = grid

    def get_value(self, row: int, col: int) -> str:
        try:
            return self.grid[row][col][0]
        except:
            return None    
        
    def get_lock(self, row: int, col: int) -> int:
        try:
            return self.grid[row][col][1]
        except:
            return 1

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
        #sys.stdin.read().strip().split('\n')
        input_lines = "VB\tVC\nVE\tVD\n".strip().split('\n')
        grid= []
        
        # As linhas subsequentes contêm o grid
        for line in input_lines:
            grid.append(list((val, 0) for val in line.strip().split("\t")))
        
        print(grid)
        width, height = len(grid[0]), len(grid)
        
        # Cria e retorna uma instância de Board
        return Board(width, height, grid)

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
        self.initial_state = PipeManiaState(initial_board)
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
                return self.connects(self, piece1, piece2, "left")
            if y1 == y2 - 1:  # (x1, y1) está à esquerda de (x2, y2)
                return self.connects(self, piece1, piece2, "right")
        elif y1 == y2:
            if x1 == x2 + 1:  # (x1, y1) está abaixo de (x2, y2)
                return self.connects(self, piece1, piece2, "up")
            if x1 == x2 - 1:  # (x1, y1) está acima de (x2, y2)
                return self.connects(self, piece1, piece2, "down")
        
        return False


    def max_connections(self, state: PipeManiaState):
        max_con = 0
        for x in range(state.board.height):
            for y in range(state.board.width):
                if state.board.grid[x][y][0] == "F": max_con +=1
                elif state.board.grid[x][y][0] == "L": max_con +=2
                elif state.board.grid[x][y][0] == "V": max_con +=2
                elif state.board.grid[x][y][0] == "B": max_con +=3
        return max_con


    def count_connections(self, state: PipeManiaState):
        """Conta o número total de conexões na grid."""
        total_connections = 0

        for x in range(state.board.height):
            for y in range(state.board.width):
                # Verifica a conexão com a célula à direita
                if y + 1 < state.board.width:
                    if self.is_connected(self, x, y, x, y + 1):
                        total_connections += 1
                # Verifica a conexão com a célula abaixo
                if x + 1 < state.board.height:
                    if self.is_connected(self, x, y, x + 1, y):
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
            direction: state.board.get_value(*pos) if state.board.get_lock(*pos) else None for direction, pos in neighbors.items()
        }

        # Determine valid pieces based on locked neighbors
        valid_pieces = []

        for piece_type, pieces in possible_pieces.items():
            for piece in pieces:
                valid = True
                for direction, neighbor_piece in locked_neighbors.items():
                    if neighbor_piece:
                        if not self.connects(piece, neighbor_piece, direction):
                            valid = False
                            break
                    else:
                        if self.connects(piece, "All", direction):
                            valid = False
                            break
                if valid:
                    valid_pieces.append(piece)

        return valid_pieces


    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        
        
        
        
        actions = []
        for x in len(state.board.grid):
            for y in len(state.board.grid[x]):
                if not state.board.grid[x][y][1]:
                    combs = self.evaluate_combinations(state, x, y)
                    if len(combs) == 1:
                        return [combs,]
                    actions.extend(combs)
        return actions



    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        board = state.board.grid
        for x in len(board):
            for y in len(board[x]):
                if board[x][y][1] == 2:
                    board[x][y] = (board[x][y][0], 0)
        
        board[action[0]][action[1]] = (action[2], 2)
        return PipeManiaState(Board(board))
        
        
    def points(self, state:PipeManiaState):
        pass


    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        if self.count_connections(state) == self.max_connections(state) and self.count_groups(state) == 0:
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

        # Try to lock each border piece
        for row, col in border_coordinates:
            if state.board.get_lock(row, col) == 0:  # If not already locked
                possible_pieces = self.evaluate_combinations(state, row, col)
                if len(possible_pieces) == 1:
                    state.board.grid[row][col] = (possible_pieces[0], 1)  # Lock the piece

        return state



    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe



if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
