# Generated by Django 2.1 on 2018-10-14 05:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20181014_0513'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='down_votes',
            new_name='downvotes',
        ),
    ]
