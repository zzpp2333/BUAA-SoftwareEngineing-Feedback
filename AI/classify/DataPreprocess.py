import os
import re
import numpy as np
import pandas as pd
from classify.baike import Baike
from classify.utils import const

pattern = r'([,.;?~!，。；！？…]+)'

class DataPreprocess:
    def __init__(self,questionfolder,commentfolder,**options):

        try: #是否需要把title和desc合并后的结果存储到csv文件下的flag 默认为需要(True)
            self.merge_save2csv = options['ques_clean_save']
        except KeyError:
            self.merge_save2csv = True

        try: #是否需要把处理后的评论数据存储到csv文件下的flag 默认为需要(True)
            self.comm_save2csv = options['comm_clean_save']
        except KeyError:
            self.comm_save2csv = True

        #直接用questionfolder参数new一个Baike的class,然后对self.baike.get_title()/self.baike.get_desc()进行处理
        #处理好的数据存在self.baike.df_all的新列中
        self.baike = Baike(questionfolder, **options)

        #需要读取commentfolder的所有子文件夹下的txt文件
        (zhihufolder, self.queryname) = os.path.split(commentfolder)
        self.cmt_folder = commentfolder
        print(zhihufolder,self.queryname)

        #self.cmtfl_files是以提问title命名的文件夹
        self.cmtfl_files = self.__dirPath__()
        self.cmtfl_files.sort()

        print(len(self.cmtfl_files))
        #print(self.cmtfl_files[0])

        #DataFrame
        self.comments = self.__prep_cmt_data__()
        self.questions = self.__prep_ques_data__()
        #f = open('./rawdata/Baike_merge.csv')
        #self.questions = pd.read_csv(f)[const._MERGE_COLUMN].to_frame()


    def __dirPath__(self):
        file_list = None
        try:
            file_list = os.listdir(self.cmt_folder)
        except IOError as err:
            print('IOError: ' + err.filename)
        return file_list

    def __prep_cmt_data__(self):

        def get_str(str, placewith=''):
            str = str.replace('\r\n',placewith)
            str = str.replace('\r',placewith)
            str = str.replace('\n',placewith)
            return str

        def read_dir(dir_path):
            cmtlist = os.listdir(dir_path)

            cmt = []
            for txt_file in cmtlist:
                full_txt_file = os.path.join(dir_path,txt_file)
                if os.path.isdir(full_txt_file):
                    continue
                try:
                    load_file = open(full_txt_file,'r',encoding='utf-8')
                except UnicodeDecodeError as e:
                    print('This transformer data is not utf-8 encoded.', e)
                    load_file = open(full_txt_file, 'r', encoding='gbk')

                contents = get_str(load_file.read(),placewith=' ')
                #内容中含有链接等html格式的内容
                cmt.append(contents)

            df_result = pd.DataFrame()
            df_result[const._COMMENT_COLUMN] = cmt
            return df_result

        def read_txt():
            df_comments = None

            for file in self.cmtfl_files:
                full_path = os.path.join(self.cmt_folder,file)

                if df_comments is None:
                    df_comments = read_dir(full_path)
                else:
                    df_comments = pd.concat([df_comments,read_dir(full_path)],axis=0).reset_index(drop=True)

            return df_comments

        def read_imooc():
            f = open('./rawdata/imooc_all.csv',"r",encoding='utf-8')
            df_imooc = pd.read_csv(f)
            return df_imooc

        def save(df_all):
            if self.comm_save2csv is True:
                save_path = r'./rawdata/_comm_clean.csv'
                df_all.to_csv(save_path, index=False, encoding='utf-8')

        df_zhihu = read_txt()
        df_imooc = read_imooc()
        df_res = pd.concat([df_zhihu,df_imooc],axis=0).reset_index(drop=True)
        save(df_res)
        return df_res
        #return df_imooc

    def __prep_ques_data__(self):

        def str_concate(start,end):
            if start is None:
                return end
            else:
                return start+end

        def merge_title_desc(title, desc): #处理title和desc
            #print(type(title),type(desc))
            if desc.replace(' ','') == '':
                return title
            elif title == desc:
                return title
            elif title.find(desc,0,len(title)) > -1:
                return title
            elif desc.find(title,0,len(desc)) > -1:
                return desc
            else:
                split_tit = re.split(pattern,title)
                #split_tit.append("")
                #split_tit = ["".join(i) for i in zip(split_tit[0::2], split_tit[1::2])]

                ret = None
                for text in split_tit:
                    if re.match(pattern, text) is not None:
                        ret = str_concate(ret,text)
                        continue
                    index = desc.find(text,0,len(desc))
                    if index > -1:
                        ret = str_concate(ret,text+desc[index+len(text):])
                        return ret
                    else:
                        ret = str_concate(ret,text)
                ret = str_concate(ret,desc)
                return ret

        def add_zhihu_question(original):
            for str in self.cmtfl_files:
                if str[-1] == '?':
                    original.append(str)
            return original

        def baike_clean(df_result,titlelist,desclist,datanum):
            question_str = []
            #print(titlelist[0], desclist[0])
            #print(titlelist[0].values, type(titlelist[0].values))
            #print(type(titlelist[0]), type(desclist[0]))
            for i in range(0,datanum):
                merge_str = merge_title_desc(titlelist[i],desclist[i])
                question_str.append(merge_str)

            df_result[const._MERGE_COLUMN] = question_str

            if self.merge_save2csv is True:
                save_path = r'./rawdata/_Baike_merge.csv'
                df_result.to_csv(save_path,index=False,encoding='utf-8')

            df_ques = pd.DataFrame()
            question_str = add_zhihu_question(question_str)
            df_ques[const._MERGE_COLUMN] = question_str
            return df_ques

        df_ques = baike_clean(self.baike.df_all, self.baike.get_title(), self.baike.get_desc(), self.baike.data_num)
        return df_ques
        #return self.baike.df_all[const._MERGE_COLUMN].to_frame()
        #ret = processques(Baike.title,Baike.desc)
        #print(ret)

if __name__ == '__main__':
    options = {"ques_save": True, "ques_separate": True, "ques_sort": True, "ques_cate": None, "ques_clean_save":True, "comm_clean_save":True}

    DataPreprocess('./rawdata/baike_qa2019', './rawdata/zhihu/如何评价_课程', **options)