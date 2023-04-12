"""
        Date Created: 2023-02-03
        Date Modified: 2023-02-03
        Author: Mia Nguyen
        Description:- Creat custom dictionary from scarping data 
                        output: txt file
                    - Generate non-sense samples from custom dictionary
                        output: json file (for model input)
                    - Evaluate word bias method

"""
import numpy as np
import pandas as pd
import json
from tqdm import tqdm
import flatten_json as fj
import string
import os
import re
import requests
from tqdm import tqdm
import random
from collections import Counter
from pyvi import ViTokenizer
import matplotlib.pyplot as plt

from configs import config


# viet_pattern = re.compile(r'[aàảãáạăằẳẵắặâầẩẫấậbcdđeèẻẽéẹêềểễếệfgh\
                        # iìỉĩíịjklmnoòỏõóọôồổỗốộơờởỡớợpqrstuùủũúụưừửữứựvwx\
                        # yỳỷỹýỵz]+')


class Vocab():
    """
    Description: Create custom dictionary from craping data and save to txt file
    Input: scraping data (json format)
    Output: txt file. Each line is a word in dictionary
    """

    def __init__(self):
        self.path = open(config.scrapFile)
        self.file = json.load(self.path)

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
        list_vocab = [config.emoji_pattern.sub(r'', word) for word in list_vocab]
        #remove digit
        list_vocab = [word for word in list_vocab if word.isdigit() is False]
        list_vocab = [word for word in list_vocab if word.isalpha() is True]

        # print(len(list_vocab)) #443552 -> 95% = 421370
        # list_vocab = list(set(list_vocab)) #14780
        vocab_freq = Counter(list_vocab) #13445 words
        vocab_freq = vocab_freq.most_common(10000)

        #get vocab has freq >20
        f = open(config.dictionaryFile, 'w')
        new_vocab = []
        for word in vocab_freq:
            if word[1] >= 20 and len(word[0])>1:
                new_vocab.append(word[0].lower())
                f.write(word[0].lower() + '\n')
        print(len(new_vocab))
        f.close()


class GenerateSample():

    """
    Description: Generate 100 samples for each bias
                Output: 
                json file in this following format
                [
                    {
                        "id": "0",
                        "text": "Thái độ"
                ]
                or csv file with header is bias and each bias (header) has 100 rows respectively
    """

    def __init__(self):
        # -----get vocab to list
        self.vocab = open(config.dictionaryFile,'r')
        self.vocab = self.vocab.read().splitlines()
        # print(len(self.vocab))

        # -----get bias list 
        self.biasdf = pd.read_csv(config.biasFile)
        self.biasList = self.biasdf['word_bias'].tolist()
        self.biasList = [word.replace('_',' ') for word in self.biasList]
        # print(len(self.biasList)) # 77 proposed bias

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
        # print(len(self.commonWord)) # 143 commonwords


    def generate_sample_bias(self, n=100):
        """
            Description: Generate n samples for each bias

        """
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
        #-------save to csv output
        # dfFinal.to_csv(config.biasSample, index=False)
        # -------- save to json output
        dictFinal = []
        column_list = dfFinal.columns.tolist()

        for header in column_list:
            sample_list = dfFinal[header].tolist()
            for idx, sample in tqdm(enumerate(sample_list)):        
                dict_sample = {}
                dict_sample['id'] = str(header + "_" + str(idx))
                dict_sample['text'] = sample
                dictFinal.append(dict_sample)

        with open(config.biasSample, 'w', encoding='utf-8') as f:
            json.dump(dictFinal, f, indent=4, ensure_ascii=False)
            f.close()


    def generate_sample_common(self, n=100):
        #path to save other common (except bias) non-sense samples
        commonPart = os.path.join(config.parentPath, 'data', 'sample_part_common.json')
        dfFinal = pd.DataFrame()
        count_others = 0
        count_bias = 0
        for idx1, common in tqdm(enumerate(self.commonWord)):
            if common in self.biasList:
                count_bias += 1
                continue
            else:
                count_others += 1
                #random length (number of words) of  n sentences for this bias
                len_sentence = np.array(np.random.randint(5,30, n))
                #loop over each sentence in this bias
                for idx2, length in enumerate(len_sentence):
                    #randomly select n words from vocab
                    words = random.sample([word for word in self.vocab if (word not in self.commonWord) and (word not in self.biasList)], int(length))
                    words.append(common)
                    #reorder words in this sentence
                    random.shuffle(words)
                    #create sentence 
                    sentence = ' '.join(words)
                    dfFinal.loc[idx2, common] = sentence

        dfFinal.reset_index(drop=True, inplace=True)
        # dfFinal.to_csv(os.path.join(config.parentPath, 'data', 'sample_common_uat.csv'), index=False)
        #save to json output
        dictFinal = []
        column_list = dfFinal.columns.tolist()
        # print(dfFinal.shape[0])
        # print('count_others: ', count_others)
        # print('len(column_list): ', count_others+ count_bias)

        for header in column_list:
            sample_list = dfFinal[header].tolist()
            for idx, sample in tqdm(enumerate(sample_list)):        
                dict_sample = {}
                dict_sample['id'] = str(header + "_" + str(idx))
                dict_sample['text'] = sample
                dictFinal.append(dict_sample)

        # with open(config.commonSample, 'w', encoding='utf-8') as f:
        with open(commonPart, 'w', encoding='utf-8') as f:
            json.dump(dictFinal, f, indent=4, ensure_ascii=False)
            f.close()


        #----- merge two json files = (proposed) bias samples + (common - bias)samples
        files = [config.biasSample, commonPart]
        commonFinal = []
        for file in files:
            with open(file, 'r', encoding='utf-8') as infile:
                commonFinal.extend(json.load(infile))
        
        with open(config.commonSample, 'w', encoding='utf-8') as commonFile:
            json.dump(commonFinal, commonFile, indent=4, ensure_ascii=False)
            commonFile.close()


