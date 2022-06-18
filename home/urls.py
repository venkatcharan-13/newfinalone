from unicodedata import name
from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_actionable_remark/<int:pk>/', views.add_actionable_remark, name='add_actionable_remark'),
    path('add_watchout_remark/<int:pk>/', views.add_watchout_remark, name='add_watchout_remark'),
    path('taxes/', views.taxes, name='taxes'),
    path('help/', views.help, name='help'),
    path('profile/', views.profile, name='profile'),
]
