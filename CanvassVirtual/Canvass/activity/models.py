from django.db import models
from django.contrib.auth.models import User

class Activity(models.Model):
    LIKE = 'L'
    UP_VOTE = 'U'
    DOWN_VOTE = 'D'
    ACTIVITY_TYPES = (
        (LIKE, 'Like'),
        (UP_VOTE, 'Up Vote'),
        (DOWN_VOTE, 'Down Vote'),
    )

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    feed = models.IntegerField(null=True, blank=True)
    question = models.IntegerField(null=True, blank=True)
    answer = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"

    def __unicode__(self):
        return self.activity_type