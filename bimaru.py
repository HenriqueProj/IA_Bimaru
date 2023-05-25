# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import sys
from sys import stdin
import numpy as np

from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

# Comprimento do tabuleiro
BOARD_SIZE = 10


class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

        # boards_left[tamanho do barco] = numero de barcos desse tamanho
            # Ex: boards_left[4] = 1
        self.boards_left = [0, 4, 3, 2, 1]

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Bimaru."""

    def __init__(self, board, rows, columns) -> None:
        self.board = board

        # Valores de cells por linhas e colunas (Por no state??)
        self.rows = rows
        self.columns = columns

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""

        return board[row][col]


    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        board = self.board

        if row == 0 or row == BOARD_SIZE - 1:
            return 
        return (board[row - 1][col], board[row + 1][col])
    

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        board = self.board

        if col == 0 or col == BOARD_SIZE - 1:
            return 
        return (board[row][col - 1], board[row][col + 1])

    @staticmethod
    def parse_instance():

        board = np.empty((BOARD_SIZE, BOARD_SIZE), dtype=str)
                         
        # Salta o primeiro valor do input (ROW e COLUMN)
        rows = [int(x) for x in stdin.readline().split()[1:]] 
        columns = [int(x) for x in stdin.readline().split()[1:]]

        # Numero de pistas
        hint_num = int(stdin.readline())

        # Hints
        for cont in range(hint_num):
            # Skip no HINT
            hint = stdin.readline().split()[1:]

            board[int(hint[0]), int(hint[1])] = hint[2]

        return Board(board, rows, columns)

    # Preenche as linhas ou colunas de agua
    def fill_water(self):
        for i in range(BOARD_SIZE):
            if self.rows[i] != 0:
                continue
            for j in range(BOARD_SIZE):
                self.board[i][j] = '.'

        for i in range(BOARD_SIZE):
            if self.columns[i] != 0:
                continue
            for j in range(BOARD_SIZE):
                self.board[j][i] = '.'

    # Imprime o tabuleiro no formato indicado
    def print_board(self):
        output = ""

        board = self.board

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == '':
                    output += "_ "
                else:
                    output += board[i][j] + " "

            output += "\n"

        print(output)
        
    # Retorna 1 caso o tabuleiro esteja cheio
    def check_full_board(self):
        board = self.board

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == '':
                    return 0
        return 1

    def coloca_barco(self, action):
        
        # Evitar overwrite no original
        board = self.board

        x = action[0][0]
        y = action[0][1]
        # h se horizontal, v se vertical, outro se size = 1
        orientacao = action[1]
        size = action[2]


        # Coloca o barco 

        # Size 1
        if size == 1:
            board[x][y] = 'm'

        # Horizontal
        elif orientacao == 'h':
            board[x][y] = 'l'

            for i in range(1, size - 1):
                board[x][y + i] = 'm'

            board[x][y + size - 1] = 'r'
        
        # Vertical
        else:
            board[x][y] = 't'

            for i in range(1, size - 1):
                board[x + i][y] = 'm'

            board[x + size - 1][y] = 'b'


        # Coloca as aguas

        # Horizontal ou size 1
        if size == 1 or orientacao == 'h':
            for i in range(x - 1, x + 2):
                if i < 0 or i >= 10:
                    continue

                for j in range(y - 1, y + size + 1):
                    if 0 <= j < 10 and board[i][j] == '.':
                        board[i][j] = "w"
        
        # Vertical
        else:
            for i in range(x - 1, x + size + 1):
                if i < 0 or i >= 10:
                    continue

                for j in range(y - 1, y + 2):
                    if 0 <= j < 10 and board[i][j] == '.':
                        board[i][j] = "w"

        return Board(board, self.rows, self.columns)
    
    # TODO: outros metodos da classe


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        
        initial = BimaruState(board)
        super().__init__(initial)

    # Acao: [posicao, orientacao (h/v), tamanho do barco]
    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        
        if state.board.check_full_board():
            return []

        return []


    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        
        new_board = board.coloca_barco()

        return BimaruState(new_board)

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        
        return state.board.check_full_board()
    
    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe




if __name__ == "__main__":

    # Ler o ficheiro do standard input, prepara o tabuleiro
    board = Board.parse_instance()
    board.fill_water()

    # Inicializa o problem (que cria o primeiro state)
    problem = Bimaru(board)

    # Debug
    board.print_board()
    board.coloca_barco([[5,0], 'h', 5]).print_board()

    # Usar uma técnica de procura para resolver a instância,
        #result_node = depth_first_tree_search(problem)

    # Retirar a solução a partir do nó resultante,
        #result = result_node.state.board

    # Imprimir para o standard output no formato indicado.
        #result.print_board() # RETIRAR OS ESPAÇOS NA ENTREGA
