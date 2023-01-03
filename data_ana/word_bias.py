# coding: utf-8
"""
    Date created: Dec 26, 2022
    Last modified: Dec 26, 2022
    Author: Mia Nguyen
    Description: 
        

"""
# import eda
from configs import config

import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import os
import re 

from nltk.probability import FreqDist
import ast


class WordBIAS():
    def __init__(self, df):
        self.df = df

    def get_common_each_aspect(self):
        """
        Return: a df contains the n most common, freq and percentage words in each aspect
                which has n rows and 26 columns, each column is a aspect

        """
        dfSumCommon = pd.DataFrame()
        all_aspects = []
        listDf = []
        dataDict = {}

        for aspect in config.listAspect:
            dfAspect = self.df.loc[self.df['aspect'] == aspect]
            words = dfAspect['processed']
            allwords = []
            for wordlist in words:
                wordList = ast.literal_eval(wordlist)
                wordList = [word for word in wordList  if re.match(r'^-?\d+(?:\.\d+)$', word) is None and word.isdigit() == False]

                #all words in an aspect
                allwords += wordList

            #number of words in an aspect
            freq_words = len(allwords)
            # get n most common words
            mostcommon = FreqDist(allwords).most_common(config.num_common)

            x, y = zip(*mostcommon)
            # count no. char in each common word
            word_char_count = [len(word) for word in x]
            #get percentage of each word
            percent = [round((freq/freq_words)*100, 4) for freq in y]

            aspectName = [aspect]
            aspect_space = [' '] * (len(config.word_common)-1)
            aspectName.extend(aspect_space)

            dfCommon = pd.DataFrame({'common_words': x, 'freq': y, 'percent': percent, 'char_count': word_char_count})
            dfCommon.columns = pd.MultiIndex.from_tuples(zip(aspectName, dfCommon.columns))
            listDf.append(dfCommon)


        dfSumCommon = pd.concat(listDf, axis=1)
        
        dfSumCommon.to_csv(os.path.join(config.edaPath, 'common_words_each_aspect.csv'), index=False)

        return mostcommon

def  _test():
    df = pd.read_csv(config.preprocessFile)
    a =WordBIAS(df)
    common = a.get_common_each_aspect()

    return common

if __name__ == '__main__':
    a = _test()