class Predict():
    def __init__(self):
        self.biasInput = config.biasSample
        self.biasPredict = config.biasPredict
        self.commonInput = config.commonSample
        self.commonPredict = config.commonPredict
    
    def requests_json_bias(self):
        """
        Description: Send json file to API and get the result for proposed bias words
        """
        api_endpoint = 'http://10.124.68.77:9098/sentiment-analyzer'
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiQVBJIiwiaWF0IjoxNjUxODExOTE4LCJzZXJ2aWNlIjoic2VudGltZW50In0.E0p6r3YeMtPBgZ65K0xWsNgRXfTW-JtLd7GpqN_zl60'
        headers = {'X-API-Token': token}

        f = open(self.biasInput, "r")
        data = json.load(f)

        with open(self.biasPredict, 'a+', encoding='utf-8') as file:
            for dt in tqdm(data):
                res = requests.post(url = api_endpoint, data=json.dumps([dt]), headers= headers)
                output = res.text
                # print(output)
                output = output[1:-1]
                file.write(output+'\n')
            
            file.close()

    def requests_json_common(self):
        """
        Description: Send json file to API and get the result for common words
        """
        api_endpoint = 'http://10.124.68.77:9098/sentiment-analyzer'
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiQVBJIiwiaWF0IjoxNjUxODExOTE4LCJzZXJ2aWNlIjoic2VudGltZW50In0.E0p6r3YeMtPBgZ65K0xWsNgRXfTW-JtLd7GpqN_zl60'
        headers = {'X-API-Token': token}

        f = open(self.commonInput, "r")
        data = json.load(f)

        with open(self.commonPredict, 'a+', encoding='utf-8') as file:
            for dt in tqdm(data):
                res = requests.post(url = api_endpoint, data=json.dumps([dt]), headers= headers)
                output = res.text
                # print(output)
                output = output[1:-1]
                file.write(output+'\n')
            
            file.close()

    def json2csv(self, input):
        """
        Input: jsonl file (model output) contains text, id, ground truth aspects, model prediction aspects, etc.
        Return: a dataframe contains 4 columns: id, text, expected_aspect, predicted_aspect
                #NOTICE: set path to save that dataframe
        """
        dataList = []
        with open(input) as f:
            for line in f:
                #get all data as a list of dictionaries
                data = json.loads(line)
                dataList.append(data)

        dfJSONL = pd.DataFrame(columns=['id', 'text', 'aspect'])
        #extract each dictionary in the list
        for data in tqdm(dataList):
            #get id, text, aspect
            id = data['id']
            text = data['text']
            aspects = [data['aspects'].keys()]
            #create sub df to concat to main df
            for aspect in aspects:
                df = pd.DataFrame({'id': id, 'text': text, 'aspect': aspect})
                dfJSONL = pd.concat([dfJSONL, df], ignore_index=True)

        #save df to csv
        dfJSONL.reset_index(drop=True, inplace=True)
        dfJSONL.to_csv(os.path.join(config.parentPath, 'data', 'predict_bias_uat'+ '.csv'), index=False)     
        return dataList


