# Generated by Django 2.1 on 2018-08-29 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0002_auto_20180827_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='description',
            field=models.TextField(max_length=1000),
        ),
    ]
