import os
import json
import numpy as np
import pandas as pd
from classify.utils import const

class Baike:

    def __init__(self, folderpath, **options):
        try: # 是否需要把数据存储到csv文件下的flag 默认为需要(True)
            self.save2csv = options['ques_save']
        except KeyError:
            self.save2csv = True

        try:
            self.separate = options['ques_separate'] # True表示把文件夹下的每一个json文件分别存储成一个csv文件
        except KeyError:
            self.separate = False # 默认为所有json文件中的数据存储到一个文件夹下

        try: # read_json的默认参数 True表示需要对json文件中的数据按照cate进行筛选
            self.sort = options['ques_sort']
        except KeyError:
            self.sort = True

        try: # read_json的默认参数 表示从json文件中筛选出cate类的数据
            self.cate2sort = options['ques_cate']
        except KeyError:
            self.cate2sort = None

        (folder_name, self.name) = os.path.split(folderpath)

        self.folder_path = folderpath
        print(folder_name, self.name)

        # 包含的是所有json文件的文件名(不是绝对路径,os.path.join(self.folder_path,self.filenames[i])才是绝对路径)
        self.filenames = self.__dirPath__()
        self.filenames.sort()
        print(self.filenames)
        # self.data[i]对应的是一个[category,title,desc]的list
        self.df_all, self.data_num = self.__read_data__()

    def __dirPath__(self):
        file_list = None
        try:
            file_list = os.listdir(self.folder_path)  # 返回的不是绝对路径
        except IOError as err:
            print('IOError: ' + err.filename)
        return file_list

    def __read_data__(self):

        def get_type(category):
            '''

            :param category: str 输入的问答的分类信息
            :return: 如果str中含有‘教育’ 则返回_EDU_RELATE_ 否则返回0
            '''
            if category.find('教育') > -1:
                return const._EDU_RELATE
            return 0

        def get_str(str, placewith=''):
            '''

            :param str: str 输入的字符串
            :param placewith: str 把str中的'\r\n' '\r' '\n' 替换为placewith
            :return: str中的'\r\n'替换成placewith得到的字符串
            '''
            # str = str.replace('\r', '')
            str = str.replace('\r\n', placewith)
            str = str.replace('\r', placewith)
            str = str.replace('\n', placewith)
            return str

        def array_concat(start, end):
            if start is None:
                return np.array(end)
            else:
                return np.concatenate((start, np.array(end)))

        def read_json(save_path, file_name=self.filenames, sort=False, cate=None):
            '''

            :param save_path: str 存储csv文件的路径
            :param file_name: list 默认为None，则读取self.filenames中的所有文件，否则只读取file_name中包含的json文件
                                file_name[i]只能是self.folder_path下的文件 并且只包含文件名和后缀
            :param sort: boolean 如果为True 则只读取cate指定的某些category的数据 否则读取所有category的数据
            :param cate: int 只有sort为True才有效 cate为None则默认只读取分类中含“教育”的数据 否则读取cate指定的类
            :return: 将数据存储到csv文件中 file_name中所有的json文件对应一个csv文件或多个csv文件
            '''
            cate_list = []
            if sort == True:
                if cate == None:
                    cate_list.append(const._EDU_RELATE)
                else:
                    cate_list.append(cate)

            all_title = all_desc = all_cate = None

            data_num = 0

            for filename in file_name:
                if os.path.isdir(os.path.join(self.folder_path, filename)):
                    continue
                filepath = os.path.join(self.folder_path, filename)
                try:
                    load_file = open(filepath, 'r', encoding='utf-8')
                except UnicodeDecodeError as e:
                    print('This transformer data is not utf-8 encoded.', e)
                    load_file = open(filepath, 'r', encoding='gbk')

                title = []
                cate = []
                desc = []

                for line in load_file.readlines():
                    data = json.loads(line)

                    ques_type = get_type(data[const._CATE_KEY])
                    if sort == True and ques_type not in cate_list:
                        continue

                    if data[const._CATE_KEY] == '' or data[const._TITLE_KEY] == '':
                        continue

                    title.append(get_str(data[const._TITLE_KEY],placewith=' '))
                    cate.append(get_str(data[const._CATE_KEY],placewith=' '))
                    desc.append(get_str(data[const._DESC_KEY],placewith=' '))

                    data_num += 1

                all_title = array_concat(all_title, title)
                all_desc = array_concat(all_desc, desc)
                all_cate = array_concat(all_cate, cate)
                '''
                if sort == True and data_num == 1:
                    np.append(all_cate,cate_list)
                elif sort == False:
                    all_cate = np.concatenate((np.array(cate),all_cate))
                '''

            result = pd.DataFrame()
            result[const._TITLE_COLUMN] = all_title
            result[const._CATE_COLUMN] = all_cate
            result[const._DESC_COLUMN] = all_desc

            if self.save2csv == True:
                result.to_csv(save_path, index=False, encoding='utf-8')

            return result, data_num

        if self.separate == False:
            save_path = r'./rawdata/baike_sorted/_%s.csv' % (self.name)
            df_result, data_num = read_json(save_path=save_path, sort=self.sort, cate=self.cate2sort)
            # print(type(df_result['title']))

        else:
            # 如果要将self.filenames下的json文件分开存储
            df_result = None
            data_num = file_num = 0
            for files in self.filenames:
                (name, extension) = os.path.splitext(files)
                save_path = r'./rawdata/baike_sorted/_%s_%d.csv' % (name,file_num)
                df_separate, data_num_sepa = read_json(file_name=[files], save_path=save_path, sort=self.sort, cate=self.cate2sort)

                if df_result is None:
                    df_result = df_separate
                    # print(type(df_result['title']))
                else:
                    df_result = pd.concat([df_result, df_separate], axis=0).reset_index(drop=True)
                    # print(type(df_result['title']))

                data_num += data_num_sepa

                file_num += 1

        return df_result, data_num

    def get_title(self):
        # print(self.df_all['title'].shape)
        return self.df_all[const._TITLE_COLUMN]

    def get_desc(self):
        # print(self.df_all['desc'].shape)
        return self.df_all[const._DESC_COLUMN]


if __name__ == '__main__':
    options = {"ques_save": True, "ques_separate": False, "ques_sort": True, "ques_cate": None}

    baike = Baike('./rawdata/baike_qa2019', **options)
    print(baike.data_num)