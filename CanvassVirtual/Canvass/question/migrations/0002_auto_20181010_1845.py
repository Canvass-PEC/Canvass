# Generated by Django 2.1 on 2018-10-10 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ('-votes', 'create_date'), 'verbose_name': 'Answer', 'verbose_name_plural': 'Answers'},
        ),
        migrations.RemoveField(
            model_name='answer',
            name='is_accepted',
        ),
    ]