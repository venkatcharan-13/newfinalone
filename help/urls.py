from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.help, name='help'),
    path('resources/', views.resources, name='resources'),
    path('raise_ticket/', views.raise_ticket, name='raise_ticket')
]
