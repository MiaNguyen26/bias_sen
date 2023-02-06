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

from configs import config

# vietnamese_patern = re.compile("["
    #    u"\U00C0 - \U1EF9"
    # "]+", flags=re.UNICODE)

viet_pattern = re.compile(r'[aàảãáạăằẳẵắặâầẩẫấậbcdđeèẻẽéẹêềểễếệfghiìỉĩíịjklmnoòỏõóọôồổỗốộơờởỡớợpqrstuùủũúụưừửữứựvwxyỳỷỹýỵz]+')
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
        # print(new_vocab)
        # print(len(new_vocab))


class generateSample():
    """
    Description: Generate 100 samples for each bias
                Output: csv file with header is bias and each bias (header) has 100 rows respectively
    """
    def __init__(self):
        # get vocab to list
        self.vocab = open(os.path.join(config.parentPath, 'data', 'vocab.txt'),'r')
        self.vocab = self.vocab.read().splitlines()
        # print(len(self.vocab))

        # get bias list (to header)
        self.biasList = pd.read_csv(config.biasFile)







def _test():
    # vocab = customDictionary()
    # vocab.create_dictionary()

    sample = generateSample()


if __name__ == '__main__':
    _test()

        

