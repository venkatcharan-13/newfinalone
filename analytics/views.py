from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def analytics(request):
    return render(request, 'analytics.html')

def insights(request):
    return render(request, 'insights.html')

def deep_insights(request):
    return render(request, 'deep_insights.html')