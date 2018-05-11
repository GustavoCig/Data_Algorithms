# Nomes: Gustavo Cignachi e Yuri Witney
# Matriculas: 371813 e 371879


import os                              #Utilizado para fazer as chamadas ao Weka
import shutil                          #Utilizado para apagar a pasta criada para armazenar os .txt resultantes do Weka
from random import choice, uniform     #Utilizados para escolha de elementos dentro de uma lista, utilizado para escolha de floats aleatorios dentro de um range
from collections import OrderedDict    #Utilizado para garantir a ordem de insercao dentro de um dicionario





############################ Constantes do algoritmo #################################


minNoRange = range(2, 50)                # Range de valores para o parametro 'minNo'
optRange = range(2, 50)                  # Range de valores para o parametro 'optimizations'
checkErrorRateRange = [True, False]      # Dupla de valores para o parametro 'checkErrorRate'
usePruningRange = [True, False]          # Dupla de valores para o parametro 'usePruningRange'


######################################################################################







######################### Variaveis de controle do algoritmo #########################


ConjuntoDeDados = "data/diabetes.arff"  # Conjunto de dados utilizado no Weka
# Codigo foi elaborado levando em consideracao que o diretorio 'data' e o arquivo 'Weka.jar' encontrao se no mesmo diretorio desde codigo fonte

numFolds = 10                           # Quantidade de dobras a serem repassadas como parametro para o Weka
numCalls = 5                            # Quantidade de seeds atribuidos e utilizados por cada individuo
popSize = 20                            # Tamanho da populacao inicial gerada
tourneyParticipants = 2                 # Quantidade de elementos que participam de cada round da selecao por torneio
roundsTourney = 3                       # Quantidade de rounds da selecao por torneio
epochs = 3                              # Quantidade de eras do algoritmo genetico
qntMutation = 1                         # Quantidade de individuos que passarao por mutacao
numMutations = 1                        # Quantidade de atributos de um individuo que sofreram mutacao(por tanto, so pode variar entre 1 e 4)
percentMutation = 0.01                  # Valor de controle da chance de ocorrer uma mutacao

DEBUG = False                           # Variavel controla a exibicao de certos valores durante a execucao do codigo, a fim de facilitar a visualizacao do funcionamento


######################################################################################















################################# Metodos e classes ##################################


# Definicao da classe "Individual" que descreve cada individuo da populacao com seus parametros e metodos
# Alem de possuir os parametros definidos na atividade, possui tambem os parametros 'id', 'seeds', 'strings' e 'mediaAcerto'
# 'id' eh um atributo de controle unico a cada individuo, sendo incrementado cada vez que eh criado um novo individuo
# 'seeds' eh um atributo apenas utilizado para armazenar as seeds associadas com a instancia especifica do individuo
# 'strings' opera de modo analogo a 'seeds', armazenando as strings a serem utilizadas no Weka associadas com a instancia especifica do individuo
# 'mediaAcerto' eh um atributo utilizado para armazenar a media de acertos do individuo em questao apos calculo utilizando os resultados gerados por cada seed/string do individuo
class Individual:


    idIndiv = 1

    def __init__(self, minNo = -1, optimizations = -1, checkErrorRate = -1, usePruning = -1):
        global idIndiv
        global numCalls

        self.id = Individual.idIndiv
        self.minNo = minNo
        self.optimizations = optimizations
        self.checkErrorRate = checkErrorRate
        self.usePruning = usePruning
        self.seeds = range(self.id, self.id + numCalls)
        self.strings = []
        self.mediaAcerto = -1

        Individual.idIndiv += numCalls


    # Override do metodo 'print' especifico para a classe 'Individual'
    def __repr__(self):
        lines = []
        lines.append("-------Individual-------")
        lines.append("ID: " + str(self.id))
        lines.append("minNo: " + str(self.minNo))
        lines.append("optimizations: " + str(self.optimizations))
        lines.append("checkErrorRate: " + str(self.checkErrorRate))
        lines.append("usePruning: " + str(self.usePruning))
        lines.append("Seeds: "),
        for seed in self.seeds:
            lines.append(str(seed) + " "),
        lines.append("")
        lines.append("Strings: ")
        for string in self.strings:
            lines.append(string + " ")
        lines.append("Media Acertos: " + str(self.mediaAcerto))
        lines.append("")
        result = "\n".join(lines)
        return result


    # Esvazia o atributo 'strings' do individuo em questao
    def cleanStrings(self):
        self.strings[:] = []


    # Metodo utilizado como um 'wrapper' para setar valores passando uma string que especifica para qual parametro eh aquela atribuicao
    def selectSetAttribute(self, method, value):
        if method == 'minNo':
            self.MinNo = value
        if method == 'optimizations':
            self.pptimizations = value
        if method == 'checkErrorRate':
            self.checkErrorRate = value
        if method == 'usePruning':
            self.usePruning = value


    # Metodo para repartir genes do individuo durante etapa de crossover
    def sliceAttributes(self, index):
        breakPoints = {
            1: [['minNo'], ['optimizations', 'checkErrorRate', 'usePruning']],
            2: [['minNo', 'optimizations'], ['checkErrorRate', 'usePruning']],
            3: [['minNo', 'optimizations', 'checkErrorRate'], ['usePruning']]
        }
        return breakPoints[index]





