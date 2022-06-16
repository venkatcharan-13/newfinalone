from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.analytics, name='analytics'),
    path('insights/', views.insights, name='insights'),
    path('deep_insights/', views.deep_insights, name='deep_insights')
]
