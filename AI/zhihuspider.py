from zhihu_oauth import ZhihuClient
from zhihu_oauth import *
import os

def create_token(tokenpath):
    '''

    :param tokenpath: 存储token的路径
    :return: 用户通过终端登录后 即生成token 并返回对应的client对象
    '''
    client = ZhihuClient()
    client.create_token(tokenpath)
    return client

def login_with_token(tokenpath):
    '''

    :param tokenpath: 已生成的token的路径
    :return: 通过token文件登录 并返回对应的client对象
    '''
    client = ZhihuClient()
    client.load_token(tokenpath)
    return client

def check_existance(filepath):
    if os.path.exists(filepath):
        print("already get the data")
        return True

def save2file(target,filepath,mode='.html'):
    '''
    :param filepath: 文件夹的路径 默认存在filepath下的子文件夹下 子文件夹以target的title命名
    :param target: 只能是Answer/Article/Question
    :param mode: 存储文件的后缀 .html .md .markdown .txt
    :return:
    '''
    if isinstance(target, Answer):
        question = target.question
        full_path = filepath + '/' + question.title
        if check_existance(full_path):
            return
        for allans in question.answers:
            allans.save(path=full_path, mode=mode)
    elif isinstance(target, Article):
        full_path = filepath + '/' + target.title
        if check_existance(full_path):
            return
        target.save(path=full_path, mode=mode)
    elif isinstance(target, Question):
        for allans in target.answers:
            full_path = filepath + '/' + target.title
            if check_existance(full_path):
                return
            allans.save(path=full_path, mode=mode)
    else:
        #综合搜索出来的话题(Topic)内容太多太杂因此不使用
        try:
            print("unsolved object with %s type and '%s' title" % (type(target), target.title))
        except AttributeError:
            print("unsolved object with %s type and '%s' title" % (type(target), target.name))


def spider_with_questionlist(client,filepath,questionid):
    for ques in questionid:
        question = client.question(ques)

        print(question.title)

        filepath = filepath + '/' + question.title
        # 重新运行最好把原来的文件夹删了 或者 改一下文件夹名 不然会有重复文件
        # 默认保存在当前目录下 每个问题的所有答案存在以问题名命名的文件夹下
        for ans in question.answers:
            ans.save(path=filepath, mode='.txt')
            # print(ans.content)

def spider_with_searchunfold(client,query,folderpath):
    #用封装过的search_unfold方法来搜索
    for result in client.search_unfold(query):
        r = result
        save2file(r,filepath=folderpath,mode='.txt')
        print('-'*20)

def spider_with_searching(client,query,folderpath,searchtype):
    '''

    :param query: str 查询语句 最好不要太多连续空格 不然会被替换成连续的_
    :param searchtype: SearchType.GENERAL
    :return:
    '''
    for result in client.search(query, searchtype):
        if isinstance(result, SearchResultSection):
            print(result.type, "search result list:")
            for ans in result:
                save2file(ans.obj,filepath=folderpath,mode='.txt')
        else:
            r = result
            save2file(r.obj,filepath=folderpath,mode='.txt')
        print('-' * 20)

if __name__ == "__main__":
    #第一次登录应该将以下语句换成 #client = create_token('token.pkl')
    client = login_with_token('token.pkl')

    # 这个情况一般是命中了知乎的反爬虫逻辑:
    #requests.exceptions.RetryError: HTTPSConnectionPool(host='api.zhihu.com', port=443): Max retries exceeded with url: /search_v3... (Caused by ResponseError('too many 403 error responses',))
    # 打开知乎网址 它会提示你网络安全存在异常 进行安全验证再重新运行代码就好了
    # save2file会自动判断目标目录是否存在 存在就不再爬取 只爬取上次异常时未爬取的任务

    #使用client.search方法爬取数据
    query = '如何评价 课程'
    folderpath = './rawdata/zhihu/' + query.replace(' ', '_')
    spider_with_searching(client=client,query=query,folderpath=folderpath,searchtype=SearchType.GENERAL)
    #也可以提供要爬取的问题列表 按照列表爬取数据
    #例如问题的url是https://www.zhihu.com/question/58685007  问题的id就是58685007
    '''
    questionid=[22289658, #如何评价沪江网校？课程质量如何？
            28661807, #如何评价思修课
            58685007, #如何评价唯库上面的课程？
            68701341, #如何评价目前本科计算机课程体系
            22437266, #如何评价哈佛大学公开课：幸福课？
            28804633, #如何评价有些大学老师上课异常严格
            59933203, #如何评价金旭亮老师的《如何自学计算机专业课程》的live
            315529252, #如何评价华南师范大学2017级的非正式课程修不够40学时无法毕业
            58430865, #如何评价《Crash Course》系列课程
            277938449, #如何评价三节课里的运营体系的课程
            65841239, #如何评价知乎私家课？
            59515745, #如何评价有道精品课？
            34921712, #如何评价NLP课程？
            ]
    spider_with_questionlist(client=client,fliepath='./rawdata/zhihu/',questionid=questionid)
    '''

'''
for result in client.search('如何评价 课程',SearchType.GENERAL):
    if isinstance(result,SearchResultSection):
        print(result.type,"search result list:")
        for ans in result:

    else:
        r = result
        print(r.highlight_title,r.highlight_desc)
        print(r.obj)
    print('-'*20)
'''


