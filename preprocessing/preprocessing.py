# -*- coding: utf-8 -*-
import os, sys
import pandas as pd
import numpy as np
import re
import string
import re
import pyvi
from pyvi import ViTokenizer, ViPosTagger, ViUtils

from configs import config

item_removal = ('', '...', '\n' )

#-----------convert all txt files to dataframe----------------
def txt2df():
    """
    Return: a dataframe with all contents in txt files - shape: (8569, 1)
    """
    #get all txt file names
    txtFiles = os.listdir(config.rawPath)
    txtFiles.sort()

    df = pd.DataFrame()
    for fileName in txtFiles:
        filePath = os.path.join(config.rawPath, fileName)
        dfTXT = pd.read_csv(filePath, sep='\t', header=None, names=['text'])
        
        df = pd.concat([df,dfTXT], ignore_index=True)
    
    return df

# -------------------preprocessing---------------------------
def preprocessing(dfPath):
    """
    Input: csv file (after data_loader)includes id, text (duplicate by number of aspects in that text), respectively aspect
    Return: a new dataframe contains numerous columns which are some preprocessing methods
            such as: tokenization, spacy tokenization, POS tagging, lowercase
    """
    df = pd.read_csv(dfPath)
    dfN = df.copy()

    # #tokenization
    # dfN['token'] = dfN['text'].apply(ViTokenizer.tokenize)
    # #space tokenization
    # dfN['spacy_token'] = dfN['text'].apply(lambda x: ViTokenizer.spacy_tokenize(x)[0])
    # #POS tagging token
    # dfN['pos'] = dfN['spacy_token'].apply(ViPosTagger.postagging_tokens)

    # #lowercase
    # dfN['lower'] = dfN['spacy_token'].apply(lambda x: [word.lower() for word in x])
   
    #tokenization
    dfN['token'] = [ViTokenizer.tokenize(text) for text in dfN['text']]

    #space tokenization
    dfN['spacy_token'] = [ViTokenizer.spacy_tokenize(text)[0] for text in dfN['text']]

    #POS tagging token
    # dfN['pos'] = [ViPosTagger.postagging_tokens(text) for text in dfN['spacy_token']]
    # dfN['pos'] = [ViPosTagger.postagging_tokens(text) for text in dfN['token']]

    #lowercase
    dfN['lower'] = [ [word.lower() for word in sentence] for sentence in dfN['spacy_token']]
    # dfN['lower'] = [ [word.lower() for word in sentence] for sentence in dfN['token']]

    #remove punctuation
    dfN['no_punc'] = [ [word for word in sentence if word not in string.punctuation] for sentence in dfN['lower']]
    
    #remove emoji
    dfN['no_emoji'] = [[config.emoji_pattern.sub(r'', word) for word in sentence] for sentence in dfN['no_punc']]
    
    #remove some specific characters
    dfN['processed'] = [[word for word in sentence if word not in item_removal] for sentence in dfN['no_emoji']]
    
    return dfN

def _test():
    # df = txt2df()
    # print(df.head())
    dfN = preprocessing(config.csvPath)
    print(dfN.head())

    #save to csv
    dfN.to_csv(config.preprocessFile, index=False)


if __name__ == '__main__':
    _test()
    