#here is the default config file
import os
import datetime


now = datetime.datetime.now()
ttime = '{}{}_{}{}'.format(now.month, now.day, now.hour, now.minute)

#---------------- constant ---------------
# 26 aspects
listAspect = ['Dọn dẹp chung', 'An ninh', 'Dịch vụ bổ sung', 
            'Dọn dẹp nhà thầu', 'Dọn dẹp khác', 'Giá tiền khác', 'Giá tiền phòng', 
            'Ăn uống', 'Dọn dẹp phòng', 'Yếu tố khách quan', 'Dịch vụ khách sạn', 
            'Dịch vụ khác', 'An toàn/An toàn thực phẩm', 'Giá tiền chung', 
            'Tiêu phẩm', 'Tiện nghi/thoải mái chung', 'Thái độ nhân viên', 
            'Dịch vụ tiện ích', 'Khác', 'Đánh giá chung', 'Nghiệp vụ nhân viên', 
            'Giá tiền dịch vụ', 'Cơ sở vật chất khách sạn', 'Địa điểm', 
            'Nhân viên khác', 'Tốc độ dịch vụ']

#number of common words
num_common = 100


# -----------------Path to load data----------------
parentPath = '/home/user/Desktop/review'

#path of RAW data file
dataName = 'data_1k'
rawPath = os.path.join(parentPath, 'data/webanno_raw')
jsonFile = os.path.join(parentPath, 'data', dataName +'.json')

#path to save csv file
csvPath = os.path.join(parentPath,'data', dataName+'.csv')


#path of loading preprocessed data file
preprocessFile = os.path.join(parentPath, 'results/preprocess',
                                'preprocess_1226_1833.csv')




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


