"""Canvass URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .views import question,questions,answer,unanswered,answered,vote,ask,all
app_name="question"

urlpatterns = [
    path('',questions,name='questions'),
    path('ask',ask,name='ask'),
    path('answer',answer,name='answer'),
    path('answer/vote',vote,name='vote'),
    path('all',all,name='all'),
    path('answered',answered,name='answered'),
    path('unanswered',unanswered,name='unanswered'),
    path('<int:pk>',question,name='question'),
]
