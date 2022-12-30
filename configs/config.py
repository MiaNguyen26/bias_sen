#here is the default config file
import os
import datetime

from click import option


now = datetime.datetime.now()
ttime = '{}{}_{}{}'.format(now.month, now.day, now.hour, now.minute)

#---------------- constant ---------------
num_common = 100
num_sample = 300
# 26 aspects
listAspect = ['Dọn dẹp chung', 'An ninh', 'Dịch vụ bổ sung', 
            'Dọn dẹp nhà thầu', 'Dọn dẹp khác', 'Giá tiền khác', 'Giá tiền phòng', 
            'Ăn uống', 'Dọn dẹp phòng', 'Yếu tố khách quan', 'Dịch vụ khách sạn', 
            'Dịch vụ khác', 'An toàn/An toàn thực phẩm', 'Giá tiền chung', 
            'Tiêu phẩm', 'Tiện nghi/thoải mái chung', 'Thái độ nhân viên', 
            'Dịch vụ tiện ích', 'Khác', 'Đánh giá chung', 'Nghiệp vụ nhân viên', 
            'Giá tiền dịch vụ', 'Cơ sở vật chất khách sạn', 'Địa điểm', 
            'Nhân viên khác', 'Tốc độ dịch vụ']

listEAspect = ['GENERAL', 'PRICE_GENERAL', 'PRICE_ROOM', 'PRICE_OTHER', 'PRICE_SERVICE',
                'FOOD_AND_BEVERANGE', 'CLEANLINESS_GENERAL', 'CLEANLINESS_INHOUSE', 'CLEANLINESS_CONTRACTOR',
                'CLEANLINESS_OTHER', 'LOCATION', 'SERVICE_ADDITIONAL', 'SERVICE_OTHER', 'SERVICE_HOTEL',
                'STAFF_ATTITUDE', 'STAFF_SPEED', 'STAFF_OTHER','STAFF_SKILL',
                'ACCOMODATION_GENERAL', 'ACCOMODATION_MAINTENANCE', 'ACCOMODATION_AMENTIES',
                'ACCOMODATION_UTILITIES', 'OTHER_OBJECTIVE']



# -----------------Path to load data----------------
parentPath = '/home/user/Desktop/review'
#path of RAW data file
dataName = 'data_1k'
rawPath = os.path.join(parentPath, 'data/webanno_raw')
jsonFile = os.path.join(parentPath, 'data', dataName +'.json')
jsonlFile = os.path.join(parentPath, 'data', 'data_pred_check' +'.jsonl')
# jsonlFile = os.path.join(parentPath, 'data', 'test' +'.jsonl')

#path to save data.csv file
csvPath = os.path.join(parentPath,'data', dataName+'.csv')


#path of loading preprocessed data file
preprocessFile = os.path.join(parentPath, 'results/preprocess',
                                'preprocess_1226_1833.csv')

#path for Data Augmentation
positiveFile = os.path.join(parentPath,'data/augmentation' , 'positive.txt')
negativeFile = os.path.join(parentPath,'data/augmentation' , 'negative.txt')
linkingFile = os.path.join(parentPath,'data/augmentation' , 'linking.txt')




#-------------Path to save result----------------


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

#path of vocab file
vocabFile = os.path.join(parentPath, 'results/eda/1216_1545', 'vocab.csv')
#path of processed file
processedFile = os.path.join(parentPath, 'results/eda/1216_1545', 'processed.csv')

#path to save data augmentation result
augmentFolder = os.path.join(parentPath, 'results/augmentation')
augmentPath = os.path.join(augmentFolder, ttime)
if not os.path.exists(augmentPath):
    os.makedirs(augmentPath)


