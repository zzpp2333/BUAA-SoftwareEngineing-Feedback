import re
import os
from abc import abstractmethod
import jieba
import jieba.posseg as pseg
import jieba.analyse as anls
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
import pickle
import codecs
from collections import Counter
import tensorflow.contrib.keras as kr
from classify.DataPreprocess import DataPreprocess
from classify.utils import const, categories

class Data_Env_ELe:
    def __init__(self,questionfolder,commentfolder,**options):

        try:  # 是否需要重新运行DataPreprocess的标志 不需要则直接从文件中load
            self.update_raw = options['reprocess_raw']
        except KeyError:
            self.update_raw= True
        try:  # 是否需要把提问和评论合并后并打好标签的结果存储到csv文件下的flag 默认为需要(True)
            self.corpus_save2csv = options['corpus_save']
        except KeyError:
            self.corpus_save2csv = True

        if self.update_raw is False:
            # f = open('./rawdata/_zhihu_clean.csv', 'r', encoding='utf-8')
            with codecs.open('./rawdata/_comm_clean.csv', 'r', 'utf-8') as f_comm:
                self.comments_ = pd.read_csv(f_comm).astype(str)
            # print(self.comments_.head())
            # f = open('./rawdata/_Baike_merge.csv', 'r', encoding='utf-8')
            with codecs.open('./rawdata/_Baike_merge.csv', 'r', 'utf-8') as f_ques:
                self.question_ = pd.read_csv(f_ques).astype(str)
                self.question_ = self.question_[const._MERGE_COLUMN].to_frame()
            # print(self.question_.head())
        else:
            self.data_base = DataPreprocess(questionfolder, commentfolder, **options)
            self.comments_ = self.data_base.comments
            self.question_ = self.data_base.questions

    def shuffle(self):
        index = np.random.choice(len(self.df_data), len(self.df_data), replace=False)
        self.df_data = self.df_data.iloc[index].reset_index(drop=True)
        self.df_labels = self.df_labels.iloc[index].reset_index(drop=True)
        # self.df_data = self.df_data.sample(frac=1).reset_index(drop=True)

    def cut_list(self, sentencelist):
        corpus_cut = []
        for sentence in sentencelist:
            sentence_cut = jieba.cut(sentence)
            try:
                result = ' '.join(sentence_cut)
            except AttributeError:
                result = ' '.join(str(w) for w in sentence_cut)
            finally:
                corpus_cut.append(result)
        # print(corpus_cut[0:10])
        return corpus_cut

    @abstractmethod
    def __prepare_corpus__(self):
        def get_raw_str(df_comments, df_questions):
            # self.data_env.comments,self.data_env.questions维数不一致
            df_comm = df_comments.rename(columns={const._COMMENT_COLUMN:const._DATA_COLUMN})
            df_ques = df_questions.rename(columns={const._MERGE_COLUMN:const._DATA_COLUMN})

            df_result = pd.concat([df_comm,df_ques],axis=0).reset_index(drop=True)
            # df_result = df_result.drop('index',axis=1)

            return df_result

        def get_labels(df_comments, df_questions):
            labels = np.array([const._COMT_LABEL for x in range(len(df_comments))])
            labels = np.append(labels, [const._QUES_LABEL for x in range(len(df_questions))])

            df_labels = pd.DataFrame()
            df_labels[const._LABEL_COLUMN] = labels
            return df_labels

        # df_balanced_comm, df_balanced_ques = balance_comm_ques(self.comments_, self.question_)
        # df_data = get_raw_str(df_balanced_comm, df_balanced_ques)
        # df_labels = get_labels(df_balanced_comm, df_balanced_ques)
        # df_balanced_comm, df_balanced_ques = balance_comm_ques(self.comments_,self.question_)

        # '''
        df_data = get_raw_str(self.comments_,self.question_)
        df_labels = get_labels(self.comments_,self.question_)
        # '''

        return df_data, df_labels

    def __save_corpus__(self):
        if self.corpus_save2csv is True:
            df = pd.concat([self.df_data,self.df_labels],axis=1)
            df.to_csv('./rawdata/corpus_labels.csv',index=False,encoding='utf-8')

    def __restore_corpus__(self):
        with codecs.open("./rawdata/corpus_labels.csv","r",'utf-8') as f:
            df_all = pd.read_csv(f).astype(str)
        df_data = df_all[const._DATA_COLUMN].to_frame()
        df_labels = df_all[const._LABEL_COLUMN].to_frame()
        return df_data,df_labels

    def get_separation(self, x, y):
        trn_test_border = int(len(self.df_labels) * const._TRN_TEST_BORDER) + 1
        test_val_border = int(len(self.df_labels) * const._TEST_VAL_BORDER) + 1
        train_label = y[:trn_test_border]
        test_label = y[trn_test_border:test_val_border]
        val_label = y[test_val_border:]

        train_set = x[:trn_test_border]
        test_set = x[trn_test_border:test_val_border]
        val_set = x[test_val_border:]
        return {'x_train':train_set,'y_train':train_label,'x_val':val_set,'y_val':val_label,
                'x_test':test_set,'y_test':test_label}

