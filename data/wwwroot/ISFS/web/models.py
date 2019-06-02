from django.db import models

# Create your models here.

class User(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=40)
    permission = models.IntegerField()


class Course(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=20)
    tid = models.CharField(max_length=20)
    tname = models.CharField(max_length=20)
    isValid = models.BinaryField(max_length=1)
