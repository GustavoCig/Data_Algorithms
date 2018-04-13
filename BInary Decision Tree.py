#Feito em Python 2.7


#Definicao de classe 'Tree' que sera usada para estruturacao dos dados da atividade.
#Cada noh possui um identificador que eh incrementado no momento da criacao de um novo noh.
#Dado do noh eh o proprio subconjunto do dataset original.
#Ramos a esquerda e direita do noh sao definidos como vazios ou tambem arvores, nao podendo ser outros valores.
#Atributo 'definedClass' se refere a classe que foi atribuida a um noh sem ramos.
#Atributo 'attribute' se refere a qual parametro do dataset foi utilizado no noh em questao para fazer a divisao em ramos.
#Metodo 'describe' faz uma especie de print 'ToString' da arvore, partindo do noh em que foi chamado o metodo e descendo pelos ramos. Listando os diversos valores dos parametros, alem de ajudar na identificacao da relacao de parentescom entre diferentes nohs.
class Tree:
      def __init__(self, dataset, treeLeft = None, treeRight = None):
          assert (treeLeft is None or isinstance(treeLeft, Tree)) and (treeRight is None or isinstance(treeRight, Tree)), "Please, use Tree-type variables for the left and right nodes or leave them empty."
          
          global idTree
          self.id = idTree
          self.node = dataset
          self.left = treeLeft
          self.right = treeRight
          self.definedClass = None
          self.attribute = None

          idTree += 1

      def describe(self, idParent = None):
          print "Tree - ",
          if idParent is not None:
             stringId = str(idParent) + "." + str(self.id)
          else:
             stringId = str(self.id)
          print stringId
          print "Value node - "
          print str(self.node)
          if self.attribute is not None:
             print "Attribute chosen:  X"+str(self.attribute)
          if self.definedClass is None:
             print "Left tree size - "
             self.left.describe(self.id) if self.left is not None else '0'
             print "Right tree size - "
             self.right.describe(self.id) if self.right is not None else '0'
          else:
             print "Class - " + str(self.definedClass)


#Faz a reformatacao da estrutura de armazenamento do dataset de entrada
def prepMatrix(dataset, numCases, numParameters):
    entries = dataset.read().split("\n")
    if '' in entries: entries.remove('')
    matrix = np.zeros(shape=(numCases, numParameters+1), dtype=int)
    for entry in range(numCases):
        matrix[entry] = entries[entry].split(',')
    return matrix


#Divide dataset passado como parametro em dois datasets utilizando o atributo, tambem passado como parametro, como ponto de corte.
#Parametro 'attribute' eh subtraido de 1 para adequar-se a sintaxe, jah que, vetores, em python, se iniciam na posicao 0.
#Funciona da seguinte forma: varre linha a linha do dataset de entrada e caso na linha em questao o valor do atributo passado como parametro seja 1, entao linha(elemento) eh atribuido a um dataset, caso contrario, eh atribuido a outro dataset.
def divDataset(dataset, attribute):
    attribute -= 1
    datasetLeft = []
    datasetRight = []
    for line in dataset:
	if line[attribute] == 1:
	   datasetLeft.append(line)
	elif line[attribute] == 0:
	     datasetRight.append(line)	  
    return datasetLeft, datasetRight


#Funciona de modo similar ao metodo 'prepMatrix' porem, sem as peculiaridades envolvidas na leitura do dataset de entrada, como a presenca de ',' e '\n'
#Converte do formato 'list' para 'numpy.array'
def convList2Array(dataset, numLines, numColumns):
    matrix = np.zeros(shape=(numLines, numColumns), dtype=int)
    for arrayIndex in range(numLines):
        for elementIndex in range(numColumns):
            matrix[arrayIndex, elementIndex] = dataset[arrayIndex][elementIndex]
    return matrix


#Metodo existente basicamente para dar suporte ao metodo 'convList2Array'.
#Verifica se algum dos datasets gerados eh vazio ou nao, passando, entao, o tamanho para o metodo 'convLis2Array' de modo a evitar erros relacionados ao acesso de valores inexistentes, por exemplo, a posicao '0' de um array vazio.
def divArray2Array(dataset, attribute):
    datasetLeft, datasetRight = divDataset(dataset, attribute)
    if len(datasetLeft) == 0:
       sizeLeft = 0
    else:
       sizeLeft = len(datasetLeft[0])

    if len(datasetRight) == 0:
       sizeRight = 0
    else:
       sizeRight = len(datasetRight[0])
    left = convList2Array(datasetLeft, len(datasetLeft), sizeLeft)
    right = convList2Array(datasetRight, len(datasetRight), sizeRight)
    return left, right