class Data_Env_Base(Data_Env_ELe):

    def __init__(self, questionfolder, commentfolder, **options):
        super(Data_Env_Base, self).__init__(questionfolder, commentfolder, **options)

        try: #是否重新获取corpus的标志
            self.tf_idf_save = options['reprocess_corpus']
        except KeyError:
            self.tf_idf_save = True

        try: #存储tfvectorize的路径
            self.vector_path = options['vector_path']
        except KeyError:
            self.vector_path = None
        try: #存储tfidf结果的路径
            self.tf_idf_path = options['tf_idf_path']
        except KeyError:
            self.tf_idf_path = None

        if self.tf_idf_save is True:
            self.df_data, self.df_labels = self.__prepare_corpus__()

            self.shuffle()

            self.__save_corpus__()

            self.vector, self.tf_idf = self.__vector_corpus__()
            self.__save_vector__()
        else:
            self.df_data, self.df_labels = self.__restore_corpus__()
            self.shuffle()
            self.__restore_vector__()

    def __save_vector__(self):
        pickle.dump(self.vector,open(self.vector_path,"wb"))
        pickle.dump(self.tf_idf,open(self.tf_idf_path,"wb"))

    def __restore_vector__(self):
        self.vector = pickle.load(open(self.vector_path,"rb"))
        self.tf_idf = pickle.load(open(self.tf_idf_path,"rb"))

    def __prepare_corpus__(self):

        def balance_comm_ques(df_1, df_2):
            df_len = len(df_1)
            if df_len > len(df_2): #len(df1) > len(df2)
                df_len = len(df_2)
                index = np.random.choice(len(df_1),df_len,replace=False)
                df_1_balanced = df_1.iloc[index].reset_index(drop=True)
                df_2_balanced = df_2
            else:  # len(df1) <= len(df2)
                index = np.random.choice(len(df_2), df_len, replace=False)
                df_1_balanced = df_1
                df_2_balanced = df_2.iloc[index].reset_index(drop=True)
            return df_1_balanced, df_2_balanced

        def get_raw_str(df_comments, df_questions):
            # self.data_env.comments,self.data_env.questions维数不一致
            df_comm = df_comments.rename(columns={const._COMMENT_COLUMN:const._DATA_COLUMN})
            df_ques = df_questions.rename(columns={const._MERGE_COLUMN:const._DATA_COLUMN})

            df_result = pd.concat([df_comm,df_ques],axis=0).reset_index(drop=True)
            # df_result = df_result.drop('index',axis=1)

            return df_result

        def get_labels(df_comments, df_questions):
            labels = np.array([const._COMT_LABEL for x in range(len(df_comments))])
            labels = np.append(labels, [const._QUES_LABEL for x in range(len(df_questions))])

            df_labels = pd.DataFrame()
            df_labels[const._LABEL_COLUMN] = labels
            return df_labels

        df_balanced_comm, df_balanced_ques = balance_comm_ques(self.comments_, self.question_)
        df_data = get_raw_str(df_balanced_comm,df_balanced_ques)
        df_labels = get_labels(df_balanced_comm,df_balanced_ques)

        return df_data, df_labels

    def __vector_corpus__(self):

        def cut_corpus(df_all):
            '''
            for sentence in df_all[const._DATA_COLUMN]:
                sentence_cut = jieba.cut(sentence)
                result = ' '.join(sentence_cut)
                corpus_cut.append(result)
            '''
            corpus_cut = self.cut_list(df_all[const._DATA_COLUMN])

            df_all[const._CUT_COLUMN] = corpus_cut
            # print(corpus_cut[0:20])

        def incld_stpwdlst(stpwrdpath):
            # 从文件导入停用词表
            stpwrd_dic = open(stpwrdpath, 'r')
            stpwrd_content = stpwrd_dic.read()
            # 将停用词表转换为list
            stpwrdlst = stpwrd_content.splitlines()
            stpwrd_dic.close()
            return stpwrdlst

        def vectorize(df_data, stpwrdpath, sublinear=True, max_df=0.5):
            vector = TfidfVectorizer(stop_words=incld_stpwdlst(stpwrdpath), sublinear_tf=sublinear, max_df=max_df)
            tfidf = vector.fit_transform(df_data[const._CUT_COLUMN])

            words = vector.get_feature_names()
            print("how many words: {0}".format(len(words)))
            print("tf-idf shape: ({0},{1})".format(tfidf.shape[0], tfidf.shape[1]))

            # weightlist = tfidf.toarray()
            # print(weightlist[0:5])

            '''
            wordlist = vector.get_feature_names()  # 获取词袋模型中的所有词
            # tf-idf矩阵 元素a[i][j]表示j词在i类文本中的tf-idf权重
            weightlist = tfidf.toarray()
            # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
            for i in range(len(weightlist)):
                print("-------第", i, "段文本的词语tf-idf权重------")
                for j in range(len(wordlist)):
                    if weightlist[i][j] > 0.2:
                        print(wordlist[j], weightlist[i][j])
            '''

            return vector, tfidf

        cut_corpus(self.df_data)
        vector, tfidf = vectorize(self.df_data, './classify/stop_words.txt', True, 0.5)
        return vector,tfidf