class Evaluate():
    """
    Description: Evaluate the model, get Precision and Recall
    """
    def __init__(self):
        self.biasPredict = config.biasPredict
        self.commonPredict = config.commonPredict


    def metrics(self):

        dataList1 = []
        count_actual = 0
        count_FP = 0
        count_allbias = 0 

        with open(self.biasPredict) as f1:
        # with open('/home/user/Desktop/review/data/test.json', 'r') as f1:
            for line in f1:
                #get all data as a list of dictionaries
                data = json.loads(line)
                dataList1.append(data)
        f1.close()

        dfBias = pd.DataFrame(columns=['proposed_bias', 'precision'])
        #dictBias with key is bias name, value is a list of [TP (actual bias), FP]
        dictBias = {}

        #extract each dictionary in the list
        for data in dataList1:
            #get id, text, aspect
            id1 = data['id']
            # text = data['text']
            aspects = list(data['aspects'].keys())
            # print(aspects)

            #get name of this bias
            this_bias = id1.split('_')[0]
            #check if this bias in the dictBias
            if this_bias not in dictBias:
                dictBias[this_bias] = [0, 0]

            if aspects == ['OTHER']:
                dictBias[this_bias][1] += 1
                count_FP += 1
            else:
                dictBias[this_bias][0] += 1
                count_actual += 1

                

        #calculate precision and recall for each bias
        for bias in dictBias:
            precision = dictBias[bias][0] / (dictBias[bias][0] + dictBias[bias][1])
            df_thisBias = pd.DataFrame([{'proposed_bias': bias, 'precision': precision}])
            dfBias = pd.concat([dfBias, df_thisBias], ignore_index=True)
        
        dfBias.reset_index(drop=True, inplace=True)
        dfBias.to_csv(os.path.join(config.parentPath, 'data', 'precision_bias'+ '.csv'), index=False)
        
        dataList2 = []
        #get all actual bias from common list
        with open(self.commonPredict) as f2:
            for line in f2:
                #get all data as a list of dictionaries
                data = json.loads(line)
                dataList2.append(data)
        f2.close()
        
        #extract each dictionary in the list
        for data in dataList2:
            #get id, text, aspect
            id = data['id']
            text = data['text']
            aspects = list(data['aspects'].keys())

            #get all actual bias = 'OTHERS'
            if aspects != ['OTHER']:
                count_allbias += 1
        
        #calculate precision and recall
        precision = count_actual/(count_actual + count_FP)
        recall = count_actual/count_allbias

        return precision, recall


class Graph_bias():
    def __init__(self):
        self.biasPrecisionPath = os.path.join(config.parentPath, 'data', 'precision_bias'+ '.csv')

    def graph_precision(self):
        df = pd.read_csv(self.biasPrecisionPath)
        df = df.sort_values(by=['precision'], ascending=False)

        figure = plt.figure(figsize=(50,30))
        plt.bar(df['proposed_bias'].tolist(), df['precision'].tolist(), color='blue')
        plt.title('Precision of each proposed bias', fontsize=50, color='g')
        plt.xticks(rotation=90, fontsize=16)
        plt.yticks(fontsize=40)
        plt.xlabel('Proposed Bias', labelpad=100, fontsize=40)
        plt.ylabel('Precision', labelpad=100, fontsize=40)
        plt.grid(axis='y', linestyle='--')
        plt.savefig(os.path.join(config.parentPath,'data', 'precision_bias.png'))



def _test():
    # vocab = Vocab()
    # vocab.create_dictionary_freq()

    # sample = GenerateSample()
    # aa = sample.generate_sample_bias()
    # a = sample.generate_sample_common()

    # predict = Predict()
    # predict.requests_json_common()
    # predict.json2csv(config.biasPredict)

    # eva = Evaluate()
    # precision, recall = eva.metrics()
    # print(precision, recall)

    graph = Graph_bias()
    graph.graph_precision()



if __name__ == '__main__':
    _test()

        

