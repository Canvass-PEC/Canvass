from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from activity.models import Activity
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from Canvass.decorators import ajax_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def _questions(request, questions, active):
    paginator = Paginator(questions, 10)
    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)
    return render(request, 'question/questions.html', {'questions': questions, 'active': active})


@login_required
def questions(request):
    questions = Question.objects.all()
    return _questions(request, questions, 'unanswered')

@login_required
def answered(request):
    questions = Question.get_answered()
    return questions(request, questions, 'answered')


@login_required
def all(request):
    questions = Question.objects.all()
    return questions(request, questions, 'all')

@login_required
def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
           question = Question()
           question.user = request.user
           question.title = form.cleaned_data.get('title')
           question.description = form.cleaned_data.get('description')
           question.save()
           return redirect('/questions/')
        else:
            return render(request, 'questions/ask.html', {'form': form})
    else:
        form = QuestionForm()
    return render(request, 'question/ask.html', {'form': form})

@login_required
def question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    form = AnswerForm(initial={'question': question})
    return render(request, 'question/question.html', {'question': question, 'form': form})

@login_required
def answer(request):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            user = request.user
            answer = Answer()
            answer.user = request.user
            answer.question = form.cleaned_data.get('question')
            answer.description = form.cleaned_data.get('description')
            answer.save()
            user.profile.notify_answered(answer.question)
            return redirect(u'/questions/{0}/'.format(answer.question.pk))
        else:
            question = form.cleaned_data.get('question')
            return render(request, 'question/question.html', {'question': question, 'form': form})
    else:
        return redirect('/questions/')


@login_required
@ajax_required
def vote(request):
    answer_id = request.POST['answer']
    answer = Answer.objects.get(pk=answer_id)
    vote = request.POST['vote']
    user = request.user
    activity = Activity.objects.filter(Q(activity_type=Activity.UP_VOTE) | Q(activity_type=Activity.DOWN_VOTE), user=user, answer=answer_id)
    if activity:
        activity.delete()
    if vote in [Activity.UP_VOTE, Activity.DOWN_VOTE]:
        activity = Activity(activity_type=vote, user=user, answer=answer_id)
        activity.save()
    return HttpResponse(answer.calculate_votes())

