import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from home.models import PendingActionable, WatchOutPoint
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required()
def index(request):
    logged_client_id = request.user.id
    pending_actionables = PendingActionable.objects.filter(
        client_id=logged_client_id
    )
    watch_out_points = WatchOutPoint.objects.filter(
        client_id=logged_client_id
    )
    context = {
        'pending_points': pending_actionables,
        'watch_out_points': watch_out_points,
    }
    return render(request, 'dashboard.html', context)

@csrf_exempt
def add_actionable_remark(request, pk):
    pending_actionable = PendingActionable.objects.get(pk=pk)
    pending_actionable.clientRemarks = json.loads(request.body)["actionRemark"]
    pending_actionable.save()
    return JsonResponse({'Message': 'Success'})

@csrf_exempt
def add_watchout_remark(request, pk):
    watchout_point = WatchOutPoint.objects.get(pk=pk)
    watchout_point.clientRemarks = json.loads(request.body)["watchoutRemark"]
    watchout_point.save()
    return JsonResponse({'Message': 'Success'})

def help(request):
    return HttpResponse("This will be Help Page")

