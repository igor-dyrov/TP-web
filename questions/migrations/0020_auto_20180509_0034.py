# Generated by Django 2.0.2 on 2018-05-08 21:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions', '0019_auto_20180508_2236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='question',
        ),
        migrations.AddField(
            model_name='like',
            name='q_id',
            field=models.IntegerField(default=0),
        ),
        migrations.RemoveField(
            model_name='like',
            name='user',
        ),
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ManyToManyField(related_query_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
