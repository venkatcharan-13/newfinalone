from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/dashboardData/', views.DashboardData.as_view()),
    path('add_actionable_remark/<int:pk>/', views.add_actionable_remark, name='add_actionable_remark'),
]
