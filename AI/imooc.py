from selenium import webdriver
from time import sleep
import os
import re
import pandas as pd
from bs4 import BeautifulSoup  #executable_path为chromedriver.exe的解压安装目录，需要与chrome浏览器同一文件夹下
from classify.utils import const

driver=webdriver.Chrome(executable_path="C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe")

def process_enter(str,placewith=''):
    str = str.replace('\r\n',placewith)
    str = str.replace('\r',placewith)
    str = str.replace('\n',placewith)
    #str = str+'\n'
    return str

def get_comments_by_url(url):
    #url='https://www.icourse163.org/course/BIT-268001'   #爬取Python语言程序设计为例
    driver.get(url)
    cont=driver.page_source             #获得初始页面代码，接下来进行简单的解析
    soup=BeautifulSoup(cont,'html.parser')
    #print(soup)
    ele=driver.find_element_by_id("review-tag-button")  #模仿浏览器就行点击查看课程评价的功能
    ele.click()                      #上边的id，下边的classname都可以在源码中看到（首选火狐，谷歌）

    tagnum = driver.find_element_by_id("review-tag-num")
    review_num = int(tagnum.text[1:-1])

    xyy=driver.find_element_by_class_name("ux-pager_btn__next")#翻页功能，类名不能有空格，有空格可取后边的部分
    connt=driver.page_source
    soup=BeautifulSoup(connt,'html.parser')
    #print(soup)
    acontent=[]         #n页的总评论
    content=soup.find_all('div',{'class':'ux-mooc-comment-course-comment_comment-list_item_body_content'})#包含全部评论项目的总表标签
    #print(content)
    reviews = 0
    for ctt in content:       #第一页评论的爬取
        scontent=[]
        aspan=ctt.find_all('span') #刚获得一页中的content中每一项评论还有少量标签
        for span in aspan:
            scontent.append(span.string)#只要span标签里边的评论内容
        reviews += len(scontent)
        acontent.append(scontent) #将一页中的一条评论加到总评论列表里，知道该页加完
    print(reviews)
    #print(acontent)
    #print(len(acontent))
    #for i in range(287): #翻页 286-0+1次，也就是287次，第一页打开就是，上边读完第一页了
    while reviews <= review_num:
        xyy.click()
        connt = driver.page_source
        soup = BeautifulSoup(connt,'html.parser')
        content = soup.find_all('div',{'class': 'ux-mooc-comment-course-comment_comment-list_item_body_content'})  # 包含全部评论项目的总表标签
        for ctt in content:
            scontent = []
            aspan = ctt.find_all('span')
            for span in aspan:
                scontent.append(span.string)
            reviews += len(scontent)
            acontent.append(scontent)
    #print(acontent)
    print('--------get %d reviews from %s --------'%(reviews,url))

    comments = []
    for strlist in acontent:
        for comm in strlist:
            comments.append(process_enter(comm,placewith=' '))

    return comments

    '''
    with open(save_path,"w",encoding='utf-8') as f:
        for strlist in acontent:
            for comm in strlist:
                f.writelines(process_enter(comm,placewith=' '))
    '''

    print('--------saved at %s--------'%(save_path))

def get_comments_by_urllist(urllist, save_path):
    comments = []

    for url in urllist:
        temp = get_comments_by_url(url)
        comments.extend(temp)

    df_result = pd.DataFrame()
    df_result[const._COMMENT_COLUMN] = comments
    df_result.to_csv(save_path, index=False, encoding='utf-8')

if __name__ == '__main__':
    # url = 'https://www.icourse163.org/course/BIT-268001'  # 爬取Python语言程序设计为例
    # url = 'https://www.icourse163.org/course/-47004'
    urllist = ['https://www.icourse163.org/course/BIT-268001', 'https://www.icourse163.org/course/-47004']
    save_path = './rawdata/imooc_all.csv'
    get_comments_by_urllist(urllist,save_path)
#print(acontent)