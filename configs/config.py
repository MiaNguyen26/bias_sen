#here is the default config file
import os
import datetime
now = datetime.datetime.now()
ttime = '{}{}_{}{}'.format(now.month, now.day, now.hour, now.minute)

parentPath = '/home/user/Desktop/review'

#path of txt data file
rawPath = os.path.join(parentPath, 'data/webanno_raw')

#path of loading preprocessed data file
preprocessFile = os.path.join(parentPath, 'results/preprocess',
                                'preprocess_1212_1212.csv')


#path to save preprocessed data file
preprocessName = 'preprocess_{}{}_{}{}.csv'.format(now.month, now.day, now.hour, now.minute)
preprocessPath = os.path.join(parentPath, 'results/preprocess', preprocessName)

#path to save graph
graphFolder = os.path.join(parentPath, 'results/graph')
graphPath = os.path.join(graphFolder, ttime)

if not os.path.exists(graphPath):
    os.makedirs(graphPath)

#path to save eda result
edaFolder = os.path.join(parentPath, 'results/eda')
edaPath = os.path.join(edaFolder, ttime)
if not os.path.exists(edaPath):
    os.makedirs(edaPath)