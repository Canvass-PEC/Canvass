from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User=get_user_model()

class Article(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    description=models.TextField(null=False)
    created_on=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-created_on']

    def __str__(self):
        return "{} Written by {}".format(self.title,self.user.username)