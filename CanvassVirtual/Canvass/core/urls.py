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
from django.contrib.auth.views import auth_login
from django.urls import path,include
from .views import home,settings,picture,save_uploaded_picture,password,network,profile,upload_picture
app_name="core"

urlpatterns = [
    path('',home,name='home'),
    path('settings',settings,name='settings'),
    path('settings/picture/',picture,name='picture'),
    path('save_uploaded_picture',save_uploaded_picture,name='save_uploaded_picture'),
    path('upload_picture',upload_picture,name='upload_picture'),
    path('password',password,name='password'),
    path('network',network,name='network'),
    path('<str:username>',profile,name='profile'),
]