######################################################################################















############################### Metodos de Utilidades ################################


# Metodo utilizado para limpeza de determinados atributos iterando sobre uma populacao
def resetPopulationStats(population):
    for individual in population:
        individual.cleanStrings()


# Metodo utilizado para printar uma populacao, iterando sobre a mesma
def printPopulation(population):
    for individual in population:
        print(individual)


# Procura e retorna um individuo com base no ID passado como parametro dentro de uma populacao
# Caso nao seja encontrado retorna 'None'
def getIndividualByID(population, idIndividual):
    for individual in population:
        if individual.id == idIndividual:
            return individual
    return None


# Basicamente metodo 'getIndividualByID' iterado dentro de uma lista de IDs
def getMultipleIndividuals(population, winnersID):
    foundIndividuals = []
    for winner in winnersID:
        foundIndividuals.append(getIndividualByID(population, winner))
    return foundIndividuals


# Metodo para limpeza dos arquivos de saida(apaga o diretorio criado)
def cleanFiles(popSize, numCalls):
    shutil.rmtree('saidas/', ignore_errors=True)


# Metodo para encontrar e retornar individuo com maior media de acertos da populacao
def findHighestMedia(population):
    maxValue = 0
    bestIndividual = None
    for individual in population:
        if individual.mediaAcerto >= maxValue:
            maxValue = individual.mediaAcerto
            bestIndividual = individual
    return bestIndividual


######################################################################################















####################### Metodos para Manipulacao da Populacao ########################


# Inicializa uma lista de individuos, representativa da populacao inicial
def initPopulation(populationSize, minNoRange, optRange, checkErrorRateRange, usePruningRange):
    population = []
    for i in range(populationSize):
        indiv = Individual()
        changeParams(indiv, minNoRange, optRange, checkErrorRateRange, usePruningRange)
        population.append(indiv)
    return population


# Utilizado para gerar aleatoriamente todos os parametros de um individuo em questao
def changeParams(individual, minNoRange, optRange, checkErrorRateRange, usePruningRange):
    individual.minNo = choice(minNoRange)
    individual.optimizations = choice(optRange)
    individual.checkErrorRate = choice(checkErrorRateRange)
    individual.usePruning = choice(usePruningRange)


######################################################################################















########################## Metodos para Manipulacao do Weka ##########################


# Gera uma string a ser utilizada no Weka com base nos atributos de um individuo juntamente do conjunto de dados a ser utilizado, alem de uma seed especifica
# Metodo cria o diretorio 'saidas', caso diretorio ainda nao exista, sendo todas as strings geradas levando em consideracao esse diretorio
def stringWeka(individual, ConjuntoDeDados, seed, numFolds = 10):
    base1 = "java -classpath weka.jar weka.classifiers.rules.JRip -F " + str(numFolds) + " -N " + str(individual.minNo)
    base2 = " -O " + str(individual.optimizations)
    base3 = " -S " + str(seed)
    base4 = " -E " if individual.checkErrorRate is False else ""
    base5 = " -P " if individual.usePruning is False else ""
    base6 = " -t " + ConjuntoDeDados
    if not os.path.exists("saidas/"):
        os.makedirs("saidas/")
    base7 = " -p 0 > " + "saidas/id_" + str(individual.id) + "_saida_seed_" + str(seed) + ".txt"

    stringWeka = base1 + base2 + base3 + base4 + base5 + base6 + base7
    return stringWeka


