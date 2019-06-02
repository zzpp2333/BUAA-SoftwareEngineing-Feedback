import os
import numpy as np
import tensorflow as tf
import time
from datetime import timedelta
from sklearn import metrics
from classify.Data_Env import Data_Env_Token
from classify.utils import categories

class CNN_config:
    """CNN配置参数"""

    embedding_dim = 64  # 词向量维度
    seq_length = 800  # 序列长度
    num_classes = 2  # 类别数
    num_filters = 256  # 卷积核数目
    kernel_size = 5  # 卷积核尺寸
    vocab_size = 8000  # 词汇表达小

    hidden_dim = 128  # 全连接层神经元

    dropout_keep_prob = 0.5  # dropout保留比例
    learning_rate = 1e-3  # 学习率

    batch_size = 64  # 每批训练大小
    num_epochs = 10  # 总迭代轮次

    print_per_batch = 100  # 每多少轮输出一次结果
    save_per_batch = 10  # 每多少轮存入tensorboard

class Classification_CNN:
    def __init__(self,data_env,config,**options):
        self.data_env = data_env
        self.config = config

        try:
            self.reprocess_token = options['reprocess_token']
        except KeyError:
            self.reprocess_token = True

        try:
            self.mode = options['mode']
        except KeyError:
            self.mode = 'train'

        try:
            self.save_dir = options['save_dir']
            self.save_path = os.path.join(self.save_dir,'bestvalidation')
        except KeyError:
            self.save_dir = './model/checkpoints/textcnn'
            self.save_path = os.path.join(self.save_dir,'bestvalidation')

        self.__init_input__()
        self.__init_cnn__()

        self.__init_summary__()
        self.__init_saver__()
        self.__init_data__()
        self.__init_session__()

    def __init_input__(self):
        # 三个待输入的数据
        self.input_x = tf.placeholder(tf.int32, [None, self.config.seq_length], name='input_x')
        self.input_y = tf.placeholder(tf.float32, [None, self.config.num_classes], name='input_y')
        self.keep_prob = tf.placeholder(tf.float32, name='keep_prob')

    def __init_cnn__(self):
        """CNN模型"""
        # 词向量映射
        with tf.device('/cpu:0'):
            embedding = tf.get_variable('embedding', [self.config.vocab_size, self.config.embedding_dim])
            embedding_inputs = tf.nn.embedding_lookup(embedding, self.input_x)

        with tf.name_scope("cnn"):
            # CNN layer
            conv = tf.layers.conv1d(embedding_inputs, self.config.num_filters, self.config.kernel_size, name='conv')
            # global max pooling layer
            gmp = tf.reduce_max(conv, reduction_indices=[1], name='gmp')

        with tf.name_scope("score"):
            # 全连接层，后面接dropout以及relu激活
            fc = tf.layers.dense(gmp, self.config.hidden_dim, name='fc1')
            fc = tf.contrib.layers.dropout(fc, self.keep_prob)
            fc = tf.nn.relu(fc)

            # 分类器
            self.logits = tf.layers.dense(fc, self.config.num_classes, name='fc2')
            self.y_pred_cls = tf.argmax(tf.nn.softmax(self.logits), 1)  # 预测类别

        with tf.name_scope("optimize"):
            # 损失函数，交叉熵
            cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=self.logits, labels=self.input_y)
            self.loss = tf.reduce_mean(cross_entropy)
            # 优化器
            self.optim = tf.train.AdamOptimizer(learning_rate=self.config.learning_rate).minimize(self.loss)

        with tf.name_scope("accuracy"):
            # 准确率
            correct_pred = tf.equal(tf.argmax(self.input_y, 1), self.y_pred_cls)
            self.acc = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    def __init_data__(self):
        print("Loading training and validation data...")
        # 载入训练集与验证集
        start_time = time.time()

        x_pad, y_pad = self.data_env.process_pad(
            self.data_env.word_to_id, self.data_env.cate_to_id, self.reprocess_token, self.config.seq_length
        )
        sepa = self.data_env.get_separation(x_pad, y_pad)
        self.x_train = sepa['x_train']
        self.y_train = sepa['y_train']
        self.x_test = sepa['x_test']
        self.y_test = sepa['y_test']
        self.x_val = sepa['x_val']
        self.y_val = sepa['y_val']

        time_dif = self.get_time_dif(start_time)
        print("Time usage:", time_dif)

    def __init_summary__(self):
        print("Configuring TensorBoard...")
        # 配置 Tensorboard，重新训练时，请将tensorboard文件夹删除，不然图会覆盖
        tensorboard_dir = 'tensorboard/textcnn'
        if not os.path.exists(tensorboard_dir):
            os.makedirs(tensorboard_dir)

        tf.summary.scalar("loss", self.loss)
        tf.summary.scalar("accuracy", self.acc)
        self.merged_summary = tf.summary.merge_all()
        self.writer = tf.summary.FileWriter(tensorboard_dir)

    def __init_saver__(self):
        # 配置 Saver
        print("Configuring Saver...")
        self.saver = tf.train.Saver()
        #准备文件夹
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def __init_session__(self):
        self.session = tf.Session()
        self.session.run(tf.global_variables_initializer())

    def get_time_dif(self,start_time):
        """获取已使用时间"""
        end_time = time.time()
        time_dif = end_time - start_time
        return timedelta(seconds=int(round(time_dif)))

    def feed_data(self,x_batch, y_batch, keep_prob):
        feed_dict = {
            self.input_x: x_batch,
            self.input_y: y_batch,
            self.keep_prob: keep_prob
        }
        return feed_dict

    def evaluate(self,sess, x_, y_):
        """评估在某一数据上的准确率和损失"""
        data_len = len(x_)
        batch_eval = self.data_env.batch_iter(x_, y_, 128)
        total_loss = 0.0
        total_acc = 0.0
        for x_batch, y_batch in batch_eval:
            batch_len = len(x_batch)
            feed_dict = self.feed_data(x_batch, y_batch, 1.0)
            loss, acc = sess.run([self.loss, self.acc], feed_dict=feed_dict)
            total_loss += loss * batch_len
            total_acc += acc * batch_len

        return total_loss / data_len, total_acc / data_len

    def train(self):
        # 创建session
        self.writer.add_graph(self.session.graph)

        print('Training and evaluating...')
        start_time = time.time()
        total_batch = 0  # 总批次
        best_acc_val = 0.0  # 最佳验证集准确率
        last_improved = 0  # 记录上一次提升批次
        require_improvement = 1000  # 如果超过1000轮未提升，提前结束训练

        flag = False
        for epoch in range(self.config.num_epochs):
            print('Epoch:', epoch + 1)
            batch_train = self.data_env.batch_iter(self.x_train, self.y_train, self.config.batch_size)
            for x_batch, y_batch in batch_train:
                feed_dict = self.feed_data(x_batch, y_batch, self.config.dropout_keep_prob)

                if total_batch % self.config.save_per_batch == 0:
                    # 每多少轮次将训练结果写入tensorboard scalar
                    s = self.session.run(self.merged_summary, feed_dict=feed_dict)
                    self.writer.add_summary(s, total_batch)

                if total_batch % self.config.print_per_batch == 0:
                    # 每多少轮次输出在训练集和验证集上的性能
                    feed_dict[self.keep_prob] = 1.0
                    loss_train, acc_train = self.session.run([self.loss, self.acc], feed_dict=feed_dict)
                    loss_val, acc_val = self.evaluate(self.session, self.x_val, self.y_val)  # todo

                    if acc_val > best_acc_val:
                        # 保存最好结果
                        best_acc_val = acc_val
                        last_improved = total_batch
                        self.saver.save(sess=self.session, save_path=self.save_path)
                        improved_str = '*'
                    else:
                        improved_str = ''

                    time_dif = self.get_time_dif(start_time)
                    msg = 'Iter: {0:>6}, Train Loss: {1:>6.2}, Train Acc: {2:>7.2%},' \
                          + ' Val Loss: {3:>6.2}, Val Acc: {4:>7.2%}, Time: {5} {6}'
                    print(msg.format(total_batch, loss_train, acc_train, loss_val, acc_val, time_dif, improved_str))

                self.session.run(self.optim, feed_dict=feed_dict)  # 运行优化
                total_batch += 1

                if total_batch - last_improved > require_improvement:
                    # 验证集正确率长期不提升，提前结束训练
                    print("No optimization for a long time, auto-stopping...")
                    flag = True
                    break  # 跳出循环
            if flag:  # 同上
                break

    def restore(self):
        self.saver.restore(sess=self.session, save_path=self.save_path)  # 读取保存的模型

    def test(self):
        start_time = time.time()

        print('Testing...')
        loss_test, acc_test = self.evaluate(self.session, self.x_test, self.y_test)
        msg = 'Test Loss: {0:>6.2}, Test Acc: {1:>7.2%}'
        print(msg.format(loss_test, acc_test))

        batch_size = 128
        data_len = len(self.x_test)
        num_batch = int((data_len - 1) / batch_size) + 1

        y_test_cls = np.argmax(self.y_test, 1)
        y_pred_cls = np.zeros(shape=len(self.x_test), dtype=np.int32)  # 保存预测结果
        for i in range(num_batch):  # 逐批次处理
            start_id = i * batch_size
            end_id = min((i + 1) * batch_size, data_len)
            feed_dict = {
                self.input_x: self.x_test[start_id:end_id],
                self.keep_prob: 1.0
            }
            y_pred_cls[start_id:end_id] = self.session.run(self.y_pred_cls, feed_dict=feed_dict)

        # 评估
        print("Precision, Recall and F1-Score...")
        print(metrics.classification_report(y_test_cls, y_pred_cls, target_names=categories))

        # 混淆矩阵
        print("Confusion Matrix...")
        cm = metrics.confusion_matrix(y_test_cls, y_pred_cls)
        print(cm)

        time_dif = self.get_time_dif(start_time)
        print("Time usage:", time_dif)

    def predict(self,message):
        input_x = self.data_env.pad_predict_message(message,self.config.seq_length)
        feed_dict = {
            self.input_x:input_x,
            self.keep_prob:1.0
        }
        y_pred_cls = self.session.run(self.y_pred_cls, feed_dict=feed_dict)
        return categories[y_pred_cls[0]]

    def run(self):
        if self.mode == 'train':
            self.train()
        else:
            self.restore()

