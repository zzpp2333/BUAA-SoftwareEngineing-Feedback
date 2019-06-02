from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from scipy.linalg import norm
from jieba import analyse
import json

tfidf = analyse.extract_tags


class Similarity_function:
    def __init__(self, stopwords_file, questions):
        self.stf = stopwords_file
        self.ques = questions

        self.__init_getstopwords__()

    def __init_getstopwords__(self):
        with open(self.stf, encoding='UTF-8') as f: 
            self.stop_words = set([l.strip() for l in f])

    def getkeywords(self, str):
        #tfidf=analyse.extract_tags
        tfidf = analyse.textrank
        keywords = tfidf(str, 3, False,allowPOS=('n', 'i', 'l', 'nr', 'ns', 'nt', 'nz',))
        
        for keyword in keywords:
            if keyword in self.stop_words:
                keywords.remove(keyword)

        print("keywords:")
        for keyword in keywords:
            print (keyword + "/")
        print('\n')

    def getmostsimilar(self, quesid, str):
        def add_space(s):
            return ' '.join(list(s))

        threshold=0.5
        s1=add_space(str)
        lst=[]

        #with open(self.quf) as f: 
         #   self.questions = set([l.strip() for l in f])

        #strJson = self.data
        #print(strJson)

        for q in self.ques:
            if quesid == q['id']:
                continue
            s2 = add_space(q['title'])
            cv = TfidfVectorizer(tokenizer=lambda s: s.split())
            corpus = [s1, s2]
            vectors = cv.fit_transform(corpus).toarray()
            similarity=np.dot(vectors[0], vectors[1]) / (norm(vectors[0]) * norm(vectors[1]))
            if similarity > threshold:
                dic={}
                dic["id"]=q['id']
                dic["title"]=q['title']
                lst.append(dic)

        result = {"similar": []}
        result["similar"]=lst

        return result

#
# file = open('test.json', encoding='utf-8')
# simi_model = Similarity_function('hlp_stop_words.txt', json.load(file))
# simi_model.getkeywords("请问冒泡排序和快速排序在选用时有什么讲究？")
# print(simi_model.getmostsimilar("请问冒泡排序和快速排序在选用时有什么讲究？"))
