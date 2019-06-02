from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import Topic, Reply
from course.models import Courses
from django.contrib.auth.models import User
from datetime import datetime, date
# from AI.predict import get_classification, get_emotion
from AI.Similarity import Similarity_function


# Create your views here.
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def createtopic(request):
    if request.method == 'POST':
        course_id = request.POST['course_id']
        user = request.user
        title = request.POST['title']
        content = request.POST['content']
        # classification = get_classification([title])[0]
        # print(title)
        # print(classification)
        # if classification == 'comment':
        #     emotion = get_emotion([title])[0]
        # else:
        #     emotion = 0

        classification = 0
        emotion = 0

        topic = Topic(course_id=course_id, author=user, title=title, content=content, classification=classification, emotion=emotion)
        topic.save()
        return HttpResponse(json.dumps({'success': True}), content_type='application/json')
    return render(request, 'forum/testcreate.html')


def gettopics(request):
    if request.method == 'GET':
        course_id = request.GET['course_id']
        # course_id = 10

        course = Courses.objects.get(course_id=course_id)

        topics = course.topics.values('id', 'title', 'author_id', 'cre_date', 'mod_date', 'reply_count', 'star', 'classification', 'emotion')

        topics = list(topics)

        for topic in topics:
            topic['author_username'] = User.objects.get(id=topic['author_id']).username

        return HttpResponse(json.dumps(topics, cls=CJsonEncoder), content_type='application/json')
    return


def getreplies(request):
    if request.method == 'GET':
        topic_id = request.GET['topic_id']
        # topic_id = 3

        topic = Topic.objects.get(id=topic_id)

        replies = topic.replies.values('author_id', 'time', 'replyto', 'content')
        for reply in replies:
            reply['author_username'] = User.objects.get(id=reply['author_id']).username

        data = {
            'id': topic_id,
            'title': topic.title,
            'author': topic.author.username,
            'cre_date': topic.cre_date,
            'mod_date': topic.mod_date,
            'reply_count': topic.reply_count,
            'content': topic.content,
            'star': topic.star,
            'classification': topic.classification,
            'emotion': topic.emotion,
            'replies': list(replies)
        }

        return HttpResponse(json.dumps(data, cls=CJsonEncoder), content_type='application/json')
    return


def reply(request):
    if request.method == 'POST':
        topic_id = request.POST['topic_id']
        author = User.objects.get(id=request.user.id)
        replyto = request.POST['replyto']
        content = request.POST['content']

        topic = Topic.objects.get(id=topic_id)
        topic.reply_count = topic.reply_count+1
        topic.save()

        reply = Reply(topic=topic, author=author, replyto=replyto, content=content)
        reply.save()

        return HttpResponse(json.dumps({'success': True}), content_type='application/json')

    return render(request, 'forum/testreply.html')
#
#
# def getalltopics():
#     course_id = 10
#
#     course = Courses.objects.get(course_id=course_id)
#
#     topics = course.topics.values('id', 'title', 'content')
#
#     topics = list(topics)
#
#     with open("test.json", "w") as f:
#         json.dump(topics, f)


def getSimilarTopics(request):
    if request.method == 'GET':
        title = request.GET['title']
        data = Topic.objects.values('id', 'title', 'content')
        # print(json.dumps(list(data)))

        simi_model = Similarity_function('AI/hlp_stop_words.txt', title, json.dumps(list(data)))
        simi_model.getkeywords()
        index = simi_model.getmostsimilar()

        similartopics = Topic.objects.filter(id__in=[index]).values('id', 'title', 'author_id', 'cre_date', 'mod_date', 'reply_count', 'star', 'classification', 'emotion')

        return HttpResponse(json.dumps(list(similartopics), cls=CJsonEncoder), content_type='application/json')