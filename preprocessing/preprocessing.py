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

emoji_pattern = re.compile("["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    u"\U00002500-\U00002BEF"  # chinese char
    u"\U00002702-\U000027B0"
    u"\U00002702-\U000027B0"
    u"\U000024C2-\U0001F251"
    u"\U0001f926-\U0001f937"
    u"\U00010000-\U0010ffff"
    u"\u2640-\u2642"
    u"\u2600-\u2B55"
    u"\u200d"
    u"\u23cf"
    u"\u23e9"
    u"\u231a"
    u"\ufe0f"  # dingbats
    u"\u3030"
    u"\u2665"
    "]+", flags=re.UNICODE)

item_removal = ('', '...' )

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
    Return: a new dataframe contains numerous columns which are some preprocessing methods
            such as: tokenization, spacy tokenization, POS tagging, lowercase
    """
    df = pd.read_csv(dfPath)
    dfN = df.copy()

    #accent marks removal
    # dfN['no_accent'] = dfN['no_punc'].apply(lambda x: ViUtils.remove_accents(x).encode('utf-8'))
    #accent marks adding
    # dfN['accent'] = dfN['text'].apply(lambda x: ViUtils.add_accents(x))
    # print(dfN.head())

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
    dfN['pos'] = [ViPosTagger.postagging_tokens(text) for text in dfN['spacy_token']]
    # dfN['pos'] = [ViPosTagger.postagging_tokens(text) for text in dfN['token']]

    #lowercase
    dfN['lower'] = [ [word.lower() for word in sentence] for sentence in dfN['spacy_token']]
    # dfN['lower'] = [ [word.lower() for word in sentence] for sentence in dfN['token']]

    #remove punctuation
    dfN['no_punc'] = [ [word for word in sentence if word not in string.punctuation] for sentence in dfN['lower']]
    
    #remove emoji
    dfN['no_emoji'] = [[emoji_pattern.sub(r'', word) for word in sentence] for sentence in dfN['no_punc']]
    
    #remove some specific characters
    dfN['processed'] = [[word for word in sentence if word not in item_removal] for sentence in dfN['no_emoji']]
    
    return dfN

def _test():
    # df = txt2df()
    # print(df.head())
    dfN = preprocessing(config.csvPath)
    print(dfN.head())

    #save to csv
    dfN.to_csv(config.preprocessPath, index=False)


if __name__ == '__main__':
    _test()
    