#here is the default config file
import os
import datetime

# from click import option


now = datetime.datetime.now()
ttime = '{}{}_{}{}'.format(now.month, now.day, now.hour, now.minute)


#---------------- constant ---------------
num_common = 100
num_sample = 300
freq_threshold = 10
dataName = 'uat8_9_10'
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


word_common = ['common_word', 'frequency', 'percentage', 'char_count']


# -----------------Path to load data----------------

parentPath = '/home/user/Desktop/review'

#-----path for processed file
#common words file
commonFile = os.path.join(parentPath, 'data', 'common_words_each_aspect_'+ dataName+'.csv')
#word_bias preprocessed file
wordbiasFile = os.path.join(parentPath, 'data', 'word_bias_preprocess_'+ dataName+ '.csv')
#word_bias file
biasFile = os.path.join(parentPath, 'data', 'word_bias_'+ dataName+'.csv')
#scrapped data file to create dictionary
scrapFile = os.path.join(parentPath, 'data', 'crawl_data', 'tripadvisor.json')

#-----path of stopword file
stopwordFile = os.path.join(parentPath, 'data/stopwords.txt')

#-----path of RAW data file
rawPath = os.path.join(parentPath, 'data/uat_results (10).csv')
#path of csv (after converted path)
csvPath = os.path.join(parentPath, 'data/raw_data', 'dict.csv')

#path of loading preprocessed data file
preprocessFile = os.path.join(parentPath, 'results/preprocess',
                                    'preprocess_113_1045.csv')
                                # 'preprocess_112_1823.csv')

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
graphPath = os.path.join(graphFolder, ttime+ '_'+ dataName)


#path to save eda result
edaFolder = os.path.join(parentPath, 'results/eda')
edaPath = os.path.join(edaFolder, ttime+'_'+dataName)

#path of vocab file
vocabFile = os.path.join(parentPath, 'results/eda/1216_1545', 'vocab.csv')
#path of processed file
processedFile = os.path.join(parentPath, 'results/eda/1216_1545', 'processed.csv')

#path to save data augmentation result
augmentFolder = os.path.join(parentPath, 'results/augmentation')
augmentPath = os.path.join(augmentFolder, ttime)



