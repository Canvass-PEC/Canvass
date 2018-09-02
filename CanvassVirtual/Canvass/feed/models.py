from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from activity.models import Activity

class Feed(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    post = models.TextField(max_length=255)
    parent = models.ForeignKey('Feed', null=True, blank=True,on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Feed'
        verbose_name_plural = 'Feeds'
        ordering = ('-date',)

    def __unicode__(self):
        return self.post

    @staticmethod
    def get_feeds(from_feed=None):
        if from_feed is not None:
            feeds = Feed.objects.filter(parent=None, id__lte=from_feed)
        else:
            feeds = Feed.objects.filter(parent=None)
        return feeds

    @staticmethod
    def get_feeds_after(feed):
        feeds = Feed.objects.filter(parent=None, id__gt=feed)
        return feeds

    def get_comments(self):
        return Feed.objects.filter(parent=self)

    def calculate_likes(self):
        likes = Activity.objects.filter(activity_type=Activity.LIKE, feed=self.pk).count()
        self.likes = likes
        self.save()
        return self.likes

    def get_likers(self):
        likes = Activity.objects.filter(activity_type=Activity.LIKE, feed=self.pk)
        likers = []
        for like in likes:
            likers.append(like.user)
        return likers

    def do_comment(self, user, post):
        comment = Feed(user=user, post=post, parent=self)
        comment.save()
        self.comments = Feed.objects.filter(parent=self).count()
        self.save()
        return self.comments
