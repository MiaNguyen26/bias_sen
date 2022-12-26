import json
import numpy as np
import os
import pandas as pd

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

        #save df to csv
        dfN.to_csv(config.csvPath, index=False)
        
        return dfN

        

def _test():
    JSONProcess = json_processing()
    a = JSONProcess.convert_json2csv()




if __name__ == '__main__':
    _test()
    # get_list_aspect()