if __name__ == '__main__':
    options = {"ques_save": True, "ques_separate": True, "ques_sort": True, "ques_cate": None,
               "ques_clean_save": True, "comm_clean_save": True,
               "corpus_save": True, "reprocess_raw": False,"reprocess_corpus": False
               }
    data_env = Data_Env_Token('./rawdata/baike_qa2019', './rawdata/zhihu/如何评价_课程', **options)

    options2 = {"reprocess_token": True, 'mode': 'train', 'save_dir': './model/checkpoints/textcnn'}

    model = Classification_CNN(data_env,CNN_config,**options2)
    model.run()
    model.test()

    testlist = [
        'emmmm',
        '如何看待大一课程缺少专业性的问题？',
        '如何看待考虫考研课程？',
        '如何评价北航计算机学院面向对象编程课程的评分制度',
        '是我见过最蠢的评分制度，只有老师一个人认为这是好的。',
        '请问这道题为什么选A？',
        '为什么没有副总书记一职',
        '我家公猫为什么晚上乱叫呀',
        '两个无穷大量之积或代数和是无穷大量吗？为什么？',
        '我有点失望，甚至以为是假的，管你什么村头的高级运营大神什么的。',
        '我认为，任何在知识付费上面的分销，都是对知识的亵渎。',
        '最后就是希望大家能够积极，乐观一些，少些戾气'
    ]
    for sen in testlist:
        print(model.predict(sen))