# Itera pela populacao a fim de gerar as strings para cada individuo utilizando o metodo 'stringWeka'
def stringWekaPopulation(population, ConjuntoDeDados, numFolds = 10):
    for individual in population:
        for seed in individual.seeds:
            individual.strings.append(stringWeka(individual, ConjuntoDeDados, seed, numFolds))
    return population


# Metodo apenas para encapsular a chamada ao sistema utilizando o modulo 'os'
def callWeka(stringWeka):
    os.system(stringWeka)


# Itera pela populacao e pelas strings de cada individuo para fazer as respectivas chamadas ao Weka
def callWekaPopulation(population):
    for individual in population:
        for string in individual.strings:
            callWeka(string)


# Varre um arquivo de texto a fim de contar a quantidade de erros existentes
# Se baseia no padrao dos txts de saida resultantes do Weka
def readErrors(output):
    errors = 0
    for line in output:
        for ch in line:
            if ch == '+':
                errors += 1
    return errors


# Varre o arquivo arff atrelado ao conjunto de dados em questao a fim de contar a quantidade de entradas contidas nele
def countCases(ConjuntoDeDados):
    dataset = open(ConjuntoDeDados, "r")
    numLines = 0
    for line in dataset:
        if len(line) <= 1:
            continue
        else:
            if (line[0] != '%') and (line[0] != '@'):
                numLines += 1
    return numLines


# Calcula a media de acertos para um arquivo de saida
def calcMediaErrorsSingleFile(output, numLines):
    errors = readErrors(output)
    ratio = errors / float(numLines)
    mediaSingle = 1 - ratio
    return mediaSingle


# Le todos os arquivos de cada individuo da populacao e calcula e atribui as medias de acertos para cada individuo
def readOutputFiles(population, ConjuntoDeDados, numCalls):
    numLines = countCases(ConjuntoDeDados)
    for individual in population:
        count = 0
        for seed in individual.seeds:
            output = open("saidas/id_" + str(individual.id) + '_saida_seed_' + str(seed) + '.txt', 'r')
            count += calcMediaErrorsSingleFile(output, numLines)
        mediaAcertos = count / numCalls
        individual.mediaAcerto = mediaAcertos
    return population


######################################################################################















################################# Metodos da Selecao #################################


# Metodo que realiza a selecao por torneio, selecionando os vencedores para o crossover
# Metodo ira buscar individuos em cada 'tourneyRound' em um loop, so saindo apos conseguir encontrar 'tourneyParticipants' individuos distintos
# Metodo nao garante que um mesmo individuo nao possa participar de mais de um torneio, conforme aconselhamento em sala de aula
def tourney(population, tourneyParticipants, roundsTourney):
    winnersID = []
    for tourneyRound in range(roundsTourney):
        selected = []
        countElem = 0
        while countElem < tourneyParticipants:
            chosen = choice(population)
            if getIndividualByID(selected, chosen.id) is None:
                selected.append(chosen)
                countElem += 1
        maxMedia = 0
        chosenIndiv = None
        for individual in selected:
            if individual.mediaAcerto > maxMedia:
                maxMedia = individual.mediaAcerto
                chosenIndiv = individual
        winnersID.append(chosenIndiv.id)
    return winnersID


######################################################################################















################################ Metodos do CrossOver ################################


# Metodo para a geracao de pares de individuos com base nos membros da populacao selecionados na etapa de selecao
# Pares sao criados atraves de todas as combinacoes possiveis entre membros, exceto combinacoes de um elemento com ele mesmo, alem de combinacoes repetidas
def combineWinners(population, winnersID):
    selected = getMultipleIndividuals(population, winnersID)
    combinations = []
    pair = []
    for indexOut in range(len(selected)):
        for indexIn in range(indexOut):
            pair = []
            if selected[indexOut] == selected[indexIn]:
                continue
            pair.append(selected[indexIn])
            pair.append(selected[indexOut])
            combinations.append(pair)
    return combinations


