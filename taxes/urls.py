from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.taxes, name='taxes'),
    path('api/incometaxData/', views.TaxesData.as_view()),
    path('gst/', views.gst, name='gst'),
    path('othertax/', views.other_taxes, name='other_taxes'),
]
