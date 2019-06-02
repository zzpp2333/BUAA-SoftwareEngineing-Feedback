from django.db import models
from django.contrib.auth.models import User
from course.models import Courses

# Create your models here.

class Topic(models.Model):
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE, name='course', related_name='topics')
    title = models.CharField(max_length=255)
    author_id = models.ForeignKey(User, on_delete=models.CASCADE, name='author', related_name='topics')
    cre_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField(auto_now=True)
    reply_count = models.IntegerField(default=0)
    content = models.TextField()
    star = models.BooleanField(default=False)
    classification = models.CharField(max_length=20)
    emotion = models.IntegerField(default=0)


class Reply(models.Model):
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE, name='topic', related_name='replies')
    author_id = models.ForeignKey(User, on_delete=models.CASCADE, name='author', related_name='replies')
    time = models.DateTimeField(auto_now_add=True)
    replyto = models.CharField(max_length=50)
    content = models.TextField()