#Metodo faz o calculo da quantidade de aparicoes de elementos de classe 0 e 1 nos datasets da esquerda e da direta apos divisao.
#Metodo retorna 2 arrays e valores numericos, representando, respectivamente, a frequencia de aparicoes de 0s e 1s no dataset da esquerda e no da direta. Alem da contagem dos elementos em cada um desses datasets. 
def calcFreqClasses(datasetL, datasetR):
    countL = np.zeros(shape=(2),dtype=float)
    countR = np.zeros(shape=(2),dtype=float)
    if len(datasetL) != 0:
       for line in datasetL[:,len(datasetL[0])-1]:
           if line == 1:
              countL[1] += 1
           elif line == 0:
              countL[0] +=1
    if len(datasetR) != 0:
       for line in datasetR[:,len(datasetR[0])-1]:
	   if line == 1:
              countR[1] += 1
           elif line == 0:
              countR[0] +=1
    total = sum(countL) + sum(countR)
    if total != 0:
       freqL = countL/total
       freqR = countR/total
    else:
       freqL = 0
       freqR = 0	

    return freqL, freqR, sum(countL), sum(countR)


#Recebe os valores do retorno do metodo 'calcFreqClasses' como parametros de entrada.
#Calculo da entropia para cada set resultando, esquerda e direita, de uma divisao.
#Sendo feita a soma ponderada das entropias a fim de levar em consideracao a diferenca de tamanho entre ambos os datasets.
def calcEntropy(freqL, freqR, sizeSetLeft, sizeSetRight):
    entropyL0 = -freqL[0]*log(freqL[0],2) if freqL[0] != 0 else 0
    entropyL1 = -freqL[1]*log(freqL[1],2) if freqL[1] != 0 else 0

    entropyR0 = -freqR[0]*log(freqR[0],2) if freqR[0] != 0 else 0
    entropyR1 = -freqR[1]*log(freqR[1],2) if freqR[1] != 0 else 0

    sizeSet = sizeSetLeft + sizeSetRight
    entropyLeft = entropyL0 + entropyL1
    entropyRight = entropyR0 + entropyR1
    ponderedMeanLeft = (sizeSetLeft/sizeSet)*entropyLeft
    ponderedMeanRight = (sizeSetRight/sizeSet)*entropyRight

    return ponderedMeanLeft + ponderedMeanRight


#Faz a varredura dos diversos parametros disponiveis para serem usados para divisao, fazendo o calculo da entropia resultante em cada uma dessas divisoes, escolhendo o parametro, logo, a divisao, que resulta na maior diminuicao de entropia.
#Se algum dos datasets resultantes de uma divisao, nessa varredura, for vazio, ignora o parametro e a divisao como um todo, jah que nao haveria ganho algum de entropia.
#Retorna parametro que levou a maior diminuicao da entropia.
def minEntropy(dataset, parameters):
    lowest = 9999
    best_param = -1
    for param_test in parameters:
        datasetLeft, datasetRight = divArray2Array(dataset, param_test)
        if (datasetLeft is None) or (datasetRight is None):
           continue
        else:
           freqL, freqR, sizeSetLeft, sizeSetRight = calcFreqClasses(datasetLeft, datasetRight)
           entropy = calcEntropy(freqL, freqR, sizeSetLeft, sizeSetRight)
           if lowest > entropy:
              lowest = entropy
              best_param = param_test
    return best_param



#Cria a arvore recursivamente, atribuindo o dataset de entrada como 'nodo' do topo da arvore.
#Eh feita uma copia do array de parametros, 'params', utilizando o metodo 'copy.deepcopy', jah que, em python, os metodos de acesso a listas, como 'list.remove', afetam a lista globalmente, o que interferiria com a logica do metodo.
#Funcionamento: basicamente utiliza do metodo 'minEntropy' para verificar divisoes que resultem no menor valor de entropia, verificando se ha datasets resultantes da divisao que sejam menores que o valor 'numMinObj', caso sim, divisao e parametro utilizados na divisao sao descartados e processo se repete.
#Ao encontrar um parametro que divida meu dataset do nodo de modo satisfatorio eh chamada, recursivamente, o proprio metodo 'createTree' para os ramos da esquerda e da direita do nodo atual, atribuindo tambem ao atributo 'tree.attribute' o parametro utilizado para fazer essa divisao.
#Como condicao de parada eh verificado o tamanho do array de parametros, caso nao haja mais parametros para serem testados para uma possivel divisao do dataset do nodo atual, eh atribuido ao nodo a classe resultante do metodo 'defineClass' e retorna a 'Tree' atual.
def createTree(dataset, params, numMinObj):
    tree = Tree(dataset)
    parameters = copy.deepcopy(params)
    if len(parameters) == 0:
       tree.definedClass = defineClass(tree.node)
       return tree
    else:
       param_chosen = minEntropy(dataset, parameters)
       treeLeft, treeRight = divArray2Array(dataset, param_chosen)
       parameters.remove(param_chosen)
       while (len(treeLeft) < numMinObj) or (len(treeRight) < numMinObj):
             if len(parameters) == 0:
                tree.definedClass = defineClass(tree.node)
                return tree
             else:
                param_chosen = minEntropy(dataset, parameters)
                treeLeft, treeRight = divArray2Array(dataset, param_chosen)
                parameters.remove(param_chosen)
       tree.attribute = param_chosen
       tree.left = createTree(treeLeft, parameters, numMinObj)
       tree.right = createTree(treeRight, parameters, numMinObj)
    return tree


