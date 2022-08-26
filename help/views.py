from django.shortcuts import render

# Create your views here.
def help(request):
    return render(request, 'schedule.html')

def resources(request):
    return render(request, 'resources.html')

def raise_ticket(request):
    return render(request, 'raise_ticket.html')