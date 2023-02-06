"""
        Date Created: 2023-02-03
        Date Modified: 2023-02-03
        Description: Evaluate word bias method

"""
import numpy as np
import pandas as pd
import json
from tqdm import tqdm
import flatten_json as fj
import string
import os
import re
from tqdm import tqdm
import random
from collections import Counter
from pyvi import ViTokenizer

from configs import config

# vietnamese_patern = re.compile("["
    #    u"\U00C0 - \U1EF9"
    # "]+", flags=re.UNICODE)

viet_pattern = re.compile(r'[aàảãáạăằẳẵắặâầẩẫấậbcdđeèẻẽéẹêềểễếệfgh\
                        iìỉĩíịjklmnoòỏõóọôồổỗốộơờởỡớợpqrstuùủũúụưừửữứựvwx\
                        yỳỷỹýỵz]+')

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
    u"\u055A - \u070D"
    u"\u2019"

    "]+", flags=re.UNICODE)

class customDictionary():
    """
    Description: Create custom dictionary from craping data and save to txt file
    """

    def __init__(self):
        self.path = open(config.scrapFile)
        self.file = json.load(self.path)

    def create_dictionary(self):
        #---get all words in all comments:
        # df = pd.json_normalize(self.path)
        di = (fj.flatten(d) for d in self.file)
        df = pd.DataFrame(di)
        # print(df.head())
        val = list(df['h_comment'].unique())
        list_vocab = []
        new_vocab = []
        for st in val:
            st = st.translate(str.maketrans('', '', string.punctuation))
            list_vocab.extend(st.split())

        list_vocab = list(set(list_vocab))
        # print(list_vocab)
        # print(len(list_vocab))
        #file to save vocab
        f = open(os.path.join(config.parentPath, 'data', 'vocab.txt'), 'w')
        for word in list_vocab:
            word = emoji_pattern.sub(r'', word)
            if word.isdigit():
                continue
            if re.search(viet_pattern, word.lower()) is None:
                continue
            if word.isalpha() is False:
                continue

            new_vocab.append(word)
            f.write(word.lower() + '\n')
        f.close()

    def create_dictionary_freq(self):
        di = (fj.flatten(d) for d in self.file)
        df = pd.DataFrame(di)
        # print(df.head())
        val = list(df['h_comment'].unique())
        list_vocab = []
        new_vocab = []
        for st in val:
            st = st.translate(str.maketrans('', '', string.punctuation))
            st = ViTokenizer.tokenize(st)
            list_vocab.extend(st.split())
        
        #remove emoji
        list_vocab = [emoji_pattern.sub(r'', word) for word in list_vocab]
        #remove digit
        list_vocab = [word for word in list_vocab if word.isdigit() is False]
        list_vocab = [word for word in list_vocab if word.isalpha() is True]

        # print(len(list_vocab)) #443552 -> 95% = 421370
        # list_vocab = list(set(list_vocab)) #14780
        vocab_freq = Counter(list_vocab) #13445 words
        vocab_freq = vocab_freq.most_common(10000)

        #get vocab has freq >20
        f = open(os.path.join(config.parentPath, 'data', 'vocab_95.txt'), 'w')
        new_vocab = []
        for word in vocab_freq:
            if word[1] >= 20 and len(word[0])>1:
                new_vocab.append(word[0].lower())
                f.write(word[0].lower() + '\n')
        print(len(new_vocab))
        f.close()


class generateSample():

    """
    Description: Generate 100 samples for each bias
                Output: csv file with header is bias and each bias (header) has 100 rows respectively
    """

    def __init__(self):
        # -----get vocab to list
        self.vocab = open(os.path.join(config.parentPath, 'data', 'vocab_95.txt'),'r')
        self.vocab = self.vocab.read().splitlines()
        # print(len(self.vocab))

        # -----get bias list 
        self.biasdf = pd.read_csv(config.biasFile)
        self.biasList = self.biasdf['word_bias'].tolist()
        self.biasList = [word.replace('_',' ') for word in self.biasList]
        # print(self.biasList)

        # -----get list common words
        self.commonWord =[]
        self.commonFile = pd.read_csv(config.wordbiasFile, header=[0,1])
        aspects = self.commonFile.columns.levels[0].tolist()
        for aspect in aspects:
            words = self.commonFile[(aspect, 'common_words')].copy()
            words.dropna(how='all', inplace=True)
            words = words.tolist()
            words = [word.replace('_',' ') for word in words]

            self.commonWord = self.commonWord + words
        
        self.commonWord = list(set(self.commonWord))
        # print(len(self.commonWord))


    def generate_sample_bias(self, n=100):
        dfFinal = pd.DataFrame(columns=self.biasList)

        for idx1, bias in enumerate(self.biasList):
            #random length (number of words) of  n sentences for this bias
            len_sentence = np.array(np.random.randint(5,30, n))
            #loop over each sentence in this bias
            for idx2, length in enumerate(len_sentence):
                #randomly select n words from vocab
                words = random.sample([word for word in self.vocab if word not in self.biasList], int(length))
                words.append(bias)
                #reorder words in this sentence
                random.shuffle(words)
                #create sentence 
                sentence = ' '.join(words)
                dfFinal.loc[idx2, bias] = sentence

        dfFinal.reset_index(drop=True, inplace=True)
        dfFinal.to_csv(config.biasSample, index=False)


    def generate_sample_common(self, n=100):
        dfFinal = pd.DataFrame(columns=self.commonWord)

        for idx1, common in enumerate(self.commonWord):
            #random length (number of words) of  n sentences for this bias
            len_sentence = np.array(np.random.randint(5,30, n))
            #loop over each sentence in this bias
            for idx2, length in enumerate(len_sentence):
                #randomly select n words from vocab
                words = random.sample([word for word in self.vocab if word not in self.commonWord], int(length))
                words.append(common)
                #reorder words in this sentence
                random.shuffle(words)
                #create sentence 
                sentence = ' '.join(words)
                dfFinal.loc[idx2, common] = sentence

        dfFinal.reset_index(drop=True, inplace=True)
        dfFinal.to_csv(config.commonSample, index=False)


def _test():
    # vocab = customDictionary()
    # vocab.create_dictionary_freq()

    sample = generateSample()
    aa = sample.generate_sample_bias()
    a = sample.generate_sample_common()


if __name__ == '__main__':
    _test()

        

