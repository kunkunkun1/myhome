"""blog_dj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from . import views

app_name = 'web'
urlpatterns = [
    path('', views.user, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    # 用户个人站点
    re_path(r'^(?P<user_id>\d+)/$', views.user, name='user'),
    # 帖子
    re_path(r'^(?P<user_id>\d+/)?transaction/(?P<pk>\d+/)?$', views.transaction, name='transaction'),

]
