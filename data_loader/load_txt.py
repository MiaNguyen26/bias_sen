import pandas as pd
import numpy as np

from configs import config

#-----------convert all txt files to dataframe----------------
def txt2df():
    """
    Return: a dataframe with all contents in txt files - shape: (8569, 1)
    """
    #get all txt file names
    txtFiles = os.listdir(config.rawPath)
    txtFiles.sort()

    df = pd.DataFrame()
    for fileName in txtFiles:
        filePath = os.path.join(config.rawPath, fileName)
        dfTXT = pd.read_csv(filePath, sep='\t', header=None, names=['text'])
        
        df = pd.concat([df,dfTXT], ignore_index=True)
    
    df.to_csv(config.csvPath, index=False)
    
    return df