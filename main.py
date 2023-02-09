import argparse
# from data_loader import convert2csv
from configs.config import GetArgs
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
parser.add_argument('--rawData', type = str, default = 'home/user/Desktop/review/data/predict_bias_uat8_9_10.json',
                    help = 'path to the data (model output)')
parser.add_argument('--freq_threshBias', type = int, default = 10, 
                    help = 'Frequency threshold for common words to find proposed bias')
parser.add_argument('--num_commonWord', type=int, default=100, 
                    help = "Number of common words to find for each aspect")
args = parser.parse_args()

params = GetArgs(dataName= args.dataName, freq_threshhold = args.freq_threshBias, num_commonWord = args.num_commonWord)

evaluate_bias._test()