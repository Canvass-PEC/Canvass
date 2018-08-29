from django import forms
from .models import Question,Answer

class QuestionForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),max_length=250)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}),max_length=1000)

    class Meta:
        model = Question
        fields = ['title', 'description']


class AnswerForm(forms.ModelForm):
    question = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=Question.objects.all())
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))

    class Meta:
        model = Answer
        fields = ['question', 'description']