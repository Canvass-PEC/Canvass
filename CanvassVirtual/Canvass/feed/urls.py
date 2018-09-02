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
from .views import feeds,like,comment,load_new,load,_html_feeds,check,post
app_name="feed"

urlpatterns = [
    path('',feeds,name='feeds'),
    path('like',like,name='like'),
    path('post',like,name='post'),
    path('check',check,name='check'),
    path('load_new',load_new,name='load_new'),
    path('laod',load,name='load'),
    path('comment',comment,name='comment'),
    path('_html_feeds',_html_feeds,name='_html_feeds'),
    path('post',post,name='post'),
]
