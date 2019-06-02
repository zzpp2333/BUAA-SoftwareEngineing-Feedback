from classify.Data_Env import Data_Env_Base, Data_Env_Token
from classify.Classification import Classification_Base
from classify.Classification_CNN import CNN_config, Classification_CNN
from emotion.Emotion_Capsule import Emotion_Capsule

def get_classification(strlist):
    options = {"reprocess_raw": False, "reprocess_corpus": False, "vector_path": "./model/vector.pickle",
               "tf_idf_path": "./model/tf_idf.pickle"}

    dataenv = Data_Env_Base('./rawdata/baike_qa2019', './rawdata/zhihu/如何评价_课程', **options)

    options2 = {"mode": "test", "enable_model_saver": True, "save_model_path": "./model/classification.pkl"}
    classification = Classification_Base(dataenv, **options2)

    classification.run()
    clsf = classification.predict(strlist)
    return clsf

def get_emotion(strlist):
    model = Emotion_Capsule('./emotion/train4.csv', './emotion/test3.csv', './emotion/hlp_stop_words.txt', './emotion/sgns.baidubaike.bigram-char.tar',
                            './emotion/submit.csv', './model/emotion.pkl', './emotion/predict.csv', 'test')

    '''
    # 模型训练与测试
    model.train_and_test()
    '''
    model.run()
    # 情感分类
    # print(strlist)
    emo = model.predict(strlist)
    return emo

def test_CNN():
    options = {"ques_save": True, "ques_separate": True, "ques_sort": True, "ques_cate": None,
               "ques_clean_save": True, "comm_clean_save": True,
               "corpus_save": True, "reprocess_raw": False, "reprocess_corpus": False
               }
    data_env = Data_Env_Token('./rawdata/baike_qa2019', './rawdata/zhihu/如何评价_课程', **options)

    options2 = {"reprocess_token": True, 'mode': 'train', 'save_dir': './model/checkpoints/textcnn'}

    model = Classification_CNN(data_env, CNN_config, **options2)
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

if __name__ == '__main__':
    # test_CNN()
    testlist = [
        'emmm',
        '请问这道题为什么选A？',
        '为什么没有副总书记一职',
        '我家公猫为什么晚上乱叫呀',
        '两个无穷大量之积或代数和是无穷大量吗？为什么？',
        '我有点失望，甚至以为是假的，管你什么村头的高级运营大神什么的。',
        '我认为，任何在知识付费上面的分销，都是对知识的亵渎。',
        '最后就是希望大家能够积极，乐观一些，少些戾气'
    ]
    print(get_classification(testlist))
    # 返回值为question或comment 表示是提问或评论
    # 可以在classify/utils里修改const._QUESTION_COLUMN/const._COMMENT_COLUMN的值
    # 并设置reprocess_raw reprocess_corpus为True后重新运行后 返回值自动修改

    #info = ['这课真不错！']
    info = [
        '我有点失望，甚至以为是假的，管你什么村头的高级运营大神什么的。',
        '我认为，任何在知识付费上面的分销，都是对知识的亵渎。',
        '最后就是希望大家能够积极，乐观一些，少些戾气'
    ]
    # print(get_emotion(info))
    # 返回值1表示正面 0表示中性 -1表示负面
