from django.shortcuts import render
from django.http import HttpResponse
from home.models import PendingActionables, WatchOut

# Create your views here.

def index(request):
    pending_actionables = PendingActionables.objects.all()
    watch_out_points = WatchOut.objects.all()
    context = {
        'pending_points': pending_actionables,
        'watch_out_points': watch_out_points,
    }
    return render(request, 'dashboard.html', context)

def accounts(request):
    return HttpResponse("This will be Accounts Page")

def analytics(request):
    return HttpResponse("This will be Analytics Page")

def taxes(request):
    return HttpResponse("This will be Taxes Page")

def help(request):
    return HttpResponse("This will be Help Page")

def profile(request):
    return HttpResponse("This will be Profile Page")
