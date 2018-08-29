from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
User=get_user_model()

class Question(models.Model):
    user=models.ForeignKey(User,null=False,on_delete="CASCADE")
    title=models.CharField(max_length=250)
    description=models.TextField(max_length=1000,null=False,blank=False)
    created_on=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-created_on']

    def __str__(self):
        return "{} \n Asked by:{}".format(self.title,self.asked_by.user)

class Answer(models.Model):
    user=models.ForeignKey(User,null=False,on_delete="CASCADE")
    question=models.ForeignKey(Question,on_delete="CASCADE")
    description=models.TextField(null=False,blank=False)
    created_on=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-created_on']

    def __str__(self):
        return "{} answered {}".format(self.user.username,self.question.title)
