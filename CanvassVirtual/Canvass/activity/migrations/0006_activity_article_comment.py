# Generated by Django 2.1 on 2018-10-15 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0005_auto_20181014_1017'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='article_comment',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
