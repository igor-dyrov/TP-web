# Generated by Django 2.0.2 on 2018-03-28 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_answer_correct'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='num_of_ans',
            field=models.IntegerField(default=0),
        ),
    ]