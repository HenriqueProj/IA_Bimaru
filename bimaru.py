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

    def __init__(self, board, boards_left):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1
        # boards_left[tamanho do barco] = numero de barcos desse tamanho
            # Ex: boards_left[4] = 1
        self.boards_left = boards_left

    def __lt__(self, other):
        return self.id < other.id

    def remove_c(self):
        board = self.board.board
        hints = self.board.hints

        for hint in hints:
            if hint[2] == 'C':
                self.boards_left[1] -= 1
                self.board.rows[int(hint[0])] -= 1
                self.board.columns[int(hint[1])] -= 1



class Board:
    """Representação interna de um tabuleiro de Bimaru."""

    def __init__(self, board, rows, columns, hints) -> None:
        self.board = board

        # Valores de cells por linhas e colunas (Por no state??)
        self.rows = rows
        self.columns = columns
        self.hints  = hints

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
        
        hints = []

        # Salta o primeiro valor do input (ROW e COLUMN)
        rows = [int(x) for x in stdin.readline().split()[1:]] 
        columns = [int(x) for x in stdin.readline().split()[1:]]

        # Numero de pistas
        hint_num = int(stdin.readline())

        # Hints
        for cont in range(hint_num):
            # Skip no HINT
            hint = stdin.readline().split()[1:]
            hints += [hint,]

            board[int(hint[0]), int(hint[1])] = hint[2]

            #if hint[2] != 'W':
            #    rows[int(hint[0])] -= 1
            #    columns[int(hint[1])] -= 1

        return Board(board, rows, columns, hints)

    def rodeia_agua(self, x, y, char):
        if char == 'T':
            if x > 0:
                if self.board[x - 1, y] == '':
                    self.board[x - 1, y] = '.'

                if y > 0:
                    if self.board[x - 1][y - 1] == '':
                        self.board[x - 1][y - 1] = '.'

                if y < 9:
                    if self.board[x - 1][y + 1] == '':
                        self.board[x - 1][y + 1] = '.'

            if y > 0:
                if self.board[x][y - 1] == '':
                    self.board[x][y - 1] = '.'

                    if x < 9:
                        if self.board[x + 1][y - 1] == '':
                            self.board[x + 1][y - 1] = '.'

            if y < 9:
                if self.board[x][y + 1] == '':
                    self.board[x][y + 1] = '.'

                    if x < 9:
                        if self.board[x + 1][y + 1] == '':
                            self.board[x + 1][y + 1] = '.'

        elif char == 'B':
            if x < 9:
                if self.board[x + 1, y] == '':
                    self.board[x + 1, y] = '.'

                if y > 0:
                    if self.board[x + 1][y - 1] == '':
                        self.board[x + 1][y - 1] = '.'

                if y < 9:
                    if self.board[x + 1][y + 1] == '':
                        self.board[x + 1][y + 1] = '.'

            if y > 0:
                if self.board[x][y - 1] == '':
                    self.board[x][y - 1] = '.'

                    if x > 0:
                        if self.board[x - 1][y - 1] == '':
                            self.board[x - 1][y - 1] = '.'

            if y < 9:
                if self.board[x][y + 1] == '':
                    self.board[x][y + 1] = '.'

                    if x > 0:
                        if self.board[x - 1][y + 1] == '':
                            self.board[x - 1][y + 1] = '.'

        elif char == 'L':
            if x < 9:
                if self.board[x + 1, y] == '':
                    self.board[x + 1, y] = '.'

                if y > 0:
                    if self.board[x + 1][y - 1] == '':
                        self.board[x + 1][y - 1] = '.'

                if y < 9:
                    if self.board[x + 1][y + 1] == '':
                        self.board[x + 1][y + 1] = '.'

            if x > 0:
                if self.board[x - 1, y] == '':
                    self.board[x - 1, y] = '.'

                if y > 0:
                    if self.board[x - 1][y - 1] == '':
                        self.board[x - 1][y - 1] = '.'

                if y < 9:
                    if self.board[x - 1][y + 1] == '':
                        self.board[x - 1][y + 1] = '.'

            if y > 0:
                if self.board[x][y - 1] == '':
                    self.board[x][y - 1] = '.'

        elif char == 'R':
            if x < 9:
                if self.board[x + 1, y] == '':
                    self.board[x + 1, y] = '.'

                if y > 0:
                    if self.board[x + 1][y - 1] == '':
                        self.board[x + 1][y - 1] = '.'

                if y < 9:
                    if self.board[x + 1][y + 1] == '':
                        self.board[x + 1][y + 1] = '.'

            if x > 0:
                if self.board[x - 1, y] == '':
                    self.board[x - 1, y] = '.'

                if y > 0:
                    if self.board[x - 1][y - 1] == '':
                        self.board[x - 1][y - 1] = '.'

                if y < 9:
                    if self.board[x - 1][y + 1] == '':
                        self.board[x - 1][y + 1] = '.'

            if y < 9:
                if self.board[x][y + 1] == '':
                    self.board[x][y + 1] = '.'

        else:   # char == 'C'
            if x < 9:
                if self.board[x + 1, y] == '':
                    self.board[x + 1, y] = '.'

                if y > 0:
                    if self.board[x + 1][y - 1] == '':
                        self.board[x + 1][y - 1] = '.'

                if y < 9:
                    if self.board[x + 1][y + 1] == '':
                        self.board[x + 1][y + 1] = '.'

            if x > 0:
                if self.board[x - 1, y] == '':
                    self.board[x - 1, y] = '.'

                if y > 0:
                    if self.board[x - 1][y - 1] == '':
                        self.board[x - 1][y - 1] = '.'

                if y < 9:
                    if self.board[x - 1][y + 1] == '':
                        self.board[x - 1][y + 1] = '.'

            if y > 0:
                if self.board[x][y - 1] == '':
                    self.board[x][y - 1] = '.'

            if y < 9:
                if self.board[x][y + 1] == '':
                    self.board[x][y + 1] = '.'


    # Preenche as linhas ou colunas de agua, Rodeando os C's de agua
    def fill_water(self):
        for i in range(BOARD_SIZE):
            if self.rows[i] != 0:
                continue
            for j in range(BOARD_SIZE):
                if self.board[i][j] == '':
                    self.board[i][j] = '.'

        for i in range(BOARD_SIZE):
            if self.columns[i] != 0:
                continue
            for j in range(BOARD_SIZE):
                if self.board[j][i] == '':
                    self.board[j][i] = '.'

        for hint in self.hints:
            i = int(hint[0])
            j = int(hint[1])

            if hint[2] == 'C':
                self.rodeia_agua(i, j, 'C')
            
            elif hint[2] == 'B':
                self.rodeia_agua(i, j, 'B')

            elif hint[2] == 'T':
                self.rodeia_agua(i, j, 'T')

            elif hint[2] == 'L':
                self.rodeia_agua(i, j, 'L')

            elif hint[2] == 'R':
                self.rodeia_agua(i, j, 'R')

    # Imprime o tabuleiro no formato indicado
    def print_board(self):
        output = ""

        board = self.board

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == '':
                    output += "_"
                else:
                    output += board[i][j]
            if i != BOARD_SIZE - 1:
                output += "\n"

        print(output)
        
    # Retorna 1 caso o tabuleiro esteja cheio
    def check_full_board(self):
        board = self.board

        for i in range(BOARD_SIZE):
            if self.rows[i] != 0 or self.columns[i] != 0:
                return 0

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == '':
                    return 0

        return 1

    def coloca_barco(self, action):
        
        # Evitar overwrite no original
        board = np.copy(self.board)

        x = action[0][0]
        y = action[0][1]
        # h se horizontal, v se vertical, outro se size = 1
        orientacao = action[1][0]
        size = action[2]


        rows =  np.copy(self.rows)
        columns = np.copy(self.columns)

        pos_inicial = board[x][y]

        # Coloca o barco 

        # Size 1
        if size == 1:
            #if x == 9 and y == 9:
            #    self.print_board()
            board[x][y] = 'c'
            #if x == 9 and y == 9:
            #    print()
            #    Board(board, rows, columns).print_board()


        # Horizontal

        elif orientacao == 'h':
            if board[x][y] == '':
                board[x][y] = 'l'

            for i in range(1, size - 1):
                if board[x][y + i] == '':
                    board[x][y + i] = 'm'

            if board[x][y + size - 1] == '':
                board[x][y + size - 1] = 'r'
        
        # Vertical
        else:
            if board[x][y] == '':
                board[x][y] = 't'

            for i in range(1, size - 1):
                if board[x + i][y] == '':
                    board[x + i][y] = 'm'

            if board[x + size - 1][y] == '':
                board[x + size - 1][y] = 'b'


        # Coloca as aguas

        # Horizontal ou size 1
        if size == 1 or orientacao == 'h':
            for i in range(x - 1, x + 2):
                if i < 0 or i >= 10:
                    continue

                for j in range(y - 1, y + size + 1):
                    if 0 <= j < 10 and board[i][j] == '':
                        board[i][j] = "."
        
        # Vertical
        else:
            for i in range(x - 1, x + size + 1):
                if i < 0 or i >= 10:
                    continue

                for j in range(y - 1, y + 2):
                    if 0 <= j < 10 and board[i][j] == '':
                        board[i][j] = "."

        # Ajusta as linhas e colunas
        if orientacao == 'h':
            rows[x] -= size

            for j in range(y, y + size):
                columns[j] -= 1
        else:
            columns[y] -= size

            for i in range(x, x + size):
                rows[i] -= 1

        return Board(board, rows, columns, self.hints)

    def check_valid_board(self):
        #! Meter as hints no board para nao fazer loop duplo aqui
        board = self.board
        
        for hint in self.hints:
            i = int(hint[0])
            j = int(hint[1])

            if board[i][j] == 'T' and board[i+1][j] in ['c', '.']:
                return 0
            elif board[i][j] == 'B' and board[i-1][j] in ['c', '.']:
                return 0
            elif board[i][j] == 'L' and board[i][j + 1] in ['c', '.']:
                return 0
            elif board[i][j] == 'R' and board[i][j - 1] in ['c', '.']:
                return 0 
                # ^ -> XOR
            elif board[i][j] == 'M' and (i==9 or i==0 or board[i - 1][j] == '.' or board[i + 1][j] == '.'):
                if j == 0 or j == 9 or board[i][j - 1] == '.' or board[i][j + 1] in ['.', 'l']:
                    return 0

        return 1

    # TODO: outros metodos da classe


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        
        initial = BimaruState(board, boards_left=[0,4,3,2,1])
        super().__init__(initial)

        initial.remove_c()
        


    # Acao: [posicao, orientacao (h/v), tamanho do barco]
    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

        #! Pre processamento - Otimizar?
        if state.board.check_full_board() or not state.board.check_valid_board() or (state.boards_left[1] == 0 and state.boards_left[2] == 0):
            return []

        actions = []
        biggest_boat = 0

        boards_left = state.boards_left
        board = state.board.board

        letras_horizontal = ['', 'M', 'R']
        letras_vertical = ['', 'M', 'B']
    
        # Descobrir o maior barco possivel
        for i in range(4):
            if boards_left[4 - i] > 0:
                biggest_boat = 4 - i
                break
        
        # Size 1
        if biggest_boat == 1:
            for i in range(BOARD_SIZE):
                if state.board.rows[i] < biggest_boat:
                    continue
                    
                for j in range(BOARD_SIZE):
                    if state.board.columns[j] >= 1 and board[i][j] == '':
                        actions.append([ [i, j], [''], biggest_boat])

            return actions
        

        # Procura horizontal
        for i in range(BOARD_SIZE):
            if state.board.rows[i] < biggest_boat:
                continue
            
            for j in range(BOARD_SIZE):
                if j != 0 and board[i][j-1] not in ['W', '', '.']:
                    continue
                
                if board[i][j] not in ['L', '']:
                    continue

                for size in range(1, biggest_boat):
                    # 
                    if j + size >= 10 or board[i][j + size] not in letras_horizontal or state.board.columns[j + size] < 1:
                        #
                        #if j == 9 or 1:  
                        break

                    if size == biggest_boat - 1 and board[i][j + size] != 'M' and (j + size + 1 >= 10 or board[i][j + size + 1] in ['W', '', '.']) :
                        actions += [[ [i,j], ['h'], biggest_boat]]
                    
        # Procura vertical
        for j in range(BOARD_SIZE):
            
            if state.board.columns[j] < biggest_boat:
                continue
            
            for i in range(BOARD_SIZE):
                if i != 0 and board[i - 1][j] not in ['W', '', '.']:
                    continue

                if board[i][j] not in ['T', '']:
                    continue

                for size in range(1, biggest_boat):
                    if i + size >= 10 or board[i + size][j] not in letras_vertical or state.board.rows[i + size] < 1:
                        break
                    
                    if size == biggest_boat - 1 and board[i + size][j] != 'M' and (i + size + 1 >= 10 or board[i + size + 1][j] in ['W', '', '.']):
                        actions += [[ [i,j], ['v'], biggest_boat ]]

        return actions


    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        
        new_board = state.board.coloca_barco(action)

        boards_left = np.copy(state.boards_left)
        boards_left[action[2]] -= 1
        
        new_board.fill_water()

        ##print(state.board.rows, state.board.columns)
        #new_board.print_board()

        return BimaruState(new_board, boards_left)


    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        
        return state.board.check_full_board() and state.board.check_valid_board()
    
    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe




if __name__ == "__main__":

    # * Ler o ficheiro do standard input, prepara o tabuleiro
    board = Board.parse_instance()
    board.fill_water()

    # * Inicializa o problem (que cria o primeiro state)
    problem = Bimaru(board)

    # * Usar uma técnica de procura para resolver a instância,
    result_node = depth_first_tree_search(problem)
    
    # * Retirar a solução a partir do nó resultante,
    result = result_node.state.board
    
    # * Imprimir para o standard output no formato indicado.
    result.print_board()
