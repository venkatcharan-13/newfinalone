from datetime import datetime, date
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from taxes.models import TaxAlert, IncomeTaxMonthlyStatus, IncomeTaxQuarterlyStatus, IncomeTaxAdvanceStatus, GSTR1MonthlyStatus, GSTR3BMonthlyStatus, GSTR8MonthlyStatus, ProvidentFundMonthlyStatus, ESICMonthlyStatus
from utility import accounts_util

# Create your views here.
CURRENT_DATE_PERIOD = accounts_util.get_current_date_period()


@login_required()
def taxes(request):
    return render(request, 'taxes.html')

@login_required()
def gst(request):
    return render(request, 'gst.html')

@login_required()
def other_compliances(request):
    return render(request, 'other_comp.html')


class TaxesData(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        logged_client_id = self.request.user.id
        selected_month = self.request.query_params.get('selected_date')
        selected_fy = int(self.request.query_params.get('selected_fy'))

        if selected_month is None:
            selected_month = CURRENT_DATE_PERIOD
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
        advance_tax_status = IncomeTaxAdvanceStatus.objects.filter(
            client_id = logged_client_id
        )
        
        income_tax_data_response = {
            'alerts': [],
            'status':{
                'monthly': {},
                'quarterly': {},
                'advance': {}
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

        for advance_stat in advance_tax_status:
            if advance_stat.fin_year == selected_fy:
                income_tax_data_response['status']['advance'][f'{advance_stat.get_quarter_display()} {advance_stat.year%100}'] = advance_stat.payment_status

        return Response(income_tax_data_response)

class GSTData(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        logged_client_id = self.request.user.id
        selected_month = self.request.query_params.get('selected_date')
        selected_fy = int(self.request.query_params.get('selected_fy'))

        if selected_month is None:
            selected_month = CURRENT_DATE_PERIOD
        else:
            selected_month = datetime.strptime(selected_month, '%Y-%m-%d').date()
            

        tax_alerts = TaxAlert.objects.filter(
            client_id = logged_client_id,
            tax_type = 'gst',
            raised_on__lte = selected_month,
            raised_on__gte = selected_month.replace(day=1)
        )

        gstr1_status = GSTR1MonthlyStatus.objects.filter(
            client_id = logged_client_id
        )
        gstr3b_status = GSTR3BMonthlyStatus.objects.filter(
            client_id = logged_client_id
        )
        gstr8_status = GSTR8MonthlyStatus.objects.filter(
            client_id = logged_client_id
        )
        
        gst_data_response = {
            'alerts': [],
            'status':{
                'gstr1': {},
                'gstr3b': {},
                'gstr8': {}
            }
        }
       
        for alert in tax_alerts:
            gst_data_response['alerts'].append({
                'desc': alert.alert,
                'dueDate': datetime.strftime(alert.due_date, "%d %b, %Y")
            })

        for monthly_stat in gstr1_status:
            if monthly_stat.fin_year == selected_fy:
                gst_data_response['status']['gstr1'][f'{monthly_stat.get_month_name_display()}-{monthly_stat.year%100}'] = monthly_stat.payment_status
        
        for monthly_stat in gstr3b_status:
            if monthly_stat.fin_year == selected_fy:
                gst_data_response['status']['gstr3b'][f'{monthly_stat.get_month_name_display()}-{monthly_stat.year%100}'] = monthly_stat.payment_status

        for monthly_stat in gstr8_status:
            if monthly_stat.fin_year == selected_fy:
                gst_data_response['status']['gstr8'][f'{monthly_stat.get_month_name_display()}-{monthly_stat.year%100}'] = monthly_stat.payment_status

        return Response(gst_data_response)


class OtherCompliancesData(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        logged_client_id = self.request.user.id
        selected_month = self.request.query_params.get('selected_date')
        selected_fy = int(self.request.query_params.get('selected_fy'))

        if selected_month is None:
            selected_month = CURRENT_DATE_PERIOD
        else:
            selected_month = datetime.strptime(selected_month, '%Y-%m-%d').date()
            

        tax_alerts = TaxAlert.objects.filter(
            client_id = logged_client_id,
            tax_type = 'other_compliances',
            raised_on__lte = selected_month,
            raised_on__gte = selected_month.replace(day=1)
        )

        provident_fund_status = ProvidentFundMonthlyStatus.objects.filter(
            client_id = logged_client_id
        )
        esic_status = ESICMonthlyStatus.objects.filter(
            client_id = logged_client_id
        )

        other_comp_data_response = {
            'alerts': [],
            'status':{
                'pf_status': {},
                'esic_status': {},
            }
        }
       
        for alert in tax_alerts:
            other_comp_data_response['alerts'].append({
                'desc': alert.alert,
                'dueDate': datetime.strftime(alert.due_date, "%d %b, %Y")
            })

        for monthly_stat in provident_fund_status:
            if monthly_stat.fin_year == selected_fy:
                other_comp_data_response['status']['pf_status'][f'{monthly_stat.get_month_name_display()}-{monthly_stat.year%100}'] = monthly_stat.payment_status
        
        for monthly_stat in esic_status:
            if monthly_stat.fin_year == selected_fy:
                other_comp_data_response['status']['esic_status'][f'{monthly_stat.get_month_name_display()}-{monthly_stat.year%100}'] = monthly_stat.payment_status

        return Response(other_comp_data_response)