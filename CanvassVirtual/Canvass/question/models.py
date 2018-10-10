from django.db import models
from django.contrib.auth.models import User
from activity.models import Activity
import markdown


class Question(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=2000)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = ('-update_date',)

    def __str__(self):
        return self.title

    @staticmethod
    def get_unanswered():
        return Question.objects.filter(has_accepted_answer=False)

    @staticmethod
    def get_answered():
        return Question.objects.filter(has_accepted_answer=True)

    def get_answers(self):
        return Answer.objects.filter(question=self)

    def get_answers_count(self):
        return Answer.objects.filter(question=self).count()


    def get_description_as_markdown(self):
        return markdown.markdown(self.description, safe_mode='escape')

    def get_description_preview(self):
        if len(self.description) > 255:
            return u'{0}...'.format(self.description[:255])
        else:
            return self.description

    def get_description_preview_as_markdown(self):
        return markdown.markdown(self.get_description_preview(), safe_mode='escape')



class Answer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    description = models.TextField(max_length=2000)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(null=True, blank=True)
    votes = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'
        ordering = ('-votes', 'create_date',)

    def __str__(self):
        return self.description


    def calculate_votes(self):
        up_votes = Activity.objects.filter(activity_type=Activity.UP_VOTE, answer=self.pk).count()
        down_votes = Activity.objects.filter(activity_type=Activity.DOWN_VOTE, answer=self.pk).count()
        self.votes = up_votes - down_votes
        self.save()
        return self.votes

    def get_up_voters(self):
        votes = Activity.objects.filter(activity_type=Activity.UP_VOTE, answer=self.pk)
        voters = []
        for vote in votes:
            voters.append(vote.user)
        return voters

    def get_down_voters(self):
        votes = Activity.objects.filter(activity_type=Activity.DOWN_VOTE, answer=self.pk)
        voters = []
        for vote in votes:
            voters.append(vote.user)
        return voters

    def get_description_as_markdown(self):
        return markdown.markdown(self.description, safe_mode='escape')

