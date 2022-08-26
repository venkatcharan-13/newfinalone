from datetime import datetime, date
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from taxes.models import TaxAlert, IncomeTaxMonthlyStatus, IncomeTaxQuarterlyStatus, GSTMonthlyStatus, GSTQuarterlyStatus

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
        selected_month = self.request.query_params.get('selected_date')
        selected_fy = int(self.request.query_params.get('selected_fy'))

        if selected_month is None:
            selected_month = date(2022, 6, 30)
        else:
            selected_month = datetime.strptime(selected_month, '%Y-%m-%d').date()
            

        tax_alerts = TaxAlert.objects.filter(
            client_id = logged_client_id,
            tax_type = 'income_tax',
            raised_on__lte = selected_month,
            raised_on__gte = selected_month.replace(day=1)
        )

        monthly_status = IncomeTaxMonthlyStatus.objects.filter(
            client_id = logged_client_id,
        )
        quarterly_status = IncomeTaxQuarterlyStatus.objects.filter(
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
                'dueDate': datetime.strftime(alert.due_date, "%d %b, %Y"),
            })

        for monthly_stat in monthly_status:
            if monthly_stat.fin_year == selected_fy:
                income_tax_data_response['status']['monthly'][f'{monthly_stat.get_month_name_display()}-{monthly_stat.year%100}'] = monthly_stat.payment_status
        
        for quarterly_stat in quarterly_status:
            if quarterly_stat.fin_year == selected_fy:
                income_tax_data_response['status']['quarterly'][f'{quarterly_stat.get_quarter_display()} {quarterly_stat.year%100}'] = quarterly_stat.payment_status

        return Response(income_tax_data_response)

class GSTData(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        logged_client_id = self.request.user.id
        selected_month = self.request.query_params.get('selected_date')
        selected_fy = int(self.request.query_params.get('selected_fy'))

        if selected_month is None:
            selected_month = date(2022, 6, 30)
        else:
            selected_month = datetime.strptime(selected_month, '%Y-%m-%d').date()
            

        tax_alerts = TaxAlert.objects.filter(
            client_id = logged_client_id,
            tax_type = 'gst',
            raised_on__lte = selected_month,
            raised_on__gte = selected_month.replace(day=1)
        )

        monthly_status = GSTMonthlyStatus.objects.filter(
            client_id = logged_client_id,
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
                'dueDate': datetime.strftime(alert.due_date, "%d %b, %Y")
            })

        for monthly_stat in monthly_status:
            if monthly_stat.fin_year == selected_fy:
                gst_data_response['status']['monthly'][f'{monthly_stat.get_month_name_display()}-{monthly_stat.year%100}'] = monthly_stat.payment_status
        
        for quarterly_stat in quarterly_status:
            if quarterly_stat.fin_year == selected_fy:
                gst_data_response['status']['quarterly'][f'{quarterly_stat.get_quarter_display()} {quarterly_stat.year%100}'] = quarterly_stat.payment_status

        return Response(gst_data_response)