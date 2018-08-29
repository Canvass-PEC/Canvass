from django.shortcuts import render

# Create your views here.
from .forms import ArticleForm
def home(req):
    return render(req,'base.html')

def write(req):
    form=ArticleForm(req.POST or None)
    if req.method=='POST':
        return render(req,'base.html')
    return render(req,'article/write.html',{'form':form})