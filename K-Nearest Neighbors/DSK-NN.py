def formatDataset(dataset, params, classes):
    reformatedDataset = np.zeros(shape=(params,classes),dtype=int)
    print reformatedDataset
    for line in dataset.split("\n"):
        reformatedDatasetLine = []
        for value in line:
            if value == ',':
               continue
            else:
               reformatedDatasetLine.append(int(value))
        if reformatedDatasetLine == []:
           continue
        else:
           reformatedDataset.append(reformatedDatasetLine)
    return reformatedDataset

def shufflingDataset(dataset):
    shuffle(dataset)
    return dataset

def settingTrainingSet(dataset, numEntries):
    dataset = shufflingDataset(dataset)
    percTraining = 50
    numTraining = int(math.floor(percTraining*numEntries/100))
    trainingDataset = dataset[0:numTraining]
    testingDataset = dataset[numTraining:]
    return trainingDataset, testingDataset
    
def gettingParams(dataset):
    params = []
    classes = []
    numEntries = len(dataset)
    numParams = len(dataset[0])-1
    for line in dataset:
        paramsLine = []
        for index in range(len(line)):
            if index == len(line):
               classes.append(line[index])
            else:
               paramsLine.append(line[index])
        params.append(paramsLine)
    return params, classes, numEntries, numParams

def KNN(trainingDataset, testingDataset):
    print "input a value for the 'K' value:"
    k = 3
    print k
    classTest=[]
    for line in testingDataset:
        results=[]
        for line2 in trainingDataset:
            results.append(sum((np.array(line)-np.array(line2))**2))
        print np.array(results)
        print np.where(results == min(np.array(results)))
        classTest.append(np.array(trainingDataset)[0][np.where(results==min(results))])
    return classTest
    
    
from random import shuffle
import math
import numpy as np

file = open('dataset.txt','r')
dataset = file.read()
params = []
params = gettingParams(dataset)
print params[3]


dataset = shufflingDataset(formatDataset(dataset,params[0], params[1]))
params, classes, numEntries, numParams = gettingParams(dataset)
training, testing = settingTrainingSet(dataset, numEntries)
print KNN(training, testing)


