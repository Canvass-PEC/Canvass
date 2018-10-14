from django.db import models
from django.contrib.auth.models import User
from django.utils.html import escape

class Activity(models.Model):
    LIKE = 'L'
    UP_VOTE = 'U'
    DOWN_VOTE = 'D'
    DOWN_VOTEA = 'E'
    UP_VOTEA='V'
    ACTIVITY_TYPES = (
        (LIKE, 'Like'),
        (UP_VOTE, 'Up Vote Answer'),
        (DOWN_VOTE, 'Down Vote Answer'),
        (DOWN_VOTEA, 'Down Vote Article'),
        (UP_VOTEA, 'Up Vote Article'),
        )

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    feed = models.IntegerField(null=True, blank=True)
    question = models.IntegerField(null=True, blank=True)
    article = models.IntegerField(null=True, blank=True)
    answer = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'

    def __unicode__(self):
        return self.activity_type


class Notification(models.Model):
    LIKED = 'L'
    COMMENTED = 'C'
    ANSWERED = 'A'
    ALSO_COMMENTED = 'S'
    UPVOTED_ANSWER='U'
    DOWNVOTED_ANSWER='D'
    UPVOTED_ARTICLE='R'
    DOWNVOTED_ARTICLE='T'

    NOTIFICATION_TYPES = (
        (LIKED, 'Liked'),
        (COMMENTED, 'Commented'),
        (UPVOTED_ANSWER,'Upvoted Answer'),
        (DOWNVOTED_ANSWER,'Downvoted Answer'),
        (UPVOTED_ARTICLE,'Upvoted Article'),
        (DOWNVOTED_ARTICLE,'Downvoted Article'),
        (ANSWERED, 'Answered'),
        (ALSO_COMMENTED, 'Also Commented'),
        )

    _LIKED_TEMPLATE = u'<a href="/{0}/">{1}</a> liked your post: <a href="/feeds/{2}/">{3}</a>'
    _COMMENTED_TEMPLATE = u'<a href="/{0}/">{1}</a> commented on your post: <a href="/feeds/{2}/">{3}</a>'
    _ANSWERED_TEMPLATE = u'<a href="/{0}/">{1}</a> answered your question: <a href="/questions/{2}/">{3}</a>'
    _ALSO_COMMENTED_TEMPLATE = u'<a href="/{0}/">{1}</a> also commentend on the post: <a href="/feeds/{2}/">{3}</a>'
    _UPVOTED_ANSWER_TEMPLATE=u'<a href="/{0}/">{1}</a> upvoted your answer: <a href="/questions/{2}/">{3}</a>'
    _DOWN_VOTED_ANSWER_TEMPLATE=u'<a href="/{0}/">{1}</a> upvoted your answer: <a href="/questions/{2}/">{3}</a>'
    _UPVOTED_ARTICLE_TEMPLATE = u'<a href="/{0}/">{1}</a> upvoted your article: <a href="/article/{2}/">{3}</a>'
    _DOWNVOTED_ARTICLE_TEMPLATE = u'<a href="/{0}/">{1}</a> downvoted your article: <a href="/article/{2}/">{3}</a>'

    from_user = models.ForeignKey(User, related_name='+',on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='+',on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    feed = models.ForeignKey('feed.Feed', null=True, blank=True,on_delete=models.CASCADE)
    question = models.ForeignKey('question.Question', null=True, blank=True,on_delete=models.CASCADE)
    answer = models.ForeignKey('question.Answer', null=True, blank=True,on_delete=models.CASCADE)
    article = models.ForeignKey('article.Article', null=True, blank=True,on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=1, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ('-date',)

    def __str__(self):
        print(self.notification_type)
        if self.notification_type == self.LIKED:
            return self._LIKED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.feed.pk,
                escape(self.get_summary(self.feed.post))
                )
        elif self.notification_type == self.COMMENTED:
            return self._COMMENTED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.feed.pk,
                escape(self.get_summary(self.feed.post))
                )
        elif self.notification_type == self.ANSWERED:
            return self._ANSWERED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.question.pk,
                escape(self.get_summary(self.question.title))
                )
        elif self.notification_type == self.ALSO_COMMENTED:
            return self._ALSO_COMMENTED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.feed.pk,
                escape(self.get_summary(self.feed.post))
                )
        elif self.notification_type == self.UPVOTED_ANSWER:
            return self._UPVOTED_ANSWER_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.question.pk,
                escape(self.get_summary(self.question.title))
            )
        elif self.notification_type == self.DOWNVOTED_ANSWER:
            return self._DOWNVOTED_ANSWER_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.self.question.pk,
                escape(self.get_summary(self.question.title))
            )
        elif self.notification_type == self.UPVOTED_ARTICLE:
            return self._UPVOTED_ARTICLE_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.article.slug,
                escape(self.get_summary(self.article.title))
            )
        elif self.notification_type == self.DOWNVOTED_ARTICLE:
            return self._DOWNVOTED_ARTICLE_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.article.slug,
                escape(self.get_summary(self.article.title))
            )
        else:
            return 'Ooops! Something went wrong.'

    def get_summary(self, value):
        summary_size = 50
        if len(value) > summary_size:
            return u'{0}...'.format(value[:summary_size])
        else:
            return value