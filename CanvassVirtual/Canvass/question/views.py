from django.shortcuts import render,HttpResponse
# Create your views here.
from .forms import QuestionForm,AnswerForm
from .models import Question
def home(req):
    questions=Question.objects.all()
    return render(req,'question/questions.html',{'questions':questions})

def ask(req):
    form=QuestionForm(req.POST or None)
    if req.method =='GET':
        return render(req,'question/ask.html',{'form':form})
    question=form.save(commit=False)
    question.user=req.user
    question.save()
    form = AnswerForm(initial={'question': question})
    return render(req,'question/answer.html', {'question': question, 'form': form})

def answer(req,id):
    if req.method=="POST":
        form = AnswerForm(req.POST)
        Ans = form.save(commit=False)
        Ans.user = req.user
        Ans.save()

    question = Question.objects.get(pk=id)
    form = AnswerForm(initial={'question': question})
    return render(req,'question/answer.html', {'question': question, 'form': form})

