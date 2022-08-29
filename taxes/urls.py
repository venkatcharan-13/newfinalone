from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.taxes, name='taxes'),
    path('api/incometaxData/', views.TaxesData.as_view()),
    path('gst/', views.gst, name='gst'),
    path('gst/api/gstData/', views.GSTData.as_view()),
    path('otherComp/', views.other_compliances, name='other_compliances'),
    path('otherComp/api/othercompData/', views.OtherCompliancesData.as_view())
]
