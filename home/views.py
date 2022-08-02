import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from datetime import date, datetime
from home.models import PendingActionable, WatchOutPoint,  StatutoryCompliance
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.

@login_required()
def index(request):
    return render(request, 'dashboard.html')

@csrf_exempt
def add_actionable_remark(request, pk):
    pending_actionable = PendingActionable.objects.get(pk=pk)
    pending_actionable.client_remarks = json.loads(request.body)["actionRemark"]
    pending_actionable.save()
    return JsonResponse({'Message': 'Success'})

def help(request):
    return HttpResponse("This will be Help Page")


class DashboardData(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        logged_client_id = self.request.user.id
        selected_month = self.request.query_params.get('selected_date')
        if selected_month is None:
            selected_month = date(2022, 6, 30)
        else:
            selected_month = datetime.strptime(selected_month, '%Y-%m-%d').date()

        pending_actionables_data = PendingActionable.objects.filter(
            client_id=logged_client_id,
            created_on__lte=selected_month,
            created_on__gte=selected_month.replace(day=1)
        )
        pending_actionables = []
        for i, pending_action in enumerate(pending_actionables_data):
            pending_actionables.append({
                'sno': i+1,
                'id': pending_action.pk,
                'point': pending_action.point,
                'client_remarks': pending_action.client_remarks,
                'status': pending_action.status
            })

        watchout_points_data = WatchOutPoint.objects.filter(
            client_id=logged_client_id,
            created_on__lte=selected_month,
            created_on__gte=selected_month.replace(day=1)
        )
        watchout_points = []
        for i, watchout in enumerate(watchout_points_data):
            watchout_points.append({
                'sno': i+1,
                'point': watchout.point,
            })

        statutory_compliances_data = StatutoryCompliance.objects.filter(
            client_id=logged_client_id
        )

        statutory_compliances = {}
        for compliance in statutory_compliances_data:
            comp_type = compliance.compliance_type.upper()
            if comp_type not in statutory_compliances:
                statutory_compliances[comp_type] = []
            statutory_compliances[comp_type].append({
                'compliance': compliance.compliance,
                'current_month': compliance.current_month_due_date,
                'current_status': compliance.get_current_month_status_display(),
                'last_status': compliance.get_last_month_status_display(),
                'last_month': compliance.last_month_completion_date
            })
        
        response = {
            'pending_points': pending_actionables,
            'watchout_points': watchout_points,
            'statutory_compliances': statutory_compliances
        }


        return Response(response)
