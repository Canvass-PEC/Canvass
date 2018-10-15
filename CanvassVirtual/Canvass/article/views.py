from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseBadRequest, HttpResponse
from .models import Article,ArticleComment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ArticleForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from Canvass.decorators import ajax_required
import markdown
from django.template.loader import render_to_string
from activity.models import Activity
from django.db.models import Q

def _articles(request, articles):
    paginator = Paginator(articles, 10)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    return render(request, 'articles/articles.html', {'articles': articles})

@login_required
def articles(request):
    all_articles = Article.get_published()
    return _articles(request, all_articles)

@login_required
def article(request, slug):
    article = get_object_or_404(Article, slug=slug, status=Article.PUBLISHED)
    return render(request, 'articles/article.html', {'article': article})


@login_required
def write(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = Article()
            article.create_user = request.user
            article.title = form.cleaned_data.get('title')
            article.content = form.cleaned_data.get('content')
            status = form.cleaned_data.get('status')
            if status in [Article.PUBLISHED, Article.DRAFT]:
                article.status = form.cleaned_data.get('status')
            article.save()
            return redirect('/articles/')
    else:
        form = ArticleForm()
    return render(request, 'articles/write.html', {'form': form})

@login_required
def drafts(request):
    drafts = Article.objects.filter(create_user=request.user, status=Article.DRAFT)
    return render(request, 'articles/drafts.html', {'drafts': drafts})

@login_required
def edit(request, id):
    if id:
        article = get_object_or_404(Article, pk=id)
    else:
        article = Article(create_user=request.user)

    if request.POST:
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('/articles/')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'articles/edit.html', {'form': form})


@login_required
@ajax_required
def preview(request):
    try:
        if request.method == 'POST':
            content = request.POST.get('content')
            html = 'Nothing to display :('
            if len(content.strip()) > 0:
                html = markdown.markdown(content, safe_mode='escape')
            return HttpResponse(html)
        else:
            return HttpResponseBadRequest()
    except Exception as e:
        return HttpResponseBadRequest()

@login_required
@ajax_required
def comment(request):
    try:
        if request.method == 'POST':
            article_id = request.POST.get('article')
            article = Article.objects.get(pk=article_id)
            comment = request.POST.get('comment')
            comment = comment.strip()
            if len(comment) > 0:
                article_comment = ArticleComment(user=request.user, article=article, comment=comment)
                article_comment.save()
            html = u''
            for comment in article.get_comments():
                html = u'{0}{1}'.format(html, render_to_string('articles/partial_article_comment.html', {'comment': comment}))
            return HttpResponse(html)
        else:
            return HttpResponseBadRequest()
    except Exception as e:
        return HttpResponseBadRequest()

@login_required
@ajax_required
def vote(request):
    article_id = request.POST['article']
    article = Article.objects.get(pk=article_id)
    vote = request.POST['vote']
    user = request.user
    activity = Activity.objects.filter(Q(activity_type=Activity.UP_VOTEA) | Q(activity_type=Activity.DOWN_VOTEA),
                                   user=user, article=article_id)
    if activity:
        activity.delete()
    if vote in [Activity.UP_VOTEA, Activity.DOWN_VOTEA]:
        activity = Activity(activity_type=vote, user=user, article=article_id)
        activity.save()

    if request.user!=article.create_user:
        if vote == Activity.UP_VOTEA :
            request.user.profile.notify_upvoted_article(article)
        else :
            request.user.profile.notify_downvoted_article(article)
    return HttpResponse(article.calculate_votes())


@login_required
@ajax_required
def like(request):
    article_id = request.POST['article']
    comment_id = request.POST['comment']
    comment = ArticleComment.objects.get(pk=comment_id)
    user = request.user
    like = Activity.objects.filter(activity_type=Activity.LIKE, article=article_id, user=user,article_comment=comment_id)
    if like:
        user.profile.unotify_liked_comment(comment)
        like.delete()
        pass
    else:
        like = Activity(activity_type=Activity.LIKE, article=article_id, user=user,article_comment=comment_id)
        like.save()
        user.profile.notify_liked_comment(comment)
    return HttpResponse(comment.calculate_likes())
