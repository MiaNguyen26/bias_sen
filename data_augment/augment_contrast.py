import numpy as np
import pandas as pd
import random
import os

from configs import config

if not os.path.exists(config.augmentPath):
    os.makedirs(config.augmentPath)

class Augment_Contrast():
    def __init__(self):
        self.positive = config.positiveFile
        self.negative = config.negativeFile
        self.linking = config.linkingFile

    def load_polarity(self, path):
        dictPol = {}  

        with open(path, 'r') as f:
            for line in f:
                if not line.isspace():
                    line = line.strip()
                    if line.startswith('#'):
                        content = []
                        new_key = str(line[1:]).strip()
                        dictPol[new_key] = content
                    else:
                        content.append(line)

        return dictPol
    
    def get_positive(self):
        return self.load_polarity(self.positive)
    
    def get_negative(self):
        return self.load_polarity(self.negative)

    def get_linkWord(self):
        with open(self.linking, 'r') as f:
            return [line.strip() for line in f]
        
    def generate_sample(self):
        positiveDict = self.get_positive()
        negativeDict = self.get_negative()
        linkWord = self.get_linkWord()

        aspectList = list(positiveDict.keys())
        num = int(config.num_sample / len(aspectList)) +1
        posList = []
        negList = []
        linkList = []

        for aspect in aspectList:
            pos = positiveDict[aspect]
            neg = negativeDict[aspect]
            for i in range(0, num):
                posList.append(random.choice(pos))
                negList.append(random.choice(neg))
                linkList.append(random.choice(linkWord))

        random.shuffle(posList)
        random.shuffle(negList)
        random.shuffle(linkList)

        for elem in zip(posList, linkList, negList):
            line = ' '.join(elem)
            with open(os.path.join(config.augmentPath, 'contrast.txt'), 'a') as f:
                f.write(line + '\n')


def _test():
    aug = Augment_Contrast()
    # a = aug.get_positive()
    # a = aug.load_linkWord()
    a = aug.generate_sample()
    # print(a)

if __name__ == '__main__':
    _test()
                        






