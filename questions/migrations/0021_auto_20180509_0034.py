# Generated by Django 2.0.2 on 2018-05-08 21:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0020_auto_20180509_0034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='user',
            field=models.ManyToManyField(related_name='users', related_query_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
