from django.db import models
import django.utils.timezone as timezone
from users.models import User


# Create your models here
class Todolist(models.Model):
    list_id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=1000)
    list_time = models.DateTimeField(default="2000-01-01 00:00:00")
    is_valid = models.BooleanField(default=0)
    # 1表示已完�?0表示未完�?
    author_id = models.ForeignKey(User, on_delete=models.CASCADE, name='author', related_name='todolist')

