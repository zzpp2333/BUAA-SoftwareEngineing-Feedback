# Generated by Django 2.2 on 2019-05-19 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailCache',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('cache', models.CharField(max_length=10)),
                ('time', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
