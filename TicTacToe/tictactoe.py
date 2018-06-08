from random import shuffle
import os

# Definicao de variaveis do algoritmo
ConjuntoDeTreinamento = 1000
kernelExponent = 2              # Kernel exponent to pass to Weka's algorithm
kernelParam = 25007             # Kernel parameter to pass to Weka's algorithm


class TicTacToe():

    # inicializa a classe com:
    #   - a variavel para mostrar o tabuleiro no console
    #   - o tamanho do dataset de jogos a ser criado, caso nenhum valor seja passado, valor padrao eh 1000.
    def __init__(self, setSize=1000):
        self.prtBoard = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.dataSetSize = setSize

    # 1. rotina para checar o vencedor da partida, se houver.
    # 2. Cada laco do if eh para checar cada chance que existe para se vencer um jogo da velha
    #   - 2 diagonais, 3 linhas e 3 colunas = 8 chances
    def check_if_I_win(self, auxBoard, player):
        if(auxBoard[0] == player and auxBoard[1] == player and auxBoard[2] == player):
            return True
        elif (auxBoard[3] == player and auxBoard[4] == player and auxBoard[5] == player):
            return True
        elif (auxBoard[6] == player and auxBoard[7] == player and auxBoard[8] == player):
            return True
        elif (auxBoard[0] == player and auxBoard[3] == player and auxBoard[6] == player):
            return True
        elif (auxBoard[0] == player and auxBoard[4] == player and auxBoard[8] == player):
            return True
        elif (auxBoard[2] == player and auxBoard[4] == player and auxBoard[6] == player):
            return True
        elif (auxBoard[1] == player and auxBoard[4] == player and auxBoard[7] == player):
            return True
        elif (auxBoard[2] == player and auxBoard[5] == player and auxBoard[8] == player):
            return True
        else:
            return False

    # 1. rotina para checar o vencedor da partida, se houver
    # 2. Identica a rotina anterior em termos de logica. Porem, retorna a posicao que o jogador esta prestes a vencer
    # 3. Exemplo: Eh a vez de X:
    #   X|X|2
    #   O|4|5
    #   6|O|8
    #       - A rotina abaixo retornara o indice 2
    def check_if_I_CAN_win(self, auxBoard, player):

        if (auxBoard[2] == player and auxBoard[1] == player and auxBoard[0] == 'b') or (auxBoard[8] == player and auxBoard[4] == player and auxBoard[0] == 'b') or (auxBoard[6] == player and auxBoard[3] == player and auxBoard[0] == 'b'):
            return 0
        elif (auxBoard[0] == player and auxBoard[2] == player and auxBoard[1] == 'b') or (auxBoard[7] == player and auxBoard[4] == player and auxBoard[1] == 'b'):
            return 1
        elif (auxBoard[0] == player and auxBoard[1] == player and auxBoard[2] == 'b') or (auxBoard[4] == player and auxBoard[6] == player and auxBoard[2] == 'b') or (auxBoard[5] == player and auxBoard[8] == player and auxBoard[2] == 'b'):
            return 2
        elif (auxBoard[5] == player and auxBoard[4] == player and auxBoard[3] == 'b') or (auxBoard[6] == player and auxBoard[0] == player and auxBoard[3] == 'b'):
            return 3
        elif (auxBoard[5] == player and auxBoard[3] == player and auxBoard[4] == 'b') or (auxBoard[1] == player and auxBoard[7] == player and auxBoard[4] == 'b') or (auxBoard[8] == player and auxBoard[0] == player and auxBoard[4] == 'b') or (auxBoard[2] == player and auxBoard[6] == player and auxBoard[4] == 'b'):
            return 4
        elif (auxBoard[3] == player and auxBoard[4] == player and auxBoard[5] == 'b') or (auxBoard[2] == player and auxBoard[8] == player and auxBoard[5] == 'b'):
            return 5
        elif (auxBoard[0] == player and auxBoard[3] == player and auxBoard[6] == 'b') or (auxBoard[8] == player and auxBoard[7] == player and auxBoard[6] == 'b') or (auxBoard[2] == player and auxBoard[4] == player and auxBoard[6] == 'b'):
            return 6
        elif (auxBoard[8] == player and auxBoard[6] == player and auxBoard[7] == 'b') or (auxBoard[1] == player and auxBoard[4] == player and auxBoard[7] == 'b'):
            return 7
        elif (auxBoard[6] == player and auxBoard[7] == player and auxBoard[8] == 'b') or (auxBoard[2] == player and auxBoard[5] == player and auxBoard[8] == 'b') or (auxBoard[0] == player and auxBoard[4] == player and auxBoard[8] == 'b'):
            return 8
        else:
            return -1

    # realiza uma partida automatica dada uma sequencia aleatoria de tamanho 9,
    # que descreve, em sequencia, as posicoes jogadas de cada jogador.
    #
    # A notacao escolhida do tabuleiro foi a de um vetor, cada indice do vetor
    # corresponde a uma casa do tabuleiro
    #
    #   _|_|_      0|1|2
    #   _|_|_  =>  3|4|5
    #    | |       6|7|8
    #
    # Exemplo: Tabuleiro = (0, 1, 2, 3, 4, 5, 6, 7, 8);
    #          Partida = (0, 3, 7, 2, 1, 6, 4, 5, 8)
    #       -1: o jogador 'X' jogou na posicao: 0
    #       -2: o jogador 'O' jogou na posicao: 3
    #       -3: o jogador 'X' jogou na posicao: 7
    #       -4: o jogador 'O' jogou na posicao: 2
    #       -5: o jogador 'X' jogou na posicao: 1
    #       -6: o jogador 'O' jogou na posicao: 6
    #       -7: o jogador 'X' jogou na posicao: 4 X venceu
    #       -8: o jogador 'O' jogaria na posicao: 5
    #       -9: o jogador 'X' jogaria na posicao: 8
    #   Resultaria numa partida como:
    #   -   X|X|O
    #   -   O|X|_   =>  X venceu na jogada numero 7  (posicao do tabuleiro = 4)
    #   -   O|X|_
    def make_a_game(self, auxBoard):
        gameIdx = [x for x in range(9)]
        shuffle(gameIdx)
        for i in range(0, 9):
            if i % 2 == 0:
                if self.check_if_I_CAN_win(auxBoard, 'X') == -1:
                    auxBoard[gameIdx[i]] = 'X'
                    Pos = gameIdx[i]
                    if self.check_if_I_win(auxBoard, 'X'):
                        return auxBoard, 'X', Pos
                else:
                    Pos = self.check_if_I_CAN_win(auxBoard, 'X')
                    auxBoard[Pos] = 'X'
                    return auxBoard, 'X', Pos
            else:
                auxBoard[gameIdx[i]] = 'O'
                Pos = gameIdx[i]
                if self.check_if_I_win(auxBoard, 'O'):
                    return auxBoard, 'O', Pos
        return auxBoard, 'empate', -1

    # Escreve o resultado de 1000 partidas em que o jogador X vence, no formato padrao e requisitado pela atividade
    def write_the_data(self):

        count = 0
        dataList = list()
        while count < self.dataSetSize:
            auxBoard, player, position = self.make_a_game(auxBoard=['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'])
            if player == 'X':
                auxBoard[position] = 'b'
                # escrevendo os resultados somente de X:
                data = ''
                while len(auxBoard) > 0:
                    data = data + '\'' + auxBoard.pop(0) + '\''
                    if len(auxBoard) > 0:
                        data = data + ','
                data = data + ',' + '\'' + str(position) + '\''
                dataList.append(data)
                count += 1
        self.prepare_file('TicTacToe.arff')
        f = open('TicTacToe.arff', 'a')
        for i in dataList:
            f.write(i + '\n')
        f.close()

    # Prepara um arquivo com template padrao do weka
    def prepare_file(self, fileName):
        header = list()
        header.append('@relation TicTacToe')
        for i in range(0, 9):
            header.append('@attribute idx' + str(i) + ' {\'X\',\'O\',\'b\'}')
        header.append('@attribute \'Class\' {\'0\',\'1\',\'2\',\'3\',\'4\',\'5\',\'6\',\'7\',\'8\'}')
        header.append('@data')

        f = open(fileName, 'w')
        for i in header:
            f.write(i + '\n')
        f.close()

    # 1. Rotina responsavel por treinar o classificador com um conjunto de treinamento criado por write_the_data
    # 2. Retorna uma string preparada para ser chamada via console
    # 3. Adicional: Salva o classificador em um arquivo chamado "saida.model"
    def import_classifier(self, ConjuntoDeDados, kernelParam, kernelExponent=2):
        base1 = 'java -classpath weka.jar weka.classifiers.functions.SMO -C 5.0 -L 0.001 -P 1.0E-12 -N 0 -V -1 -W 1'
        base2 = ' -K "weka.classifiers.functions.supportVector.PolyKernel -C ' + str(kernelParam) + ' -E ' + str(kernelExponent) + '"'
        base3 = ' -t ' + ConjuntoDeDados
        base4 = ' -d saida.model'
        stringWeka = base1 + base2 + base3 + base4
        return stringWeka

    # 1. Rotina responsavel por testar o classificador com um conjunto de testes
    # 2. Retorna uma string preparada para ser chamada via console
    def test_classifier(self, ConjuntoDeDados, modelo):
        base1 = 'java -classpath weka.jar weka.classifiers.functions.SMO -l ' + modelo
        base2 = ' -T ' + str(ConjuntoDeDados) + ' -p 0'
        stringModel = base1 + base2
        return stringModel

    # mostra os dados no console na forma de um tabuleiro
    def data2board(self, board):
        auxBoard = list(board)
        for i in range(0, 3):
            for j in range(0, 3):
                self.prtBoard[i][j] = auxBoard.pop(0)
        for i in range(0, 3):
            print('\t\t\t   ' + str(self.prtBoard[i]))

    # mostra as posicoes restantes a serem jogadas na forma de tabuleiro
    def remainingPos2board(self, board):
        print("\t\t\t   ["),
        for i in range(0, 9):
            if(board[i] == "b"):
                print(i),
            else:
                print(board[i]),
            if((i + 1) % 3 == 0):
                print("]")
                if(i != 8):
                    print("\t\t\t   ["),

    # 1. Rotina responsavel por montar o arquivo que sera usado para teste, nesse caso no jogo em si
    # 2. Retorna um arquivo no padrao weka com somente uma amostra (no caso, o jogo atual)
    def prepare_a_move(self, auxBoard):
        self.prepare_file('moveChoosed.arff')
        line = str()
        for i in range(0, len(auxBoard)):
            line = line + '\'' + auxBoard[i] + '\'' + ','
        line = line + '\'' + '0' + '\''
        f = open('moveChoosed.arff', 'a')
        f.write(line)
        f.close()

    # Atraves do arquivo gerado apos testar a amostra do jogo, essa rotina eh responsavel por extrair a posicao
    # (classe) que o classificador escolheu
    def move_chosen(self, fileName):
        dados = list()
        f = open(fileName, 'r')
        for line in f:
            dados.append(line)
        f.close()
        line = dados[5].split()
        classifierDecision = line[2]
        return classifierDecision[2]

    # Retorna a precisao que o classificador obteve com os dados de treinamento inicializados
    def classifier_precision(self, fileName):
        correctLine = list()
        with open(fileName) as f:
            for line in f:
                if "Correctly Classified Instances" in line:
                    correctLine.append(line)

        percentage = correctLine[1].split()
        return percentage[4]

    # funcao principal que roda o jogo
    def run(self, kernelParam, kernelExponent):
        board = ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', ]
        validPos = [x for x in range(9)]
        shuffle(validPos)
        ConjuntoDeDados = "TicTacToe.arff"
        modelo = "saida.model"
        testList = "moveChoosed.arff"
        percentage = "log.txt"

        self.write_the_data()
        os.system(self.import_classifier(ConjuntoDeDados, kernelParam, kernelExponent) + ' > log.txt')
        print('========================================================================')
        print('                  Tic-Tac-Toe Using the SVM Algorithm')
        print('========================================================================')
        print('========================================================================')
        print('                                0|1|2')
        print('                                3|4|5')
        print('                                6|7|8')
        print('========================================================================')
        print('CPU precision = ' + str(self.classifier_precision(percentage)) + '%' + '                            X => CPU && O => player')
        print('========================================================================')
        print('........................................................................')
        while True:
            print('CPU`s turn:')
            print('-------------------------------------------------------------------------')
            self.prepare_a_move(board)
            os.system(self.test_classifier(testList, modelo) + ' > output.txt')
            CPUMove = self.move_chosen('output.txt')
            xPos = int(CPUMove)
            if board[xPos] != 'b':
                validMoves = len(validPos)
                if validMoves == 0:
                    print('     DRAW')
                    self.data2board(board)
                    break
                board[validPos[0]] = 'X'
                validPos.pop(0)
                if self.check_if_I_win(board, 'X'):
                    print('     CPU Wins! Better luck next time')
                    self.data2board(board)
                    break
            else:
                board[xPos] = 'X'
                validPos.remove(xPos)
                if self.check_if_I_win(board, 'X'):
                    print('     CPU Wins! Better luck next time')
                    self.data2board(board)
                    break
            self.data2board(board)
            print('-------------------------------------------------------------------------')
            if len(validPos) == 0:
                    print('     DRAW')
                    self.data2board(board)
                    break
            print('Your turn (choose a valid position): ')
            remainingPos = list(validPos)
            print('Valid positions:')
            self.remainingPos2board(board)
            playerMove = raw_input('Your play:\n')
            while playerMove not in str(remainingPos):
                playerMove = raw_input('Please, insert a valid input to the game.\n')
            print('-------------------------------------------------------------------------')
            oPos = int(playerMove)
            if board[oPos] != 'b':
                validMoves = len(validPos)
                if validMoves == 0:
                    print('     DRAW')
                    self.data2board(board)
                    break
                board[validPos[0]] = 'O'
                validPos.pop(0)
                if self.check_if_I_win(board, 'O'):
                    print('     YOU WIN, CONGRATULATIONS!')
                    self.data2board(board)
                    break
            else:
                board[oPos] = 'O'
                validPos.remove(oPos)
                if self.check_if_I_win(board, 'O'):
                    print('     YOU WIN, CONGRATULATIONS!')
                    self.data2board(board)
                    break
            self.data2board(board)
            print('-------------------------------------------------------------------------')


teste = TicTacToe(ConjuntoDeTreinamento)
print('Loading... Please Wait')
teste.run(kernelParam, kernelExponent)
