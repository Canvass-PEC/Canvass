# Generated by Django 2.1 on 2018-10-15 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0008_articlecomment_likes'),
        ('activity', '0006_activity_article_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='article.ArticleComment'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('L', 'Liked'), ('E', 'Liked'), ('C', 'Commented'), ('U', 'Upvoted Answer'), ('D', 'Downvoted Answer'), ('R', 'Upvoted Article'), ('T', 'Downvoted Article'), ('A', 'Answered'), ('S', 'Also Commented')], max_length=1),
        ),
    ]
