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
            return self.grid[row][col]
        except:
            return None

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str): # type: ignore
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        return  (self.get_value(row-1, col), self.get_value(row+1, col))

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str): # type: ignore
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


class PipeManiaState:
    state_id = 0

    def __init__(self, board: Board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe



class PipeMania(Problem):
    def __init__(self, initial_board: Board):
        """O construtor especifica o estado inicial."""
        self.initial_state = PipeManiaState(initial_board)
        # TODO
        pass


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
        
    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        
        actions = []
        for x in len(state.board.grid):
            for y in len(state.board.grid[x]):
                for move in self.possible_moves(state.board.grid[x][y]):
                    actions.append((x, y, move))

        return actions


    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        if action in self.actions(state):
            board = state.board.grid
            board[action[0]][action[1]] = action[2]
            return PipeManiaState(Board(board))
        else:
            raise "Action not in possible listS"


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
