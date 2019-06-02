from aip import AipNlp
from classify.utils import const
import codecs
import pandas as pd
import time

LENGTH = 2048 #字节

APP_ID = '15970320'
API_KEY = 'POiFaoRBForD1dFxZ4Mcvi4O'
SECRET_KEY = 'bstyECSVyjyoRXSisOyk1bfj2pod2Erz'

client = AipNlp(APP_ID,API_KEY,SECRET_KEY)

def truncate(text):
    if len(text) > LENGTH/6:
        text = text.replace(' ','')
        return text[0:(int)(LENGTH/6)]
    else:
        return text

def get_by_text(text):
    try:
        result = client.sentimentClassify(truncate(text))
    except UnicodeEncodeError:
        text = text.encode('gbk','ignore').decode('gbk')
        #print(text)
        result = client.sentimentClassify(truncate(text))

    try:
        ret = result['items'][0]['sentiment']
        if  ret == 0:
            # return const._NEG_EMOTION
            return -1
        elif ret == 1:
            # return const._NEU_EMOTION
            return 0
        else:
            # return const._POS_EMOTION
            return 1
    except KeyError:
        print(">>error occurred while dealing with "+result)
        # return const._ERR_EMOTION
        return 0

def get_by_list(textlist):
    resultlist = []
    for text in textlist:
        time.sleep(0.20)
        resultlist.append(get_by_text(text))
    return resultlist

def read_raw(path):
    with codecs.open(path,'r','utf-8') as f:
        df = pd.read_csv(f).astype(str)
    comment = df[const._COMMENT_COLUMN].tolist()
    df[const._EMO_COLUMN] = get_by_list(comment)
    save_path = './rawdata/_emotion_label.csv'
    df.to_csv(save_path,index=False,encoding='utf-8')

if __name__ == '__main__':
    read_raw('./rawdata/_comm_clean.csv')