import MySQLdb
import json
import sendmail_new

def send(filename):
    f = open(filename, 'r')

    topics = json.load(f)

    for t in topics:
        m_id = int(t['id'])
        m_title = t['title']

        sim_t = list(t['similar'])

        i = len(sim_t)-1
        while i >= 0:
            st = sim_t[i]
            # print(st)
            if not ofSameCourse(m_id, int(st['id'])):
                sim_t.remove(st)
            # else:
                # print(m_id)
                # print(int(st['id']))
            i -= 1
        # print(sim_t)
        if len(sim_t) > 0:
            strs = []
            for st in sim_t:
                strs.append(st['title'])
            string = '、'.join(strs)

            subject = r'检测到您的提问"%s"的相似问题' % (m_title)
            text = r'''
                            您的提问"%s"有相似问题，仅供参考：
                            %s
                            ''' % (m_title, string)

            sendmail_new.send_plain_text(getEmail(m_id), subject, text)
            print(text)
            print(getEmail(m_id))



def getEmail(topic_id):
    db = MySQLdb.connect("localhost", "root", "Bro.2019", "ISFSDB", charset='utf8')

    cursor = db.cursor()

    sql = 'select author_id from forum_topic where id = %d' % (topic_id)
    cursor.execute(sql)
    results = cursor.fetchall()
    user_id = results[0][0]

    sql = 'select email from auth_user where id = %d' % (user_id)
    cursor.execute(sql)
    results = cursor.fetchall()
    email = results[0][0]

    return email



def ofSameCourse(id1, id2):
    db = MySQLdb.connect("localhost", "root", "Bro.2019", "ISFSDB", charset='utf8')

    cursor = db.cursor()

    sql = 'select course_id from forum_topic where id = %d' % (id1)
    cursor.execute(sql)
    results = cursor.fetchall()
    cid1 = results[0][0]

    sql = 'select course_id from forum_topic where id = %d' % (id2)
    cursor.execute(sql)
    results = cursor.fetchall()
    cid2 = results[0][0]

    if cid1 == cid2:
        return True
    else:
        return False


send("_new.json")
