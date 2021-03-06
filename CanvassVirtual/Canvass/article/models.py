from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from datetime import datetime
from django.template.defaultfilters import slugify
import markdown
from activity.models import Activity
class Article(models.Model):
    DRAFT = 'D'
    PUBLISHED = 'P'
    STATUS = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    content = models.TextField(max_length=4000)
    status = models.CharField(max_length=1, choices=STATUS, default=DRAFT)
    create_user = models.ForeignKey(User,on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True,auto_now=True)
    upvotes=models.IntegerField(default=0)
    downvotes=models.IntegerField(default=0)

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        ordering = ("-create_date",)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Article, self).save(*args, **kwargs)
        else:
            self.update_date = datetime.now()
        if not self.slug:
            slug_str = "%s %s" % (self.pk, self.title.lower())
            self.slug = slugify(slug_str)
        super(Article, self).save(*args, **kwargs)

    def get_content_as_markdown(self):
        return markdown.markdown(self.content, safe_mode='escape')

    def get_upvoters(self):
        upvotes = Activity.objects.filter(activity_type=Activity.UP_VOTEA, article=self.pk)
        upvoters=[]
        for upvoter in upvotes:
            upvoters.append(upvoter.user)
        return upvoters

    def get_downvoters(self):
        downvotes = Activity.objects.filter(activity_type=Activity.DOWN_VOTEA, article=self.pk)
        downvoters = []
        for downvoter in downvotes:
            downvoters.append(downvoter.user)
        return downvoters

    def calculate_votes(self):
        upvotes = Activity.objects.filter(activity_type=Activity.UP_VOTEA, article=self.pk).count()
        downvotes = Activity.objects.filter(activity_type=Activity.DOWN_VOTEA, article=self.pk).count()
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.save()
        return


    @staticmethod
    def get_published():
        articles = Article.objects.filter(status=Article.PUBLISHED)
        return articles

    def get_upvotes(self):
        return self.upvotes


    def get_downvotes(self):
        return self.downvotes

    def get_summary(self):
        if len(self.content) > 255:
            return u'{0}...'.format(self.content[:255])
        else:
            return self.content

    def get_summary_as_markdown(self):
        return markdown.markdown(self.get_summary(), safe_mode='escape')

    def get_comments(self):
        return ArticleComment.objects.filter(article=self)


class ArticleComment(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    likes=models.IntegerField(blank=True,default=0)
    class Meta:
        verbose_name = _("Article Comment")
        verbose_name_plural = _("Article Comments")
        ordering = ("date",)

    def __str__(self):
        return u'{0} - {1}'.format(self.user.username, self.article.title)

    def calculate_likes(self):
        likes = Activity.objects.filter(activity_type=Activity.LIKE, article_comment=self.pk).count()
        self.likes = likes
        self.save()
        return self.likes

    def get_likes(self):
        likes = Activity.objects.filter(activity_type=Activity.LIKE, article_comment=self.pk)
        return likes

    def get_likers(self):
        likes = self.get_likes()
        likers = []
        for like in likes:
            likers.append(like.user)
        return likers