# Generated by Django 2.1 on 2018-10-14 05:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20181013_1116'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='down_upvotes',
            new_name='down_votes',
        ),
    ]
