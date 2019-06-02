from django.db import models
from users.models import User
from course.models import Courses
import django.utils.timezone as timezone
# Create your models here


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/homework/user_<id>/<filename>
    return 'homework/user_{0}/{1}'.format(instance.author_id, filename)


class Homework(models.Model):
    homework_id = models.AutoField(primary_key=True)
    coid = models.IntegerField(default=0)
    is_valid = models.BooleanField(default=0)
    # 1表示上传者为老师 0表示上传者为学生
    author_id = models.ForeignKey(User, on_delete=models.CASCADE, name='author', related_name='homework')

    homework_name = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    filepath = models.FileField(upload_to=user_directory_path)
    num = models.IntegerField(default=0)

    grade = models.IntegerField(default=0)
    deadline = models.DateTimeField(default=timezone.now)
