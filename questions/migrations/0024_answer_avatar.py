# Generated by Django 2.0.2 on 2018-05-11 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0023_auto_20180509_0044'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='avatar',
            field=models.ImageField(default=1, upload_to=''),
            preserve_default=False,
        ),
    ]