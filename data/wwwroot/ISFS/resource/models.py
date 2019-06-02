from django.db import models
from users.models import User
# Create your models here


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/resource/user_<id>/<filename>
    return 'resource/user_{0}/{1}'.format(instance.author_id, filename)


class Resource(models.Model):
    resource_id = models.AutoField(primary_key=True)
    author_id = models.ForeignKey(User, on_delete=models.CASCADE, name='author', related_name='resource')
    coid = models.IntegerField(default=0)
    resource_name = models.CharField(max_length=100)
    filepath = models.FileField(upload_to=user_directory_path)

