from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.accounts, name='accounts'),
    path('api/zohoData/', views.ZohoData.as_view()),
]
