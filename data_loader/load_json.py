import json
import numpy as np
import os
import pandas as pd
import xlsxwriter
from tqdm import tqdm

from configs import config

class json_processing():
    def __init__(self):
        self.file = open(config.jsonFile)
        self.data = json.load(self.file)

        
    def get_list_aspect(self):
        list_aspect = []
        for idx1, content in enumerate(self.data):
            for idx2, label in enumerate(content['labels']):
                list_aspect.append(label['aspect'])
        
        list_aspect = list(set(list_aspect))
        # print(list_aspect)

        return list_aspect


    def json2csv(self):
        df = pd.json_normalize(self.data, meta =['id', 'text'], record_path=['labels'])
        
        # change the order of columns
        cols = df.columns.tolist()
        cols = cols[-2:]  + cols[:-2]
        dfN = df[cols]

        #output file
        csvFile = str(input("Enter the name of csv file: "))
        csvPath = os.path.join(config.parentPath,'data/raw_data', csvFile+'.csv')

        #save df to csv
        dfN.to_csv(csvPath, index=False)
        
        return dfN


class jsonl_processing():
    def __init__(self):
        # self.file = open(config.jsonlFile, 'r')
        # self.lines = list(self.file)
        # self.data =[]
        # for json_str in self.lines:
        #     data = json.loads(json_str)
        #     self.data.append(data)
        self.data = []
        with open(config.jsonlFile) as f:
            # f = list(f)
            for line in f:
                data = json.loads(line)
                self.data.append(data)
        # print(self.data)

        
    def get_list_id(self):
        idList = []
        for idx1, content in enumerate(self.data):
            idList.append(content["id"])

        # print(idList)
        # workbook = xlsxwriter.Workbook('check_pred_10k.xlsx')
        # worksheet = workbook.add_worksheet()
        # worksheet.write_column('A1', idList)
        # workbook.close()

        return idList

    def compare_gt_pred(self):
        gt_text =  []
        pred_text = []
        # count = 0
        result = []
        idList = []
        for idx1, content in enumerate(tqdm(self.data)):

            #--- into each review
            idList.append(content["id"])

            #get list of text gt 
            for idx2, text in enumerate(content["entity_spans"]):
                gt_text.append(text['text'].lower())
            
            #get list of text pred
            for idx3, text in enumerate(content["entity_spans_pred"]):
                pred_text.append(text['text'].lower())

            # print('gt==' , gt_text)
            # print('pred==', pred_text)

            #compare gt vs. pred
            count = 0
            sum = len(gt_text)
            for idx4, gt in enumerate(gt_text):
                for idx5, pred in enumerate(pred_text):
                    if gt in pred or pred in gt:
                        count += 1
            
            if count == sum:
                result.append('True')
            else:
                result.append(f'{count}/{sum}')
            
        workbook = xlsxwriter.Workbook(os.path.join(config.parentPath, 'results','compare.xlsx'))
        worksheet = workbook.add_worksheet()
        worksheet.write_column('A1', idList)
        worksheet.write_column('B1', result)
        workbook.close()
    
        return result
            


def _test():
    JSONProcess = json_processing()
    a = JSONProcess.json2csv()

    # JSONL = jsonl_processing()
    # a = JSONL.compare_gt_pred()
    # print('ma === ', a.count('True'))




if __name__ == '__main__':
    _test()
    # get_list_aspect()