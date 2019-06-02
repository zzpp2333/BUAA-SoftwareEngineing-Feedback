from django.db import models
from users.models import User
# Create your models here.


class Courses(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=50)
    is_valid = models.BooleanField()
    details = models.CharField(max_length=1000)
    course_time = models.CharField(max_length=200)
    course_loc = models.CharField(max_length=200)
    teacher_name = models.CharField(max_length=200)


class CourseUsers(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='course_user')
    cid = models.ManyToManyField(Courses, name='course', related_name='users')


class Assistants(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='course_assistant')
    cid = models.ManyToManyField(Courses, name='course', related_name='assistants')


class AssistantApplication(models.Model):
    id = models.AutoField(primary_key=True)
    cid = models.ForeignKey(Courses, on_delete=models.CASCADE, name='course', related_name='assistant_applications')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, name='user', related_name='assistant_applications')


# class Students(models.Model):
#     id = models.AutoField(primary_key=True)
#     test = models.CharField(max_length=20)
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='course_link')
#     cid = models.ManyToManyField(to='Courses', name='s_course')
#
#
# class Assistants(models.Model):
#     id = models.AutoField(primary_key=True)
#     what = models.CharField(max_length=20)
#     cid = models.ManyToManyField(to='Courses', name='a_course')
