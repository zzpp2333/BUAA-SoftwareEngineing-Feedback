import MySQLdb
import json


def renew(filename):
    f = open(filename, 'r')
    topics = json.load(f)
    print(topics)

    db = MySQLdb.connect("localhost", "root", "Bro.2019", "ISFSDB", charset='utf8')

    cursor = db.cursor()

    for topic in topics:
        try:
            sql = 'update forum_topic set emotion=%d where id = %d' % (topic['emotion'], topic['id'])
            cursor.execute(sql)
            db.commit()
            print(topic)
            print(type('%s'%topic['classification']))
        except:
            db.rollback()

        try:
            sql = 'update forum_topic set classification="%s" where id = %d' % (topic['classification'], topic['id'])
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()


renew('new.json')