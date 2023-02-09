# coding: utf-8
"""
    Date created: Dec 26, 2022
    Last modified: Dec 26, 2022
    Author: Mia Nguyen
    Description: Get proposed bias words
                1. Get common words(and freq, percentage, char_count) in each aspect
                2. Preprocessing those common words (remove stopwords and get words have freq>10)
                3. Get proposed bias words

"""
import data_ana.eda_test as eda_test
from configs import config

import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import os
import re 
import pyvi
from pyvi import ViTokenizer
import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from tqdm import tqdm
import ast


class WordBIAS():
    def __init__(self, df):
        self.df = df


    def get_common_each_aspect(self):
        """
        Input: df , which was preprocessed, contains many columns but must have post_id, text, aspect, processed (text)
        Return: a df contains the n most common words, freq and percentage words in each aspect
                which has n rows and 26 columns, each column is a aspect

        """
        dfSumCommon = pd.DataFrame()
        listDf = []

        for aspect in config.listAspect:

            dfAspect = self.df.loc[self.df['aspect'] == aspect].copy()
            words = dfAspect['processed'].copy()
            allwords = []
            for wordlist in words:
                wordList = ast.literal_eval(wordlist)

                wordList = [word for word in wordList  if re.match(r'^-?\d+(?:\.\d+)$', word) is None and word.isdigit() == False]
                #all words in an aspect
                allwords += wordList

            #number of words in an aspect (also auplicate words)
            freq_words = len(allwords)
            if not allwords:
                continue

            # get n most common words
            mostcommon = FreqDist(allwords).most_common(config.num_common)

            x, y = zip(*mostcommon)
            # count no. char in each common word
            word_char_count = [len(word) for word in x]
            #get percentage of each word
            percent = [round((freq/freq_words), 4) for freq in y]

            #get aspect for header
            aspectName = [aspect]
            aspect_space = [' '] * (len(config.word_common)-1)
            aspectName.extend(aspect_space)
            aspectList = [aspect]*4

            #get dataframe for each aspect
            dfCommon = pd.DataFrame({'common_words': x, 'freq': y, 'percent': percent, 'char_count': word_char_count})
            
            # dfCommon.columns = pd.MultiIndex.from_tuples(zip(aspectName, dfCommon.columns))
            # print(list(dfCommon.columns))
            a = [aspectList, list(dfCommon.columns)]
            dfCommon.columns = a
            listDf.append(dfCommon)


        dfSumCommon = pd.concat(listDf, axis=1)
        
        # dfSumCommon.to_csv(os.path.join(config.edaPath, 'common_words_each_aspect.csv'), index=False)
        dfSumCommon.to_csv(config.commonFile, index=False)
        return mostcommon


    def preprocess_word_common(self):
        #------ remove stopwords and get words have freq >=10----------------
        #list stopwords
        with open(config.stopwordFile, 'r') as f:
            stopwords_vi = [line.strip() for line in f]
            stopwords_token = [ViTokenizer.tokenize(word) for word in stopwords_vi]
        
        stopwords_en = stopwords.words('english')
        stopwords_german = stopwords.words('german')
        stopwords_french = stopwords.words('french')

        stopwords_token.extend(stopwords_en)
        stopwords_token.extend(stopwords_german)
        stopwords_token.extend(stopwords_french)

        #read common word file
        df = pd.read_csv(config.commonFile, header=[0,1])
        dfFinal = pd.DataFrame()
        listDF = []

        #get list aspects in dataframe
        a = df.columns.to_flat_index()
        a = list(a)
        aspects = [aspect[0] for aspect in a]
        aspectList = list(set(aspects))
  
        for aspect in aspectList:
            #aspect List
            aspect_header = [aspect]*4

            dfN = df[[(aspect, 'common_words'), (aspect, 'freq'), (aspect, 'percent'), (aspect, 'char_count')]]
            dfN.columns = dfN.columns.droplevel(0)
            dfN1 = dfN.loc[(dfN['freq'] >= config.freq_threshold) & (~dfN['common_words'].isin(stopwords_token))].copy()

            header = [aspect_header, ['common_words', 'freq', 'percent', 'char_count']]
            dfN1.columns = header

            #replace nan/ empty cell
            dfN1.replace('', np.nan, inplace=True)
            dfN1.dropna(how='all', inplace=True)
            dfN1.reset_index(drop=True, inplace=True)
            listDF.append(dfN1)
        
            
        dfFinal = pd.concat(listDF, axis=1)
        # dfFinal.to_csv(os.path.join(config.edaPath, 'word_bias_preprocess.csv'), index=False)
        dfFinal.to_csv(config.wordbiasFile, index=False)
        

    def get_proposed_bias(self):

        """
        Return: a df contains those columns: bias, word_count,
                and aspects with each cell is the percentage of word in that aspect
        """

        # -----------------get bias-----------------------
        #read preprocess word_bias file (removed stopwords and freq threshold)
        dfCommon = pd.read_csv(config.wordbiasFile, header=[0,1])
        #get list aspects in dataframe
        aspectList = dfCommon.columns.levels[0].tolist()

        header = ['word_bias', 'char_count'] + config.listAspect
        dfBias = pd.DataFrame(columns=header)

        
        biasSet = set()

        #get list aspects in dataframe

        for idx, this_aspect in enumerate(tqdm(aspectList)):
            idxList = np.arange(idx+1, len(aspectList)).tolist()

            #get this(aspect) word value
            wordList = dfCommon[(this_aspect, 'common_words')].copy()
            wordList.dropna(how='all', inplace=True)
            wordList = wordList.tolist()

            #loop over aspects after this aspect                
            for idx1 in idxList:
                # aspect1 = config.listAspect[idx1]
                aspect1 = aspectList[idx1]

                #get aspect common_word
                wordList1 = dfCommon[(aspect1, 'common_words')].copy()
                wordList1.dropna(how='all', inplace=True)
                wordList1 = wordList1.tolist()

                #compare two list common words
                word_bias = list(set(wordList).intersection(wordList1))

                #check bias is empty or not
                if not word_bias:
                    # print('no bias')
                    continue
                else:
                    for bias in word_bias:
                        
                        a1 = dfCommon.loc[dfCommon[(aspect1, 'common_words')] == bias]
                        a1 = a1[(aspect1)]
                        bias_percent1 = a1['percent'].iloc[0]

                        #check if bias existed or not
                        if bias in biasSet:
                            #add percent to corresponding aspect column
                            row_idx = dfBias.index[dfBias['word_bias'] == bias].tolist()[0]
                            dfBias.at[row_idx, aspect1] = bias_percent1
            
                        else:
                            #get bias char count and perccentage in this aspect
                            a0 = dfCommon.loc[dfCommon[(this_aspect, 'common_words')] == bias]
                            a0 = a0[(this_aspect)]
                            bias_char_count = a0['char_count'].iloc[0]
                            bias_percent0 = a0['percent'].iloc[0]

                            new_row = [{'word_bias': bias, 'char_count': bias_char_count,this_aspect: bias_percent0, aspect1: bias_percent1}]
                            dfB = pd.DataFrame(new_row)
                            dfBias = pd.concat([dfB, dfBias]).reset_index(drop=True)
                            # dfBias.reset_index(drop=True, inplace=True)

                        dfBias.reset_index(drop=True, inplace=True)

                    biasSet.update(word_bias)
                    

            dfBias.reset_index(drop=True, inplace=True)
            dfBias.fillna(0, inplace=True)
            # dfBias.to_csv(os.path.join(config.edaPath, 'word_bias.csv'), index=False)
            dfBias.to_csv(config.biasFile, index=False)

      
def  _test():
    df = pd.read_csv(config.preprocessFile)
    a = WordBIAS(df)
    common = a.get_common_each_aspect()
    process = a.preprocess_word_common()
    bias = a.get_proposed_bias()


if __name__ == '__main__':
    a = _test()



