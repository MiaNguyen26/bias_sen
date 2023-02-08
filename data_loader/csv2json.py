"""
    By: Mia Nguyen
    Date Created: 2023-02-07
    Date Modified: 2023-02-07, 5.45PM
    Description: convert generate samples (non-sense) to json file 
                and send to API to get the result; output is json file

"""
import numpy as np
import pandas as pd
import json
import os
from tqdm import tqdm
import requests
from configs import config

# csvPath = os.path.join(config.parentPath, "data", "sample_bias_uat8_9_10.csv")
# jsonPath = os.path.join(config.parentPath, "data", "sample_bias_uat8_9_10.json")
csvPath = os.path.join(config.parentPath, "data", "sample_common_uat8_9_10.csv")
jsonPath = os.path.join(config.parentPath, "data", "sample_common_uat8_9_10.json")


def csv2json():
    """
    Description: Convert csv file (generated samples - non sense) to json file
    """
    df = pd.read_csv(csvPath)
    column_list = df.columns.tolist()
    # print(column_list)
    dictFinal = []

    for header in column_list:
        sample_list = df[header].tolist()
        for idx, sample in tqdm(enumerate(sample_list)):        
            dict_sample = {}
            dict_sample['id'] = str(header + "_" + str(idx))
            dict_sample['text'] = sample
            dictFinal.append(dict_sample)

    with open(jsonPath, 'w', encoding='utf-8') as f:
        json.dump(dictFinal, f, indent=4, ensure_ascii=False)

        f.close()

def requests_json():
    """
    Description: Send json file to API and get the result
    """
    api_endpoint = 'http://10.124.68.77:9098/sentiment-analyzer'
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiQVBJIiwiaWF0IjoxNjUxODExOTE4LCJzZXJ2aWNlIjoic2VudGltZW50In0.E0p6r3YeMtPBgZ65K0xWsNgRXfTW-JtLd7GpqN_zl60'
    headers = {'X-API-Token': token}

    f = open(jsonPath, "r")
    data = json.load(f)
    outputPath = os.path.join(config.parentPath, "data", "predict_common_uat8_9_10.json")
    # for dt in data:
    #     res = requests.post(url = api_endpoint, data=json.dumps([dt]), headers= headers)
    #     output = res.text
    #     print(output)
    #     listFinal.append(list(output))
    # f.close()

    with open(outputPath, 'a+', encoding='utf-8') as file:
        for dt in tqdm(data):
            res = requests.post(url = api_endpoint, data=json.dumps([dt]), headers= headers)
            output = res.text
            # print(output)
            output = output[1:-1]
            file.write(output+'\n')
        
        file.close()
        


    # if res.status_code == 200 or res.status_code == 201:
    #     #success
    #     #code 
    #     pass
    #     print(res.txt)
    # else:
    #     #code
    #     #error
    #     pass




def _test():
    # csv2json()
    requests_json()

if __name__ == "__main__":
    _test()
    
  