from keras import backend as K
from keras.models import load_model
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.ensemble import VotingClassifier
from sklearn.model_selection import cross_val_score
from sklearn import svm
from sklearn.svm import SVC
from sklearn.externals import joblib
import pandas as pd
from emotion.capsule import *
import jieba

class Emotion_Capsule:
    def __init__(self,train_file,test_file,stopwords_file,emb_file,result_file,save_file,predict_file,mode='test'):
        self.trf = train_file
        self.tef = test_file
        self.stf = stopwords_file
        self.emf = emb_file
        self.rsf = result_file
        self.svf = save_file
        self.pdf = predict_file
        self.maxlen = 100
        self.mode = mode

        self.__init_getstopwords__()
        self.__init_glove__()
        self.__init_getdata__()
        self.__init_removestopwords__()
        self.__init_dataprocess__()

    def __init_getstopwords__(self):
        with open(self.stf, encoding='UTF-8') as f: #encoding='gbk'
            self.stop_words = set([l.strip() for l in f])

    def __init_glove__(self):
        self.embeddings_index = {}
        self.EMBEDDING_DIM = 300
        with open(self.emf, encoding='utf-8') as f:
            for i, line in enumerate(f):
                values = line.split()
                words = values[:-self.EMBEDDING_DIM]
                word = ''.join(words)
                try:
                    coefs = np.asarray(values[-self.EMBEDDING_DIM:], dtype='float32')
                    self.embeddings_index[word] = coefs
                except:
                    pass
                
    def __init_getdata__(self):
        self.train_df = pd.read_csv(self.trf, encoding='utf-8')
        self.test_df = pd.read_csv(self.tef, encoding='utf-8')
        self.train_df['label'] = self.train_df['subject'].str.cat(self.train_df['sentiment_value'].astype(str))

    def __init_removestopwords__(self):
        self.train_df['content'] = self.train_df.content.astype(str).map(
            lambda x: ''.join([e for e in x.strip().split() if e not in self.stop_words]))
        self.test_df['content'] = self.test_df.content.astype(str).map(
            lambda x: ''.join([e for e in x.strip().split() if e not in self.stop_words]))

    def __init_dataprocess__(self):
        train_dict = {}
        #train_dict以content为索引，content索引对应的是label集合
        for ind, row in self.train_df.iterrows():
            content, label = row['content'], row['label']
            if train_dict.get(content) is None:
                train_dict[content] = set([label])
            else:
                train_dict[content].add(label)
        
        conts = []
        labels = []
        for k, v in train_dict.items():
            conts.append(k)
            labels.append(v)

        self.mlb = MultiLabelBinarizer()
        #在多标签的情况下，输入必须是二值化的。所以需要MultiLabelBinarizer()先处理
        self.y_train = self.mlb.fit_transform(labels)

        self.content_list = [jieba.lcut(str(c)) for c in conts]

        test_content_list = [jieba.lcut(c) for c in self.test_df.content.astype(str).values]

        word_set = set([word for row in list(self.content_list) + list(test_content_list) for word in row])

        self.word2index = {w: i + 1 for i, w in enumerate(word_set)}
        self.seqs = [[self.word2index[w] for w in l] for l in self.content_list]
        self.seqs_dev = [[self.word2index[w] for w in l] for l in test_content_list]

        self.embedding_matrix = np.zeros((len(self.word2index) + 1, self.EMBEDDING_DIM))
        for word, i in self.word2index.items():
            embedding_vector = self.embeddings_index.get(word)
            if embedding_vector is not None:
                self.embedding_matrix[i] = embedding_vector

        max_features = len(word_set) + 1

    def get_padding_data(self,maxlen):
        # self.maxlen=maxlen
        x_train = sequence.pad_sequences(self.seqs, maxlen=maxlen) #构建等长序列
        x_dev = sequence.pad_sequences(self.seqs_dev, maxlen=maxlen)
        return x_train, x_dev

    def get_capsule_model(self):
        input1 = Input(shape=(self.maxlen,))
        embed_layer = Embedding(len(self.word2index) + 1,
                                self.EMBEDDING_DIM,
                                weights=[self.embedding_matrix],
                                input_length=self.maxlen,
                                trainable=False)(input1)
        embed_layer = SpatialDropout1D(rate_drop_dense)(embed_layer)

        x = Bidirectional(
            GRU(gru_len, activation='relu', dropout=dropout_p, recurrent_dropout=dropout_p, return_sequences=True))(
            embed_layer)
        capsule = Capsule(num_capsule=Num_capsule, dim_capsule=Dim_capsule, routings=Routings,
                          share_weights=True)(x)
        
        capsule = Flatten()(capsule)
        capsule = Dropout(dropout_p)(capsule)
        output = Dense(3, activation='sigmoid')(capsule)
        model = Model(inputs=input1, outputs=output)
        model.compile(
            loss='binary_crossentropy',
            optimizer='adam',
            metrics=['accuracy'])
        return model

    def train_and_test(self):
        # maxlen = 100
        X_train, X_dev = self.get_padding_data(self.maxlen)

        first_model_results = []
        for i in range(1):
            self.model = self.get_capsule_model()
            self.model.fit(X_train, self.y_train, batch_size=64, epochs=1)
            first_model_results.append(self.model.predict(X_dev, batch_size=1024))
        pred4 = np.average(first_model_results, axis=0)

        tmp = [[i for i in row] for row in pred4]

        for i, v in enumerate(tmp):
            if max(v) < 0.5:
                max_val = max(v)
                tmp[i] = [1 if j == max_val else 0 for j in v]
            else:
                tmp[i] = [int(round(j)) for j in v]

        tmp = np.asanyarray(tmp)
        res = self.mlb.inverse_transform(tmp)

        cids = []
        subjs = []
        sent_vals = []
        for c, r in zip(self.test_df.content_id, res):
            for t in r:
                if '-' in t:
                    sent_val = -1
                    subj = t[:-2]
                else:
                    sent_val = int(t[-1])
                    subj = t[:-1]
                cids.append(c)
                subjs.append(subj)
                sent_vals.append(sent_val)

        res_df = pd.DataFrame({'content_id': cids, 'subject': subjs, 'sentiment_value': sent_vals,
                               'sentiment_word': ['' for i in range(len(cids))]})

        columns = ['content_id', 'subject', 'sentiment_value', 'sentiment_word']
        res_df = res_df.reindex(columns=columns)
        res_df.to_csv(self.rsf, encoding='utf-8', index=False)
        self.save()

    def save(self):
        #joblib.dump(self.model, self.svf)
        #print('-------------- model saved in %s -------------'%(self.svf))
        self.model.save(self.svf)

    def restore(self):
        #self.model = joblib.load(self.svf)
        self.model = load_model(self.svf,custom_objects={'Capsule':Capsule})

    def predict(self,info):
        dataframe = pd.DataFrame({'content_id':1,'content':info})
        dataframe.to_csv(self.pdf, encoding='utf-8',index=False)
        self.predict_df = pd.read_csv(self.pdf, encoding='utf-8')
        self.predict_df['content'] = self.predict_df.content.astype(str).map(
            lambda x: ''.join([e for e in x.strip().split() if e not in self.stop_words]))

        predict_content_list = [jieba.lcut(c) for c in self.predict_df.content.astype(str).values]
        word_set = set([word for row in list(self.content_list) + list(predict_content_list) for word in row])

        word2index = {w: i + 1 for i, w in enumerate(word_set)}
        seqs_dev = [[word2index[w] for w in l] for l in predict_content_list]
        X_dev = sequence.pad_sequences(seqs_dev, maxlen=self.maxlen)

        # self.restore()
        results = []
        results.append(self.model.predict(X_dev, batch_size=1024))
        pred4 = np.average(results, axis=0)

        tmp = [[i for i in row] for row in pred4]

        for i, v in enumerate(tmp):
            if max(v) < 0.5:
                max_val = max(v)
                tmp[i] = [1 if j == max_val else 0 for j in v]
            else:
                tmp[i] = [int(round(j)) for j in v]

        tmp = np.asanyarray(tmp)
        res = self.mlb.inverse_transform(tmp)

        cids = []
        subjs = []
        sent_vals = []
        for c, r in zip(self.predict_df.content_id, res):
            for t in r:
                if '-' in t:
                    sent_val = -1
                    subj = t[:-2]
                else:
                    sent_val = int(t[-1])
                    subj = t[:-1]
                cids.append(c)
                subjs.append(subj)
                sent_vals.append(sent_val)

        res_df = pd.DataFrame({'content_id': cids, 'subject': subjs, 'sentiment_value': sent_vals,
                               'sentiment_word': ['' for i in range(len(cids))]})

        columns = ['content_id', 'subject', 'sentiment_value', 'sentiment_word']
        res_df = res_df.reindex(columns=columns)
        res_df.to_csv(self.rsf, encoding='utf-8', index=False)
        return sent_vals

    def run(self):
        if self.mode == 'train':
            # print('training')
            self.train_and_test()
        else:
            # print('restore')
            self.restore()

if __name__ == '__main__':
    model = Emotion_Capsule('train4.csv', 'test3.csv', 'hlp_stop_words.txt', 'sgns.baidubaike.bigram-char.tar',
                            'submit.csv', '../model/emotion.pkl', 'predict.csv','test')

    '''
    # 模型训练与测试
    model.train_and_test()
    '''
    model.run()
    # 情感分类
    info = ['这课真不错！']
    ret = model.predict(info)
    print(ret)