#Basicamente faz uma soma das classes presentes dentro de um certo dataset, retornando classe 1, caso haja um numero maior ou igual de elementos de classe 1 no dataset, ou classe 0, caso haja um numero maior de elementos de classe 0 no dataset.
def defineClass(dataset):
    count0 = 0
    count1 = 0
    for line in dataset[:,len(dataset[0])-1]:
        if line == 1:
           count1 += 1
        else:
           count0 += 1
    if count1 >= count0:
       return 1
    else:
       return 0




#Metodo criado para dar inicio no processo de conversao recursivo da arvore do formato da classe 'Tree' para formato da linguagem 'DOT', mais especificamente do pacote 'graphviz'
#No fim, salvando o codigo fonte resultante da linguagem 'DOT' no arquivo 'Digraph.gv' e visualizando a o grafo resultante.
def beginTree2Graph(tree):
    dot = Digraph(comment="Arvore de Decisao")
    dot.node(str(tree.node))
    tree2Graph(dot, tree).render('Digraph.gv', view=True)


#Realiza a conversao recursiva de 'Tree' para 'DOT'.
#Varre nodos e seus filhos, criando vertices e arestas com base nos atributos da arvore.
#Para ao alcancar um nodo que nao possui filhos e retorna.
def tree2Graph(dot, tree):
    if tree.left is not None:
       if tree.left.definedClass is not None:
          dot.node(str(tree.left.node)+'\n'+"Classe = "+str(tree.left.definedClass))
          dot.edge(str(tree.node), str(tree.left.node)+'\n'+"Classe = "+str(tree.left.definedClass), 'X'+str(tree.attribute)+' = 1')
       else:
          dot.node(str(tree.left.node))
          dot.edge(str(tree.node), str(tree.left.node), 'X'+str(tree.attribute)+' = 1')
       tree2Graph(dot, tree.left)
    if tree.right is not None:
       if tree.right.definedClass is not None:
          dot.node(str(tree.right.node)+'\n'+"Classe = "+str(tree.right.definedClass))
          dot.edge(str(tree.node), str(tree.right.node)+'\n'+"Classe = "+str(tree.right.definedClass), 'X'+str(tree.attribute)+' = 0')
       else:
          dot.node(str(tree.right.node))
          dot.edge(str(tree.node), str(tree.right.node), 'X'+str(tree.attribute)+' = 0')
       tree2Graph(dot, tree.right)

    if (tree.left is not None) and (tree.right is not None):
       return dot
    
    
	
import numpy as np
import copy
from graphviz import Digraph
from math import log

#Leitura e captura de parametros do dataset de entrada
dataset = open('arquivo2.txt','r')
numCases = int(dataset.readline())
numParameters = int(dataset.readline())

#Criacao de vetor de parametros a serem utilizados como pivo de divisoes.
params = []
for paramsIndex in range(numParameters):
    params.append(paramsIndex+1)


#Inicializacao do id global das arvores.
idTree = 1

#Inicializacao do parametro 'minNumObj'.
minNumObj = 2

#Dataset de entrada reformatado, facilitando a captura de parametros especificos como a 
#classe e os valores de entrada para cada caso
cases = prepMatrix(dataset, numCases, numParameters)


#Cria arvore recursivamente passando o dataset reformatado, vetor inicializado de parametros e parametro 'numMinObj' inicializado.
tree = createTree(cases, params, minNumObj)

#Printa arvore resultante conforme metodo 'describe'.
tree.describe()

#Converte formato da arvore resultante.
beginTree2Graph(tree)