# Metodo que realiza a geracao de dois filhos para cada par de pais, sendo quebrado os genes dos pais em um ponto especifico e recombinado para formacao do genes dos filhos
def reproduce(population, father, mother):
    breakPoint = choice(range(1, 4))

    fatherLeftGenes = father.sliceAttributes(breakPoint)[0]
    fatherRightGenes = father.sliceAttributes(breakPoint)[1]
    motherLeftGenes = mother.sliceAttributes(breakPoint)[0]
    motherRightGenes = mother.sliceAttributes(breakPoint)[1]


    if DEBUG:
        print("-----------Separacao dos genes------------")
        print(fatherLeftGenes)
        print(fatherRightGenes)
        print(motherLeftGenes)
        print(motherRightGenes)
        print("------------------------------------------")


    son = Individual()
    daughter = Individual()


    if DEBUG:
        print("--------------Filhos gerados--------------")
        print(son)
        print(daughter)
        print("------------------------------------------")


    for gene in fatherLeftGenes:
        son.selectSetAttribute(gene, getattr(father, gene))
    for gene in motherRightGenes:
        son.selectSetAttribute(gene, getattr(mother, gene))

    for gene in fatherRightGenes:
        daughter.selectSetAttribute(gene, getattr(father, gene))
    for gene in motherLeftGenes:
        daughter.selectSetAttribute(gene, getattr(mother, gene))

    population.append(son)
    population.append(daughter)
    return population



# Aplicacao do crossover simples, sendo primeiro gerados os pares pai e mae, sendo repassados para a geracao dos filhos
def crossover(population, winnersID):
    combinationSet = combineWinners(population, winnersID)
    for pair in combinationSet:
        population = reproduce(population, pair[0], pair[1])
    return population


######################################################################################















################################# Metodos da Mutacao #################################


# Cria a roleta com base nas medias de acerto de cada vencedor da fase de selecao
def makeRoulette(population, winnersID):
    selected = getMultipleIndividuals(population, winnersID)
    rangeCeil = 0
    roulette = OrderedDict()
    for individual in selected:
        rangeCeil += individual.mediaAcerto
        roulette.update({individual.id: rangeCeil})
    roulette.update({0: rangeCeil * (1 / percentMutation)})
    return roulette


# Faz uma segunda selecao de alguns individuos anteriormente selecionados na fase de selecao
def selectionRoulette(roulette):
    rouletteCeil = list(roulette.items())[-1][1]            #Armazena em 'rouletteCeil' valor da ultima tupla adicionada a roleta, logo, retorna o teto do range armazenado na roleta
    chosen = uniform(0, rouletteCeil)                       #Selecao de um valor float dentro do range de valores armazenados na roleta
    rangeCeil = 0
    rangeFloor = rangeCeil
    for idIndividual, percentIndiv in roulette.items():     #Seleciona apenas um individuo para mutacao atraves do metodo da roleta viciada
        rangeCeil += percentIndiv
        if (chosen >= rangeFloor) and (chosen <= rangeCeil):
            return idIndividual
        rangeFloor = rangeCeil


# Realiza a mutacao propriamente dita
# Mutacao utiliza uma roleta viciada a fim de escolher individuos para mutar seus parametros
# Mutacao dos parametros propriamente dita eh feita utilizando Mutacao Uniforme
def mutation(population, minNoRange, optRange, checkErrorRateRange, usePruningRange, winnersID, qntMutations, numMutations = 1):
    sorted(population, key=lambda individual: individual.mediaAcerto)
    roulette = makeRoulette(population, winnersID)               #Cria a roleta com base nos individuos ganhadores da fase de selecao

    if DEBUG:
        print(roulette)

    for qnt in range(qntMutations):                              #Realiza processo de mutacao 'numMutations' vezes
        select = selectionRoulette(roulette)                     #Seleciona um ID de individuo de acordo com roleta viciada

        if DEBUG:
            print("")
            print("------- ID selecionado para mutacao - " + str(select))
            print("")

        if select == 0:                                          #Se ID selecionado para mutacao for ID '0', simplesmente sai do metodo, ja que ID '0' representa que nenhum individuo foi selecionado
            return population
        chosenIndividual = getIndividualByID(population, select)  #Caso ID seja um valor valido, ID eh repassado para resgatar o individuo relacionado
        params = list(range(1, 4))                               #Lista de parametros para armazenamento, utilizada para casos em que eh definido que a mutacao deve ocorrer em mais de um parametro
        for mutation in range(numMutations):                     #Seleciona um parametro aleatoriamente e o remove da lista de possiveis parametros para mutacao
            chosenParam = choice(params)
            params.remove(chosenParam)
            if chosenParam == 1:                                 #Realiza mutacao de atributo selecionando valor dentro do respectivo range aleatoriamente
                chosenIndividual.minNo = choice(minNoRange)
            elif chosenParam == 2:
                chosenIndividual.optimizations = choice(optRange)
            elif chosenParam == 3:
                chosenIndividual.checkErrorRate = choice(checkErrorRateRange)
            elif chosenParam == 4:
                chosenIndividual.usePruning = choice(usePruningRange)
    return population


