# Generated by Django 2.2 on 2019-05-14 14:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import resource.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('resource_id', models.AutoField(primary_key=True, serialize=False)),
                ('coid', models.IntegerField(default=0)),
                ('resource_name', models.CharField(max_length=100)),
                ('filepath', models.FileField(upload_to=resource.models.user_directory_path)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resource', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]