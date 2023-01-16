import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from configs import config

if not os.path.exists(config.graphPath):
    os.makedirs(config.graphPath)

class Graph:
    def __init__(self):
        pass

    def common_aspect_bar(self):
        """
        Return:  a bar of the most common words in each aspect
        """
        #get list aspects in dataframe
        df = pd.read_csv(config.biasFile)
        aspectList = df.columns.tolist()
        aspectList.remove('word_bias')
        aspectList.remove('char_count')

        # fig, axs = plt.subplots(9, 3, figsize=(40*9,25*3))
        figure = plt.figure(figsize=(50,30))

        #loop over aspects
        for idx, this_aspect in enumerate(aspectList):
            dfData = df[['word_bias',this_aspect]]
            #find row
            # row = idx//5
            # axs[row, idx].barh(dfData['word_bias'].tolist(), dfData[this_aspect].tolist(), color='blue')

            plt.bar(dfData['word_bias'].tolist(), dfData[this_aspect].tolist(), color='blue')
            plt.title(this_aspect, fontsize=50, color='g')
            plt.xticks(rotation=90, fontsize=16)
            plt.yticks(fontsize=40)
            plt.xlabel('Word', labelpad=100, fontsize=40)
            plt.ylabel('Percent', labelpad=100, fontsize=40)
            plt.grid(axis='y', linestyle='--')
            # plt.show()
            this_aspect = this_aspect.replace('/',' ')
            plt.savefig(os.path.join(config.graphPath, this_aspect + '.png'))


    def hist_word_count(self):
        """
        Return: histogram of common char count
        """
        #get list aspects in dataframe
        df = pd.read_csv(config.biasFile)
        word_count = df['char_count'].tolist()

        plt.figure(figsize=(30,30))
        plt.hist(word_count)

        plt.grid(axis='y', linestyle='--')
        plt.xlabel('char_count', fontsize=40, labelpad=100)
        plt.ylabel('Frequency', fontsize=40, labelpad=100)
        plt.xticks(fontsize=30)
        plt.yticks(fontsize=30)
        plt.title('Histogram of char_count', fontsize=50)
        plt.savefig(os.path.join(config.graphPath, 'char_count' + '.png'))

    def corr_aspect(self):
        """
        Return : a correlation matrix of all aspects 
        """
        df = pd.read_csv(config.biasFile)
        aspectList = df.columns.tolist()
        aspectList.remove('char_count')

        dfC = df[aspectList].copy()
        corr_matrix = dfC.corr()
        plt.figure(figsize=(50,40))
        corr = sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
        # fig = corr.get_figure()
        plt.xticks(fontsize=30)
        plt.yticks(fontsize=30)
        corr.figure.savefig(os.path.join(config.graphPath, 'correlation_common_aspect' + '.png'))


        

def _test():
    g = Graph()
    # g.common_aspect_bar()
    # g.hist_word_count()
    g.corr_aspect()


if __name__ == '__main__':
    _test()
