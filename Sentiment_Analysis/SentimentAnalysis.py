import string

def readFile(inputFile):
    formedFilelist=[]
    classlabel = []
    with open(inputFile, "r", encoding='utf-8') as f:
        for line in f:
            #get the classlable
            line = line.split('\t')
            classlabel.append(line[1].strip(' \n'))
            line = line[0]
            #remove punctuations and convert to lower case
            line = line.translate(str.maketrans('','',string.punctuation+string.digits)).lower()
            #split string to list
            line = line.split()
            formedFilelist.append(line)
    return classlabel, formedFilelist


def formVocabulary(formedFilelist):
    vocabularyList = []
    for eachSen in formedFilelist:
        for eachWord in eachSen:
            if((eachWord not in vocabularyList) and (not eachWord.isdigit())):
                vocabularyList.append(eachWord)
    vocabularyList.sort()
    return vocabularyList

def convert2Features(formedFilelist, vocabularyList, classlabel):
    featureVectors = []
    for i in range(len(formedFilelist)):
        eachVector = []
        for eachWord in vocabularyList:
            if eachWord in formedFilelist[i]:
                eachVector.append(1)
            else:
                eachVector.append(0)
        eachVector.append(int(classlabel[i]))
        featureVectors.append(eachVector)
    return featureVectors

def outputPreProcessData(vocabularyList, featureVectors, outFile):
    with open(outFile, "w+", encoding='utf-8') as f:
        for eachWord in vocabularyList:
            f.write(eachWord+", ")
        f.write("classlabel\n")
        for eachline in featureVectors:
            for i, eachele in enumerate(eachline):
                if i != len(eachline)-1:
                    f.write(str(eachele)+", ")
                else:
                    f.write(str(eachele)+"\n")

def get_P_N_Sen(featureVectors):
    posList = []
    negList = []
    for each in featureVectors:
        if each[-1] == 1:
            posList.append(each)
        else:
            negList.append(each)
    return posList, negList

def get_P_WordGivePosOrNeg(trainPosOrNegList):
    p_WordGivePosOrNegList = []
    eachLineLen = len(trainPosOrNegList[0])
    for i in range(eachLineLen-1):
        curWordNum = 0
        for eachLine in trainPosOrNegList:
            if eachLine[i] == 1:
                curWordNum+=1
        p_WordGivePosOrNegList.append((curWordNum+1)/(len(trainPosOrNegList)+2))

    return p_WordGivePosOrNegList

def classificationStep(trainPosList, trainNegList, testFeatureVectors, testClasslabel):
    poslen = len(trainPosList)
    neglen = len(trainNegList)
    #get number of postive and negative senctence number and cal p(1) and p(0)
    p_Pos = poslen/(poslen+neglen)
    p_Neg = neglen/(poslen+neglen)
    # get probability of all Vocabulary given it is positive
    p_WordGivePosList = get_P_WordGivePosOrNeg(trainPosList)
    p_WordGiveNegList = get_P_WordGivePosOrNeg(trainNegList)
    correctness = nativeBayesTest(p_Pos, p_Neg, p_WordGivePosList, p_WordGiveNegList, testFeatureVectors, testClasslabel)
    return correctness


def nativeBayesTest(p_Pos, p_Neg, p_WordGivePosList, p_WordGiveNegList, testFeatureVectors, testClasslabel):
    correctNum = 0;
    for j, eachLine in enumerate(testFeatureVectors):
        p_PosTemp = p_Pos
        p_NegTemp = p_Neg
        isPos = 0
        for i in range(len(eachLine)-1):
            if (eachLine[i] == 1):
                p_PosTemp = p_PosTemp*p_WordGivePosList[i]
                p_NegTemp = p_NegTemp*p_WordGiveNegList[i]
            else:
                p_PosTemp = p_PosTemp*(1-p_WordGivePosList[i])
                p_NegTemp = p_NegTemp*(1-p_WordGiveNegList[i])
        if p_PosTemp > p_NegTemp:
            isPos = 1
        if isPos == int(testClasslabel[j]):
            correctNum+=1
    return correctNum/len(testFeatureVectors)

def outputResult(correctnessTrain, correctnessTest):
    with open("results.txt", "w+") as f:
        f.write("Training: trainingSet.txt\n\
Testing: trainingSet.txt\nAccuracy:"+str(correctnessTrain))
        f.write("\n\nTraining: trainingSet.txt\n\
Testing: testSet.txt\nAccuracy:"+str(correctnessTest))

def run(trainFile, testFile):
    trainClasslabel, formedTrainFilelist = readFile(trainFile)
    vocabularyList = formVocabulary(formedTrainFilelist)
    trainFeatureVectors = convert2Features(formedTrainFilelist, vocabularyList, trainClasslabel)
    testClasslabel, formedTestFilelist = readFile(testFile)
    testFeatureVectors = convert2Features(formedTestFilelist, vocabularyList, testClasslabel)
    #output the pre process data
    outputPreProcessData(vocabularyList, trainFeatureVectors, "preprocessed_train.txt")
    outputPreProcessData(vocabularyList, testFeatureVectors, "preprocessed_test.txt")
    # put the postive and negative sentences into two list
    trainPosList, trainNegList = get_P_N_Sen(trainFeatureVectors)
    #get the correctness
    correctnessTrain = classificationStep(trainPosList, trainNegList, trainFeatureVectors, trainClasslabel)
    correctnessTest = classificationStep(trainPosList, trainNegList, testFeatureVectors, testClasslabel)
    #output the result
    outputResult(correctnessTrain, correctnessTest)


if __name__ == "__main__":
    trainFile = "trainingSet.txt"
    testFile = "testSet.txt"
    run(trainFile, testFile)
   


