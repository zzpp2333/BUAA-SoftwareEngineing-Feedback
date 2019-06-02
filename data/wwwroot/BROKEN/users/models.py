from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')         #related_name   -->  user.profile指向UserProfile表

    permission = models.IntegerField()

    mod_date = models.DateTimeField("Last modified", auto_now=True)

    no = models.CharField(max_length=10, unique=True)

    class Meta:
        verbose_name = "User Profile"

    def __str__(self):
        return self.__str__()