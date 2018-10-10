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
from .views import inbox,new,delete,users,check,messages,send
app_name="messages"

urlpatterns = [
    path('',inbox,name='inbox'),
    path('new',new,name='new'),
    path('send',send,name='send'),
    path('delete',delete,name='delete'),
    path('users',users,name='users'),
    path('check',check,name='check'),
    path('<str:username>/',messages,name='messages'),
]
