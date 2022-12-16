# -*- coding: utf-8 -*-
"""
This module contains the Graph class, which is used to represent a graph.
# It contains the following graph:
Sentiment Analysis, Word Count, Word Common

"""


import os, sys

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
# from sklearn.feature_extraction.text import CountVectorizer

# from data_ana import eda
from configs import config
# from ..configs import config
from .eda import EDA

class Graph:
    def __init__(self, dfProcess, mostcommon, allwords, listVocab, charCount):
        self.dfProcess = dfProcess
        self.mostcommon = mostcommon
        self.allwords = allwords
        self.listVocab = listVocab
        self.charCount = charCount
    
    def graph_word_count(self):
        #correlation heatmap for word count and review length
        correlation = self.dfProcess[['word_count',  'review_len']].corr()
        mask = np.zeros_like(correlation, dtype=np.bool)
        mask[np.triu_indices_from(mask)] = True
        plt.figure(figsize=(50,30))
        plt.xticks(fontsize=40)
        plt.yticks(fontsize=40)
        sns.heatmap(correlation, cmap='coolwarm', annot=True, annot_kws={"size": 40},
                    linewidths=10, vmin=-1.5, mask=mask)
        plt.title('Correlation Heatmap', fontsize=60)
        plt.savefig(os.path.join(config.graphPath, 'heatmap.png'))

        
    def graph_word_common(self, num=25):
        x, y = zip(*self.mostcommon)

        plt.figure(figsize=(50,30))
        plt.margins(0.02)
        plt.bar(x,y)
        plt.xlabel('Words', fontsize=50)
        plt.ylabel('Frequency of Words', fontsize=50)
        plt.yticks(fontsize=40)
        plt.xticks(rotation=60, fontsize=40)
        plt.title('Frequency of {} Words'.format(num), fontsize=60)
        plt.savefig(os.path.join(config.graphPath, 'wordcommon.png'))

    def graph_vocal(self):
        bin = 60
        fig = plt.figure(figsize=(50,30))
        plt.hist(self.charCount, bins=bin)
        plt.xlabel('Words', fontsize=50, labelpad=100)
        plt.ylabel('Frequency', fontsize=50, labelpad=100)
        plt.yticks(fontsize=40)
        plt.xticks(fontsize=40)
        plt.xlim([1,30])
        #remove the first tick in x axis

        # xticks = ax.xaxis.get_major_ticks()
        # xticks[0].label1.set_visible(False)

        plt.title('Frequency of \'the number of characters in each vocab\' with bin = {}'.format(bin), fontsize=60)
        plt.savefig(os.path.join(config.graphPath, 'vocal.png'))




def _test():

    num = int(input("Enter the number of common words: "))
    dfProcess = pd.read_csv(config.processedFile)
    # dfProcess = pd.read_csv(config.processedFile)
    eda= EDA(dfProcess)
    allwords, listVocab, charVocab, mostcommon = eda.vocab(num)
    
    graph = Graph(dfProcess, mostcommon, allwords, listVocab, charVocab)
    # graph.graph_word_count()
    graph.graph_word_common(num)
    graph.graph_vocal()


if __name__ == '__main__':
    _test()
    