"""
    Description: This script converts the data from the original format to csv format.
    Input: txt file, json file, jsonl file, csv file (uat)
    Output: csv data input format
"""
import numpy as np
import pandas as pd
import os
import json
import argparse
from tqdm import tqdm

from configs import config



parser = argparse.ArgumentParser(description = 'Convert data to csv format')
# 4 types of dataset : 
# 1. RAW_TEXT : raw text file
# 2. JSON_GT : json file with ground truth
# 3. JSONL_MODEL : jsonl file with model prediction and ground truth
# 4. UAT (uat_results) : csv file with user annotation and ground truth
parser.add_argument('--dataName', type = str, default = 'uat8')
parser.add_argument('--dataType', type = str, default = 'UAT',
                    choices=['RAW_TEXT', 'JSON_GT', 'JSONL_MODEL', 'UAT'],
                     help = 'data name')

parser.add_argument('--dataPath', type = str, default = config.rawPath,
                    help = 'path to the data')

args = parser.parse_args()



class Convert2CSV():

    def __init__(self):
        self.dataName = args.dataName
        self.dataPath = args.dataPath
        self.save_path = os.path.join(config.parentPath, 'data', self.dataName + '.csv')

    def rawtext2csv(self):
        """
        Input: folder contains many text files. 
                Each file contains 100 ids and corresponding texts which are separated by "||"
        Return: a dataframe with all contents in txt files.
                This dataframe contains two columns: id and text
        """
        #get all txt file names
        txtFiles = os.listdir(self.dataPath)
        txtFiles.sort()

        df = pd.DataFrame()
        for fileName in txtFiles:
            filePath = os.path.join(self.dataPath, fileName)
            dfTXT = pd.read_csv(filePath, sep='\t', header=None, names=['text'])
            
            df = pd.concat([df,dfTXT], ignore_index=True)
        
        df.to_csv(self.save_path, index=False)

        return df

    def json2csv(self):
        """
        Input: json file contains text, id, ground truth aspects, etc.
        Return: a dataframe has 3 columns: id, text and corresponding aspect.
                Duplicating text (to new row) in case a text has multiple aspects.
        """
        file = open(self.dataPath)
        data = json.load(file)
        dfJSON = pd.json_normalize(data, meta =['id', 'text'], record_path=['labels'])
        
        # change the order of columns
        cols = dfJSON.columns.tolist()
        cols = cols[-2:]  + cols[:-2]
        df = dfJSON[cols].copy()

        #save df to csv
        df.to_csv(self.save_path, index=False)

        return df

    def jsonl2csv(self):
        """
        ----------- not done yet -----------
        Input: jsonl file contains text, id, ground truth aspects, model prediction aspects, etc.
        Return: a dataframe contains 4 columns: id, text, expected_aspect, predicted_aspect
                Duplicating text (to new row) in case a text has multiple aspects.
        """
        dataList = []
        with open(self.dataPath) as f:
            for line in f:
                data = json.loads(line)
                dataList.append(data)
        
        return dataList

    def uat2csv(self):
        """
        Input: csv file contains (predicted) aspect, aspect_polarity, category, date, 
                language, source, post_id, text, hotel_name
        Return: a dataframe which columns respectively id (post_id), hotel_name, date,
                language, aspect, aspect_polarity, category, text
        """
        df = pd.read_csv(self.dataPath)
        dfU = df.loc[:,['post_id', 'hotel_name', 'date', 'language', 'aspect', 'aspect_polarity', 'category', 'text']]
        dfU.to_csv(self.save_path, index=False)

        return dfU

def concat_df():
    df1 = pd.read_csv(os.path.join(config.parentPath, 'data/uat8.csv'))
    df2 = pd.read_csv(os.path.join(config.parentPath, 'data/uat9.csv'))
    df3 = pd.read_csv(os.path.join(config.parentPath, 'data/uat10.csv'))
    
    df = pd.concat([df1, df2, df3], ignore_index=False)
    df.to_csv(os.path.join(config.parentPath, 'data/uat_ver1.csv'), index=False)



def _test():
    data = args.dataType
    convert = Convert2CSV()

    if data == 'RAW_TEXT':
        df = convert.rawtext2csv()
    elif data == 'JSON_GT':
        df = convert.json2csv()
    elif data == 'JSONL_MODEL':
        df = convert.jsonl2csv()
    elif data == 'UAT':
        print('aaaa')
        df = convert.uat2csv()

    # concat_df()


if __name__ == '__main__':
    _test()






