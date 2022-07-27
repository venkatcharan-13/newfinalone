from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from taxes.models import TaxAlert, ITMonthlyStatus, ITQuarterlyStatus, GSTMonthlyStatus, GSTQuarterlyStatus

# Create your views here.
@login_required()
def taxes(request):
    return render(request, 'taxes.html')

@login_required()
def gst(request):
    return render(request, 'gst.html')

@login_required()
def other_taxes(request):
    return render(request, 'other_taxes.html')


class TaxesData(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        logged_client_id = self.request.user.id
        
        tax_alerts = TaxAlert.objects.filter(
            client_id = logged_client_id,
            taxType = 'income_tax'
        )

        monthly_status = ITMonthlyStatus.objects.filter(
            client_id = logged_client_id
        )
        quarterly_status = ITQuarterlyStatus.objects.filter(
            client_id = logged_client_id
        )
        
        income_tax_data_response = {
            'alerts': [],
            'status':{
                'monthly': {},
                'quarterly': {}
            }
        }
       
        for alert in tax_alerts:
            income_tax_data_response['alerts'].append({
                'desc': alert.alert,
                'dueDate': datetime.strftime(alert.dueDate, "%d %b, %Y"),
                'raisedOn': datetime.strftime(alert.raisedOn, "%d %b, %Y at %H:%M")
            })

        for monthly_stat in monthly_status:
            income_tax_data_response['status']['monthly'][monthly_stat.monthName] = monthly_stat.paymentStatus
        
        for quarterly_stat in quarterly_status:
            income_tax_data_response['status']['quarterly'][quarterly_stat.quarter] = quarterly_stat.paymentStatus

        return Response(income_tax_data_response)

class GSTData(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        logged_client_id = self.request.user.id
        
        tax_alerts = TaxAlert.objects.filter(
            client_id = logged_client_id,
            taxType = 'gst'
        )

        monthly_status = GSTMonthlyStatus.objects.filter(
            client_id = logged_client_id
        )
        quarterly_status = GSTQuarterlyStatus.objects.filter(
            client_id = logged_client_id
        )
        
        gst_data_response = {
            'alerts': [],
            'status':{
                'monthly': {},
                'quarterly': {}
            }
        }
       
        for alert in tax_alerts:
            gst_data_response['alerts'].append({
                'desc': alert.alert,
                'dueDate': datetime.strftime(alert.dueDate, "%d %b, %Y"),
                'raisedOn': datetime.strftime(alert.raisedOn, "%d %b, %Y at %H:%M")
            })

        for monthly_stat in monthly_status:
            gst_data_response['status']['monthly'][monthly_stat.monthName] = monthly_stat.paymentStatus
        
        for quarterly_stat in quarterly_status:
            gst_data_response['status']['quarterly'][quarterly_stat.quarter] = quarterly_stat.paymentStatus

        return Response(gst_data_response)