######################################################################################















################################### Metodo 'Main' ####################################


def geneticAlgorithm(popSize, numFolds, minNoRange, optRange, checkErrorRateRange, usePruningRange, ConjuntoDeDados, numCalls, tourneyParticipants, roundsTourney, epochs, qntMutation, numMutations):

        # Geracao de populacao inicial aleatoria
        population = initPopulation(popSize, minNoRange, optRange, checkErrorRateRange, usePruningRange)

        # Procedimento se repete durante numero de epocas pre definidos
        for repeats in range(epochs):
            print("Epoca atual - " + str(repeats + 1))

            if DEBUG:
                print ("")
                print ("-----------INITIAL POPULATION-----------")
                printPopulation(population)


            # Realiza chamados ao Weka utilizando os dados da populacao inicial criada, alem de realizar a leitura e os calculos relacionados aos arquivos de saida do Weka
            population = stringWekaPopulation(population, ConjuntoDeDados, numFolds)
            callWekaPopulation(population)
            population = readOutputFiles(population, ConjuntoDeDados, numCalls)


            if DEBUG:
                print ("")
                print ("-----------POSCALC POPULATION-----------")
                printPopulation(population)

            # Captura os IDs dos individuos selecionados durante a fase de selecao
            winnersID = tourney(population, tourneyParticipants, roundsTourney)


            if DEBUG:
                print ("")
                print ("------------TOURNEY WINNERS-------------")
                print(winnersID)
                for ID in winnersID:
                    print(getIndividualByID(population, ID))
                print ("")
                print ("-----------------TOTAL------------------")
                printPopulation(population)


            # Realiza o crossover dos individuos da populacao selecionados durante a fase de selecao
            population = crossover(population, winnersID)


            if DEBUG:
                print ("")
                print ("---------------CROSSOVER----------------")
                printPopulation(population)


            # Realiza a mutacao de acordo com resultado da selecao alem de outros parametros pre estabelecidos
            population = mutation(population, minNoRange, optRange, checkErrorRateRange, usePruningRange, winnersID, qntMutation, numMutations)


            if DEBUG:
                print ("")
                print ("----------------MUTATION----------------")
                printPopulation(population)


            # Eh feita a limpeza da lista de strings de cada individuo da populacao, a fim de evitar que evitar que lista fique desatualizada com strings nao mais condizentes, alem de garantir que numero de strings fique consistente com numero de seeds
            if repeats < epochs - 1:
                    resetPopulationStats(population)

            # Metodo limpa arquivos gerados pelo Weka entre as diferentes eras
            cleanFiles(popSize, numCalls)


        # Ultima execucao de alguns metodos, a fim de preencher e calcular certos parametros dos individuos filhos recem gerados
        print("Realizando calculos finais levando em consideracao geracao de filhos recem gerada...")
        resetPopulationStats(population)
        stringWekaPopulation(population, ConjuntoDeDados, numFolds)
        callWekaPopulation(population)
        population = readOutputFiles(population, ConjuntoDeDados, numCalls)


        if DEBUG:
            print ("")
            print ("--------------FINAL POPULATION--------------")
            printPopulation(population)
            print ("")
            print ("---------------BEST INDIVIDUAL--------------")


        # Metodo retorna individuo com melhores parametros pertencente a populacao
        return findHighestMedia(population)


######################################################################################












############################### Main propriamente dita ###############################

print(geneticAlgorithm(popSize, numFolds, minNoRange, optRange, checkErrorRateRange, usePruningRange, ConjuntoDeDados, numCalls, tourneyParticipants, roundsTourney, epochs, qntMutation, numMutations))
