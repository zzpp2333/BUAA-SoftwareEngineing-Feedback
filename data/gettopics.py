import MySQLdb
import json


def getUnclassified(filename, filename2):
    db = MySQLdb.connect("localhost", "root", "Bro.2019", "ISFSDB", charset='utf8')

    cursor = db.cursor()

    sql = "select id, title, content from forum_topic  where emotion = -2;"

    cursor.execute(sql)

    results = cursor.fetchall()

    # print(results)

    topics = []

    for r in results:
        topic = {}
        topic['id'] = r[0]
        topic['title'] = r[1]
        topic['content'] = r[2]
        topics.append(topic)
    # print(topics)

    f = open(filename, 'w+')

    json.dump(topics, f)

    sql = "select id, title, content from forum_topic;"

    cursor.execute(sql)

    results = cursor.fetchall()

    topics = []

    for r in results:
        topic = {}
        topic['id'] = r[0]
        topic['title'] = r[1]
        topic['content'] = r[2]
        topics.append(topic)

    f = open(filename2, 'w+')

    json.dump(topics, f)


getUnclassified('topics.json', 'alltopics.json')
# renew('topics.json')