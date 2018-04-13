#Feito em Python2.7


#Faz a reformatacao da estrutura de armazenamento do dataset de entrada
def prepMatrix(dataset, numCases, numParameters):
    entries = dataset.read().split("\n")
    if '' in entries: entries.remove('')
    matrix = np.zeros(shape=(numCases, numParameters+1), dtype=int)
    for entry in range(numCases):
        matrix[entry] = entries[entry].split(',')
    return matrix


#Gera a hipotese inicial
#Usa uma matriz 3D de associacao que armazena na terceira dimensao dois valores
#para geracao de monomios de tamanho dois. No caso onde eh apenas um monomio, 
#exemplo: x1 , x2 ,xn, o primeiro valor armazenado eh o do monomio e o segundo eh o valor 
#zero, que na matriz opera como uma especie de don't care.
#No seguinte formato:
#
#          |  x1  |  x2  |...|  xn  |  x-1  |...|  x-n  |
#        x1|  x1  | x1x2 |...|  xn  | x1x-1 |...| x1x-n |
#        x2|  0   |  x2  |...| x2xn | x2x-1 |...| x2x-n |
#         .|  .   |   .  |  .
#         .|  .   |   .  |     .
#         .|  .   |   .  |        .
#        xn|  0   |   0  |           .
#       x-1|  0   |   0  |              .
#         .|  .   |   .  |                 .
#         .|  .   |   .  |                    .
#       x-n|  0   |   0  |                       .
#
#Para evitar repeticao desnecessaria de valores, todos as posicoes abaixo da diagonal 
#principal sao ignorados, sendo deixados com valor 0(don't care)
def initHypotesis(numParameters):
    numNegatedAndPositive = 2*numParameters
    monomials = np.zeros(shape=(numNegatedAndPositive,numNegatedAndPositive,2),dtype=int)
    for indexOut in range(numNegatedAndPositive):
        if indexOut/numParameters == 1:
           attributeOut = -(indexOut%numParameters+1)
        else:
           attributeOut = indexOut+1
        for indexIn in range(numNegatedAndPositive):
            if indexIn/numParameters == 1:
               attributeIn = -(indexIn%numParameters+1)
            else:
               attributeIn = indexIn+1
	    if indexOut < indexIn:
               continue
            elif indexIn == indexOut:
               monomials[indexOut][indexIn][0] = attributeIn
            else:
               monomials[indexOut][indexIn][0] = attributeOut
               monomials[indexOut][indexIn][1] = attributeIn
            if ((monomials[indexOut][indexIn][0] == -monomials[indexOut][indexIn][1]) or (-monomials[indexOut][indexIn][0] == monomials[indexOut][indexIn][1])):
               monomials[indexOut][indexIn][0] = 0
               monomials[indexOut][indexIn][1] = 0
    return monomials


#Apenas faz a formatacao dos valores passados em matriz para ser impresso na forma de 
#disjuncao de monomios
def listHypotesis(matrix):
    num, num, aux =  matrix.shape
    for indexOut in range(num):
        for indexIn in range(num):
            if matrix[indexOut][indexIn][0] != 0: print "x" + str(matrix[indexOut][indexIn][0]),
            if matrix[indexOut][indexIn][1] != 0: print "x" + str(matrix[indexOut][indexIn][1]),
            if ((matrix[indexOut][indexIn][1] != 0) or (matrix[indexOut][indexIn][0] != 0)): print "V",


#Faz uma formatacao previa do array contendo os numeros a serem eliminados da matriz de 
#hipoteses, de forma a simplificar sua remocao
def prepArrayRemove(values):
    array = []
    for elemOut in values:
        for elemIn in values:
            if elemOut == elemIn:
               array.append([elemIn,0])
            else:
               array.append([elemIn,elemOut])
    return array


#Remove da matriz passada por parametro o aray de valores passados tambem por parametro,
#substituindo-os por 0
def removeMonomials(matrix, values):
    size1, size2, size3 = matrix.shape
    for element in values:
        for indexOut in range(size1):
            for indexIn in range(size2):
                if (matrix[indexOut][indexIn][0] == element[0]) and (matrix[indexOut][indexIn][1] == element[1]):
                   matrix[indexOut][indexIn][0] = 0
                   matrix[indexOut][indexIn][1] = 0
    return matrix


#Executa a remocao dos valores da matriz de hipoteses onde a classe definida no dataset de entrada seja 0 e onde pelo menos um dos seus parametros tenha valor 1
def processHypotesis(monomials, params, classes):
    numOut = classes.size
    numIn = params[1].size
    for indexOut in range(numOut):
        values = []
        classInit = 0
        if classes[indexOut] == 0:
            for indexIn in range(numIn):
                if params[indexOut, indexIn] == 1:
                   values.append((indexIn+1)) 
                else:
                   values.append(-(indexIn+1))
                classInit = (params[indexOut, indexIn]) + classInit
        if classInit != 0:
            monomials = removeMonomials(monomials,prepArrayRemove(values))
    return monomials


import numpy as np

#Leitura e captura de parametros do dataset de entrada
dataset = open('arquivo0.txt','r')
numCases = int(dataset.readline())
numParameters = int(dataset.readline())

#Dataset de entrada reformatado, facilitando a captura de parametros especificos como a 
#classe e os valores de entrada para cada caso
cases = prepMatrix(dataset, numCases, numParameters)
params = cases[:,0:numParameters]
classes = cases[:,numParameters]

#Gera a hipotese inicial para o dataset utilizado
monomials = initHypotesis(numParameters)
print "- Hipotese inicial:"
listHypotesis(monomials)
print " "
print " "

#Faz o processamento e eliminacao de certos monomios do espaco de hipoteses inicial
hypotesis = processHypotesis(monomials, params, classes)
print "- Hipotese final(pos processamento):"
listHypotesis(hypotesis)
dataset.close()
