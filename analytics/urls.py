from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.analytics, name='analytics'),
    path('api/reportData/', views.ReportData.as_view()),
    path('insights/', views.insights, name='insights'),
    path('insights/api/insightsData/', views.InsightsData.as_view()),
    path('deep_insights/', views.deep_insights, name='deep_insights'),
    path('deep_insights/api/deepinsData/', views.DeepInsightsData.as_view())
]
