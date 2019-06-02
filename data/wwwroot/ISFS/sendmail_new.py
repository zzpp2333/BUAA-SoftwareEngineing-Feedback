import time
import datetime
import smtplib
import random
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

# 
mail_host = "smtp.163.com"
mail_user = "wxxxzhang@163.com"
mail_pass = "zhang1228"

mail_port = 465

sender = 'wxxxzhang@163.com'
from_id = '个性化反馈'

# 邮件的发件人显示为 from_id<sender>
# 收件人显示为 rece_id<receiver>
# 标题：subject
# 正文：MIMEText(text,'plain','utf-8')

def send_mail(receivers,message):
    '''

    :param receivers: list
    :param message: MIMEText、MIMEMultipart
    :return:
    '''
    try:
        # smtpObj = smtplib.SMTP()
        # smtpObj.connect(mail_host,mail_port)
        smtpObj = smtplib.SMTP_SSL(mail_host, mail_port)
        smtpObj.ehlo()
        smtpObj.login(mail_user, mail_pass)
        # print(message.as_string())
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("发送成功")
    except smtplib.SMTPException:
        print("发送失败")

def get_notestr(alarm_type):
    '''

    :param alarm_type: int(1/2/3) 1-->提问 2-->正面评价 3-->负面吐槽
    :return: str 对应的提示字段
    '''
    if alarm_type == 1:
        note = '新的提问'
    elif alarm_type == 2:
        note = '一条正面评价'
    else:
        note = '一条负面吐槽'
    return note

def get_cache():
    veri_num = 0
    for i in range(4):
        veri_num = 10*veri_num + random.randint(0,9)
    return veri_num

def send_plain_text(rece_mail, subject, text, rece_id=''):
    '''

    :param rece_mail: str 收件人的邮箱
    :param rece_id: str 标识收件人的字符串 如'教师/助教'、'学生'、'教务管理人员'等 默认''
    :param subject: str 邮箱标题
    :param text: str 邮件正文
    :return:
    '''
    message = MIMEText(text,'plain','utf-8')
    message['From'] = formataddr([from_id,sender])
    message['To'] = formataddr([rece_id,rece_mail])
    message['Subject'] = subject

    send_mail([rece_mail], message)

def send_cache(rece_mail):
    '''

    :param rece_mail: str 收件人的邮箱
    :return: str 正确的四位数字验证码
    '''
    cache = (str)(get_cache())
    message = MIMEText('您的验证码为'+cache, 'plain', 'utf-8')
    message['From'] = formataddr([from_id, sender])
    message['To'] = formataddr(['', rece_mail])
    message['Subject'] = '验证码'

    send_mail([rece_mail],message)
    return cache

def send_alarm_with_url(rece_mail, class_name, alarm_type, title, alarm_url, rece_id=''):
    '''

    :param rece_mail: str 收件人的邮箱
    :param class_name: str 课程名
    :param alarm_type: int(1/2/3) 提醒类型
    :param title: str 新帖子的标题
    :param alarm_url: str 新帖子的链接
    :param rece_id: str 标识收件人的字符串
    :return:
    '''
    note = get_notestr(alarm_type)
    mail_msg = r"""
        <p>您的课程"%s"课程收到了%s，点击链接查看：</p>
        <p><a href="%s">%s</a></p>
        """%(class_name, note, alarm_url, title)
    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = formataddr([from_id, sender])
    message['To'] = formataddr([rece_id, rece_mail])
    message['Subject'] = r'您的课程"%s"收到了%s'%(class_name, note)
    send_mail([rece_mail], message)

def send_with_attach(rece_mail, subject, messagebody, attachments, rece_id=''):
    '''

    :param rece_mail: str 收件人的邮箱
    :param subject: str 邮件标题
    :param messagebody: str 邮件正文
    :param attachments: list 附件的文件名的列表
    :param rece_id: str 标识收件人的字符串
    :return:
    '''
    message = MIMEMultipart()
    message['From'] = formataddr([from_id, sender])
    message['To'] = formataddr([rece_id, rece_mail])
    message['Subject'] = subject
    # 邮件正文
    message.attach(MIMEText(messagebody,'plain','utf-8'))
    for filename in attachments:
        # 附件
        att = MIMEText(open(filename,'rb').read(), 'base64', 'utf-8')
        att['Content-Type'] = 'application/octet-stream'
        # 此处的filename可以任意写 写什么邮件中显示什么
        att['Content-Disposition'] = r'attachment; filename="%s"'%(filename)
        message.attach(att)
    
    send_mail([rece_mail],message)

def send_ddl_alarm(receivers, ddl, class_name, homework, rece_id=''):
    '''

    :param receivers: str 收件人的邮箱
    :param ddl: str 截止日期
    :param class_name: str 课程名
    :param homework: str 作业名
    :param rece_id: str 标识收件人的字符串
    :return:
    '''
    aDayAgo = (datetime.datetime.strptime(ddl, "%Y-%m-%d %H:%M:%S") - datetime.timedelta(days=1))
    timeStamp = int(aDayAgo.timestamp())
    time_cur = int(time.time())
    deltatime = timeStamp - time_cur
    if deltatime > 0:
        time.sleep(deltatime)
    for rece in receivers:
     send_plain_text(rece, '作业提醒', r'你的“%s”课程的作业“%s”即将截止，请及时提交'%(class_name,homework), rece_id)

if __name__ == '__main__':
    t = "2019-05-04 15:55:00"
    send_ddl_alarm(['wxxxzhang@163.com','16061121@buaa.edu.cn'], t, "数据结构", "作业四：栈与队列", "学生甲")

    '''
    receivers = ['wxxxzhang@163.com']
    
    for rece in receivers:
        send_plain_text(rece, '账号分配结果',
                    '感谢贵校选择我们平台，为您分配的账号为：123455，密码为：000000，登录后请及时修改密码！', '教务管理人员')
        send_plain_text(rece, '反馈结果',
                    '您的课程“面向对象”的作业10反馈结果已出，请及时查看！', '学生')
        # send_with_attach(rece,'账号分配结果2',
        #                  '感谢贵校选择我们平台，请在附件中查看为您分配的教务管理人员账号，登录后请及时修改密码！',['test.txt','test2.png'],'教务管理人员')
        send_alarm_with_url(rece,'面向对象',1,'请问这道题答案是不是有问题？','http://www.runoob.com','教师/助教')
        cache = send_cache(rece)
        print(cache)
    '''
