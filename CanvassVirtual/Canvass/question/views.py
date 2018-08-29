from django.shortcuts import render

# Create your views here.
from .forms import QuestionForm
def home(req):
    return render(req,'base.html')

def ask(req):
    form=QuestionForm(req.POST or None)
    if req.method =='GET':
        return render(req,'question/ask.html',{'form':form})
    pass