from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles, name='profiles'),
    path('company/', views.company, name='company'),
    path('company/api/company_info/', views.CompanyInfo.as_view()),
    path('company/save_company_info/', views.save_company_info, name='save_company_info'),
    path('context/', views.context, name='context'),
    path('context/api/context_data/', views.ContextData.as_view()),
    path('context/save_company_context/', views.save_company_context, name='save_company_context'),
    path('connections/', views.connections, name='connections'),
    path('banks/', views.bank_details, name='banks'),
    path('banks/api/bank_details/', views.BanksData.as_view())
]
