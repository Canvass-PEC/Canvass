# Generated by Django 2.1 on 2018-10-14 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0003_auto_20181014_0505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='activity_type',
            field=models.CharField(choices=[('L', 'Like'), ('U', 'Up Vote Answer'), ('D', 'Down Vote Answer'), ('E', 'Down Vote Article'), ('V', 'Up Vote Article')], max_length=1),
        ),
    ]
