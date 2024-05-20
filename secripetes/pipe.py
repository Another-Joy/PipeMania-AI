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


class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de PipeMania."""


    def __init__(self, width, height, grid):
        self.width = width
        self.height = height
        self.grid = grid

    def get_value(self, row: int, col: int) -> str:
        try:
            return self.grid[row][col]
        except:
            return None

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        return  (self.get_value(row-1, col), self.get_value(row+1, col))

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return  (self.get_value(row, col-1), self.get_value(row, col+1))

    @staticmethod
    def parse_instance():
        """Lê a instância do problema do standard input (stdin) e retorna uma instância da classe Board."""
        input_lines = sys.stdin.read().strip().split('\n')
        

        
        # As linhas subsequentes contêm o grid
        grid = [list(line.split("\t").strip()) for line in input_lines]
        
        width, height = len(grid[0]), len(grid)
        
        # Cria e retorna uma instância de Board
        return Board(width, height, grid)

    # TODO: outros metodos da classe


class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO
        pass

    def get_value(self,state, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if 0 <= row < state.board.height and 0 <= col < self.width:
            return state.board.grid.get_value(row,col)
        else:
            raise IndexError("Position out of the board boundaries")

    def is_connected(self,state, x1, y1, x2, y2):
        """Verifica se as coordenadas (x1, y1) e (x2, y2) estão conectadas entre si."""
        if not (0 <= x1 < state.board.height and 0 <= y1 < state.board.width and 0 <= x2 < state.board.height and 0 <= y2 < state.board.width):
            return False
        
        piece1 = state.board.grid.get_value(x1, y1)
        piece2 = state.board.grid.get_value(x2, y2)
        
        # Definir as conexões de cada peça (ajustar conforme necessário)
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
            # Adicione outras peças conforme necessário
        }

        # Verificar se a peça está conectada a outra peça adjacente
        if x1 == x2:
            if y1 == y2 + 1:  # (x1, y1) está à direita de (x2, y2)
                return connections[piece1]['left'] and connections[piece2]['right']
            if y1 == y2 - 1:  # (x1, y1) está à esquerda de (x2, y2)
                return connections[piece1]['right'] and connections[piece2]['left']
        elif y1 == y2:
            if x1 == x2 + 1:  # (x1, y1) está abaixo de (x2, y2)
                return connections[piece1]['up'] and connections[piece2]['down']
            if x1 == x2 - 1:  # (x1, y1) está acima de (x2, y2)
                return connections[piece1]['down'] and connections[piece2]['up']
        
        return False

    def count_connections(self, state):
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

    def possible_moves(piece):
        """Retorna uma lista de todas as rotações possiveis da peça e que não inclui o estado atual da peça"""
        #TODO
        pass
        
    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        
        actions = []
        for x in len(state.board):
            for y in len(state.board[x]):
                for move in possible_moves(state.board[x][y]):
                    actions.append((x, y, move))

        return actions

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

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
