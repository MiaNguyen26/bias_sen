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
        Return: a df contains the n most common words in each aspect
                which has 26*n rows and 4 columns: aspect, common_word, freq, char_count

        """
        dfSumCommon = pd.DataFrame()

        for aspect in config.listAspect:
            dfAspect = self.df.loc[self.df['aspect'] == aspect]
            words = dfAspect['processed']
            allwords = []
            for wordlist in words:
                wordList = ast.literal_eval(wordlist)
                wordList = [word for word in wordList  if re.match(r'^-?\d+(?:\.\d+)$', word) is None and word.isdigit() == False]

                allwords += wordList

    
            mostcommon = FreqDist(allwords).most_common(config.num_common)

            x, y = zip(*mostcommon)
            # count no. char in each common word
            word_char_count = [len(word) for word in x]

            listAspect = [aspect] * len(x)

            dfCommon = pd.DataFrame({'aspect': listAspect, 'common_words': x, 'freq': y, 'char_count': word_char_count})

            dfSumCommon = pd.concat([dfSumCommon, dfCommon], axis=0)
        
        dfSumCommon.to_csv(os.path.join(config.edaPath, 'common_words_each_aspect.csv'), index=False)

        return mostcommon

def  _test():
    df = pd.read_csv(config.preprocessFile)
    a =WordBIAS(df)
    common = a.get_common_each_aspect()

    return common

if __name__ == '__main__':
    a = _test()