class Data_Env_Token(Data_Env_ELe):

    def __init__(self, questionfolder, commentfolder, **options):
        super(Data_Env_Token, self).__init__(questionfolder, commentfolder, **options)

        try: #是否重新获取corpus的标志
            self.vocab_save = options['reprocess_corpus']
        except KeyError:
            self.vocab_save = True

        if self.vocab_save is True:
            self.df_data, self.df_labels = self.__prepare_corpus__()

            self.shuffle()

            self.vocab, self.word_to_id = self.__prepare_token__()
            self.__save_corpus__()

        else:
            self.df_data, self.df_labels = self.__restore_corpus__()
            # self.shuffle()
            self.vocab, self.word_to_id = self.__restore_token__()

        self.cate_to_id = self.cate2id()

    def __save_corpus__(self):
        if self.corpus_save2csv is True:
            df = pd.concat([self.df_data,self.df_labels],axis=1)
            df.to_csv('./rawdata/corpus_labels.csv',index=False,encoding='utf-8')
            with codecs.open('./rawdata/vocabulary.txt','w','utf-8') as f:
                f.write('\n'.join(self.vocab)+'\n')

    def __restore_token__(self):
        with codecs.open('./rawdata/vocabulary.txt','r','utf-8') as f:
            words = [_.strip() for _ in f.readlines()]
        word_to_id = dict(zip(words,range(len(words))))
        return words,word_to_id

    def cate2id(self):
        # categories = [const._COMT_LABEL, const._QUES_LABEL]
        cate_to_id = dict(zip(categories, range(len(categories))))
        return cate_to_id

    def __prepare_token__(self):
        def word2id(words):
            word_to_id = dict(zip(words,range(len(words))))
            return word_to_id

        '''将数据处理成token列表'''
        def get_listed_contents(data):
            contents = []
            for content in data:
                contents.append(list(content))
            return contents

        '''根据训练集构建词汇表并存储下来'''
        def build_vocab(data, vocab_size=5000):
            list_data = get_listed_contents(data)

            all_data = []
            for content in list_data:
                all_data.extend(content)

            counter = Counter(all_data)
            count_pairs = counter.most_common(vocab_size-1)
            words, _ = list(zip(*count_pairs))
            # 添加一个<PAD>来讲所有文本pad为同一长度
            words = ['<PAD>'] + list(words)
            return words

        data = self.df_data[const._DATA_COLUMN].values.tolist()
        words = build_vocab(data)
        word_to_id = word2id(words)
        return words, word_to_id

    '''将文本pad为固定长度'''
    def process_pad(self, word_to_id, cate_to_id, re_seq=True, max_length=600):
        if re_seq is True:
            data = self.df_data[const._DATA_COLUMN].values.tolist()
            labels = self.df_labels[const._LABEL_COLUMN].values.tolist()

            data_id, label_id = [], []
            for i in range(len(data)):
                data_id.append([word_to_id[x] for x in data if x in word_to_id])
                label_id.append(cate_to_id[labels[i]])

            x_pad = kr.preprocessing.sequence.pad_sequences(data_id,max_length)
            y_pad = kr.utils.to_categorical(label_id,num_classes=len(cate_to_id))
            print(type(x_pad),type(y_pad))
            np.save("./rawdata/padseq/data.npy",x_pad)
            np.save("./rawdata/padseq/label.npy",y_pad)
        else:
            x_pad = np.load('./rawdata/padseq/data.npy')
            y_pad = np.load('./rawdata/padseq/label.npy')
        return x_pad, y_pad

    def pad_predict_message(self, message, max_length=600):
        data = [self.word_to_id[x] for x in message if x in self.word_to_id]
        input_x = kr.preprocessing.sequence.pad_sequences([data], max_length)
        return input_x

    def batch_iter(self, x, y, batch_size=64):
        data_len = len(x)
        num_batch = int((data_len - 1)/batch_size)+1

        indices = np.random.permutation(np.arange(data_len))
        x_shuffle = x[indices]
        y_shuffle = y[indices]

        for i in range(num_batch):
            start_id = i*batch_size
            end_id = min((i+1)*batch_size, data_len)
            yield x_shuffle[start_id:end_id], y_shuffle[start_id:end_id]

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
    '''
    options = {"ques_save": True, "ques_separate": True, "ques_sort": True, "ques_cate": None,
               "ques_clean_save": True, "comm_clean_save":True, "corpus_save":True,"reprocess_raw":True,
               "reprocess_corpus":False, "vector_path":"./model/vector.pickle","tf_idf_path":"./model/tf_idf.pickle",
               }
    Data_Env_Base('./rawdata/baike_qa2019', './rawdata/zhihu/如何评价_课程', **options)
