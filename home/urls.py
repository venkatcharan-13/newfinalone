from unicodedata import name
from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', views.accounts, name='accounts'),
    path('analytics/', views.analytics, name='analytics'),
    path('taxes/', views.taxes, name='taxes'),
    path('help/', views.help, name='help'),
    path('profile/', views.profile, name='profile'),
]
