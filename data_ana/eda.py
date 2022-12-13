"""
This module contains the EDA class, which is the main class for the EDA
module. It contains the following methods:
Sentiment Analysis, Word Count, Word Common

"""
import warnings
# warnings.simplefilter("always")
warnings.filterwarnings('ignore', category=DeprecationWarning)

from distutils.version import LooseVersion
from packaging import version
import seaborn as sns
from operator import mod 

# LooseVersion(sns.__version__)
# version.parse(sns.__version__)
# version.Version(sns.__version__)

# # currently:
# if LooseVersion(mod.__version__) < LooseVersion(minversion):
#     pass

# # options:
# if version.parse(mod.__version__) < version.parse(minversion):
#     pass

# if version.Version(mod.__version__) < version.Version(minversion):
#     pass

# if Version(mod.__version__) < Version(minversion):
#     pass

import os 
import ast
import pandas as pd
import numpy as np
# import nltk
import pickle
# import pyLDAvis.sklearn
from collections import Counter
from textblob import TextBlob
# from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.decomposition import LatentDirichletAllocation, NMF
# from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt


from configs import config

class EDA:
    def __init__(self, df):
        self.df = df
        self.dfN = self.df.copy()
        self.dfN['process_str'] = [' '.join(ast.literal_eval(wordList)) for wordList in self.df['processed']]
        # self.dfN['process_str'] = [''.join(map(str,l)) for l in self.dfN['processed']]


    def sentiment_analysis(self):
        """
        Return: a new dataframe contains the sentiment analysis of each sentence
        """
        # self.dfN['sentiment'] = self.dfN['process_str'].apply(lambda x: TextBlob(x).sentiment)
        self.dfN['sentiment'] = [TextBlob(sentence).sentiment.polarity for sentence in self.dfN['process_str']]
        return self.dfN

    def word_count(self):
        """
        Return: a new dataframe contains the word count of each sentence
        """
        self.dfN['word_count'] = self.dfN['processed'].apply(lambda x: len(str(x).split()))
        self.dfN['review_len'] = self.dfN['process_str'].astype(str).apply(len)
        return self.dfN

    def word_common(self, num):
        """
        Return: a new dataframe contains the 100 most common words
        """
        words = self.dfN['processed']
        allwords =[]
        for wordlist in words:
            wordList = ast.literal_eval(wordlist)
            allwords += wordList
        
        print(allwords[:10])
        mostcommon = FreqDist(allwords).most_common(num)
        # x, y = zip(*mostcommon)
        return mostcommon

    def count_vectorizer(self):
        tf_vectorizer = CountVectorizer( max_features=20, ngram_range=(2,2))
        tf = tf_vectorizer.fit_transform(self.dfN['process_str'].values.astype('U'))
        tf_feature_names = tf_vectorizer.get_feature_names_out()
        doc_term_matrix = pd.DataFrame(tf.toarray(), columns=list(tf_feature_names))
        doc_term_matrix.to_csv(os.path.join(config.edaPath, 'count_vectorizer.csv'))
        return doc_term_matrix

    def tfidf_vectorizer(self):
        tfidf_vectorizer = TfidfVectorizer(max_df=0.90, min_df =25, max_features=100, use_idf=True)
        tfidf = tfidf_vectorizer.fit_transform(self.dfN['process_str'])
        tfidf_feature_names = tfidf_vectorizer.get_feature_names_out()
        doc_term_matrix_tfidf = pd.DataFrame(tfidf.toarray(), columns=list(tfidf_feature_names))
        doc_term_matrix_tfidf.to_csv(os.path.join(config.edaPath, 'tfidf_vectorizer.csv'))
        return doc_term_matrix_tfidf

def _test():
    df = pd.read_csv(config.preprocessFile)
    # print(df.head())
    eda = EDA(df)
    dfN = eda.sentiment_analysis()
    dfN = eda.word_count()
    mostcommon = eda.word_common(25)
    # print(dfN.head(10))
    print(mostcommon)


if __name__ == '__main__':
    _test()
    

      
    
        