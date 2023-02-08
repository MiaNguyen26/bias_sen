import argparse
# from data_loader import convert2csv
from data_ana import evaluate_bias

parser = argparse.ArgumentParser(description = 'Convert data to csv format')
# 4 types of dataset : 
# 1. RAW_TEXT : raw text file
# 2. JSON_GT : json file with ground truth
# 3. JSONL_MODEL : jsonl file with model prediction and ground truth
# 4. UAT (uat_results) : csv file with user annotation and ground truth
parser.add_argument('--dataName', type = str, default = 'uat8910', help='data name')
parser.add_argument('--dataType', type = str, default = 'JSONL_MODEL',
                    choices=['RAW_TEXT', 'JSON_GT', 'JSONL_MODEL'],
                     help = 'data type')

parser.add_argument('--dataPath', type = str, default = config.rawPath,
                    help = 'path to the data')

args = parser.parse_args()

evaluate_bias._test()