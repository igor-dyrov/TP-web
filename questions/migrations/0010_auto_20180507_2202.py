# Generated by Django 2.0.2 on 2018-05-07 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0009_auto_20180507_2201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='question',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='tags', related_query_name='tag', to='questions.Question'),
        ),
    ]
