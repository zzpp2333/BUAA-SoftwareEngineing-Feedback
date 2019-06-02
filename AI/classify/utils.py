class ConstType:
    class ConstError(TypeError): pass

    def __setattr__(self, key, value):
        if key in self.__dict__.keys():
            raise self.ConstError("constant reassignment error!")
        self.__dict__[key] = value

const = ConstType()

#Baike问答的category与教育有关
const._EDU_RELATE = 1

#百科问答json文件中的所有键名
const._CATE_KEY = 'category'
const._TITLE_KEY = 'title'
const._ANSWER_KEY = 'answer'
const._DESC_KEY = 'desc'

#Baike类中的df_all的列名
const._CATE_COLUMN = 'cate'
const._TITLE_COLUMN = 'title'
const._DESC_COLUMN = 'desc'
const._MERGE_COLUMN = 'merge'

#存储提问数据的df的列名
const._QUESTION_COLUMN = 'questions'
#存储知乎评价数据的df的列名
const._COMMENT_COLUMN = 'comments'

#存储评论和提问数据和标签的df的列名
const._DATA_COLUMN = 'data'
const._CUT_COLUMN = 'cut'
const._LABEL_COLUMN = 'label'

const._COMT_LABEL = 'comment'
const._QUES_LABEL = 'question'

const._TRN_TEST_BORDER = 0.7
const._TEST_VAL_BORDER = 0.9

const._EMO_COLUMN = 'emotion'
const._POS_EMOTION = 2
const._NEU_EMOTION = 1
const._NEG_EMOTION = 0
const._ERR_EMOTION = -1

categories = [const._COMT_LABEL, const._QUES_LABEL]