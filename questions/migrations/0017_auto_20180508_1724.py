# Generated by Django 2.0.2 on 2018-05-08 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0016_auto_20180508_1721'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='question',
        ),
        migrations.AddField(
            model_name='tag',
            name='question',
            field=models.ManyToManyField(related_name='tags', related_query_name='tag', to='questions.Question'),
        ),
    ]