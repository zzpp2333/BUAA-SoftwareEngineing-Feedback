from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.externals import joblib

from classify.Data_Env import Data_Env_Base
from classify.utils import const

class Classification_Base:
    def __init__(self, dataenv, **options):

        try: #模式为训练还是测试
            self.mode = options['mode']
        except KeyError:
            self.mode = 'train'

        try: #模式为训练还是测试
            self.model_save = options['enable_model_saver']
        except KeyError:
            self.model_save = True
        try:
            self.save_path = options["save_model_path"]
        except KeyError:
            self.save_path = None

        self.data_env = dataenv

        self.labels = self.data_env.df_labels[const._LABEL_COLUMN]

        self.vector = self.data_env.vector
        self.tfidf = self.data_env.tf_idf

        self.StandardScale()
        self.get_separation()

    def StandardScale(self):
        self.encoder = preprocessing.LabelEncoder()
        self.corpus_encode_label = self.encoder.fit_transform(self.labels)

    def get_separation(self):
        sepa = self.data_env.get_separation(self.tfidf,self.corpus_encode_label)
        self.train_set = sepa['x_train']
        self.test_set = sepa['x_test']
        self.val_set = sepa['x_val']

        self.train_label = sepa['y_train']
        self.test_label = sepa['y_test']
        self.val_label = sepa['y_val']

    def train(self):
        self.lr_model = LogisticRegression()
        self.lr_model.fit(self.train_set,self.train_label)

        print("val mean accuracy: {0}".format(self.lr_model.score(self.val_set, self.val_label)))
        y_pred = self.lr_model.predict(self.test_set)
        print(classification_report(self.test_label, y_pred))
        if self.model_save == True:
            self.save()

    def predict(self,sentencelist):
        sentence_cut = self.data_env.cut_list(sentencelist)
        # print(sentence_cut)
        test = self.vector.transform(sentence_cut).toarray()

        test_pred = self.lr_model.predict(test)
        test_pred = self.encoder.inverse_transform(test_pred)
        # print(test_pred)
        return test_pred
        '''
        for sentence in sentencelist:
            sentence_cut = self.data_env.cut_list([sentence])
            print(sentence_cut)
            test = self.vector.transform(sentence_cut).toarray()
            print(test)
            test_pred = self.lr_model.predict(test)
            print(test_pred)
            for x in test[0]:
                if x != 0:
                    print(x)
            print(self.encoder.inverse_transform(test_pred))
        '''

    def save(self):
        joblib.dump(self.lr_model, self.save_path)
        print('-------------- model saved in %s -------------'%(self.save_path))

    def restore(self):
        self.lr_model = joblib.load(self.save_path)

    def run(self):
        if self.mode == 'train':
            print('--------------training-------------')
            self.train()
        else:
            self.restore()

if __name__ == '__main__':
    '''
    ques_save:
        从json文件中读取的数据是否需要存储为csv文件的标志
    ques_separate:
        True:原始多个json文件 每个文件对应一个csv文件存储还是多个json文件的结果存储到一个csv文件中
    ques_sort:
        True:从原始数据中筛选特定种类的数据 False:提取所有种类的数据
    ques_cate:
        从原始json数据文件中筛选的数据的种类，取值从const._EDU_RELATED中取,默认为None
    ques_clean_save, comm_clean_save: 
        默认为True 表示是否需要将处理后的提问和评论数据存储为两个csv文件(路径不可指定)
    corpus_save:
        是否需要将提取出来的训练语料存储为csv文件的标志,默认为True
    reprocess_raw:
        是否需要重新运行DataPreprocess的标志 为False则直接从对应的路径中读取数据 默认为True
    reprocess_raw:
        是否需要重新获取corpus并重新计算tfidf的标志 
        为False则直接从对应的路径中读取tfidf 否则重新获取corpus并计算tfidf 默认为True
    vector_path,tf_idf_path:
        存储vector和tfidf的路径 默认为None
    mode:
        'train':重新计算TF-IDF的结果 并将vector和tfidf存储在两个pickle文件中 并调用相应的分类器 训练模型
        'test':不重新计算TF-IDF的结果 从指定的路径中将vector和tfidf恢复出来 并将模型从指定路径中恢复出来
    enable_model_saver:
        是否存储模型的标志 mode为train时才有效 为True时将模型存储到指定路径
    save_model_path:
        mode为train时 enable_model_saver为True才有效 表示将模型存储到该路径
        mode为test时 将模型从该路径中恢复出来
    '''

    options = {"reprocess_raw": False, "reprocess_corpus": False, "vector_path": "./model/vector.pickle", "tf_idf_path": "./model/tf_idf.pickle"}

    dataenv = Data_Env_Base('./rawdata/baike_qa2019', './rawdata/zhihu/如何评价_课程', **options)

    options2 = {"mode":"test","enable_model_saver":True,"save_model_path":"./model/classification.pkl"}
    classification = Classification_Base(dataenv, **options2)

    classification.run()

    testlist = [
        '请问这道题为什么选A？',
        '为什么没有副总书记一职',
        '我家公猫为什么晚上乱叫呀',
        '两个无穷大量之积或代数和是无穷大量吗？为什么？',
        '我有点失望，甚至以为是假的，管你什么村头的高级运营大神什么的。',
        '我认为，任何在知识付费上面的分销，都是对知识的亵渎。',
        '最后就是希望大家能够积极，乐观一些，少些戾气'
    ]

    classification.predict(testlist)