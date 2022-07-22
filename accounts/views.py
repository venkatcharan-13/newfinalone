import calendar
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import locale
from django.shortcuts import render
from utility import accounts_util, acc_gets
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

locale.setlocale(locale.LC_ALL, 'en_IN.utf8')
SELECTED_DATE = date(2022, 6, 30)
current_period_str, previous_period_str, response_data_str = "current_period", "previous_period", "response_data"

config_file = open("config/accounts_config.json")
config_data = json.load(config_file)
# Create your views here.

@login_required()
def accounts(request):
    return render(request, 'accounts.html')

@login_required()
def balsheet(request):
    return render(request, 'balsheet.html')

@login_required()
def cashflow(request):
    return render(request, 'cashflow.html')

@login_required()
def pnl_transaction(request, account):
    selected_month = request.GET.get('selected_date')
    logged_client_id = request.user.id

    if selected_month is None:
        selected_month = date(2022, 6, 30)
    else:
        selected_month = datetime.strptime(selected_month, '%Y-%m-%d').date()

    # Fetching PNL transactions for each payee related to an account
    response_data, totals, prev_three_months = accounts_util.fetch_pnl_transactions(
        selected_month, logged_client_id, account
    )
    current_month = prev_three_months[0]
    previous_month = prev_three_months[1]
    pre_previous_month = prev_three_months[2]
    context = {
        'current_period': calendar.month_name[current_month.month] + '-' + str(current_month.year)[2:],
        'previous_period': calendar.month_name[previous_month.month] + '-' + str(previous_month.year)[2:],
        'pre_previous_period': calendar.month_name[pre_previous_month.month] + '-' + str(pre_previous_month.year)[2:],
        'account': account,
        response_data_str: response_data,
        'totals': totals
    }
    return render(request, 'pnl_trans.html', context)


def ratios(request):
    return render(request, 'ratios.html')


class PnlData(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        logged_client_id = self.request.user.id
        selected_month = self.request.query_params.get('selected_date')
        expenses_order = (
            'Advertising and Marketing Expenses',
            'Employment Expenses',
            'Rent, Rates & Repairs Expenses',
            'Brokerage & Commission Charges',
            'General & Admin Charges',
            'Tax Expenses'
        )

        if selected_month is None:
            selected_month = date(2022, 6, 30)
        else:
            selected_month = datetime.strptime(selected_month, '%Y-%m-%d').date()
            
        current_month, current_month_year = selected_month.month, selected_month.year
        previous_month = (selected_month.replace(day=1) + relativedelta(days=-1)).month
        previous_month_year = (selected_month.replace(day=1) + relativedelta(days=-1)).year

        pnl_data = acc_gets.get_pnl(selected_month, logged_client_id)[0]

        # sorting account heads in standard order
        pnl_data['income']['data'] = sorted(
            pnl_data['income']['data'],
            key=lambda x: x["account_header"]
        )
        pnl_data['expense'] = dict(sorted(
            pnl_data['expense'].items(), 
            key=lambda x: expenses_order.index(x[0])
        ))
        
        pnl_data_response = {}
        pnl_data_response[current_period_str] = calendar.month_name[current_month] + '-' + str(current_month_year)[2:]
        pnl_data_response[previous_period_str] = calendar.month_name[previous_month] + '-' + str(previous_month_year)[2:]
        pnl_data_response[response_data_str] = accounts_util.convert_to_indian_comma_notation('pnl', pnl_data)

        return Response(pnl_data_response)


class BalanceSheetData(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        selected_month = self.request.query_params.get('selected_date')
        logged_client_id = self.request.user.id

        if selected_month is None:
            selected_month = date(2022, 6, 30)
        else:
            selected_month = datetime.strptime(selected_month, '%Y-%m-%d').date()
        current_month, current_month_year = selected_month.month, selected_month.year
        previous_month = (selected_month.replace(day=1) + relativedelta(days=-1)).month
        previous_month_year = (selected_month.replace(day=1) + relativedelta(days=-1)).year

        bal_sheet_data = acc_gets.get_balsheet(selected_month, logged_client_id)
        bal_sheet_data_response = {}
        bal_sheet_data_response[current_period_str] = calendar.month_name[current_month] + '-' + str(current_month_year)[2:]
        bal_sheet_data_response[previous_period_str] = calendar.month_name[previous_month] + '-' + str(previous_month_year)[2:]
        bal_sheet_data_response[response_data_str] = accounts_util.convert_to_indian_comma_notation('balsheet', bal_sheet_data)
        current_year_earnings, retained_earnings = acc_gets.get_earnings(selected_month, logged_client_id)
        
        bal_sheet_data_response[response_data_str]['equity'].extend([
            {
                "account_header": "Current Year earnings",
                "current": locale.format("%d", current_year_earnings["current"], grouping=True),
                "previous": locale.format("%d", current_year_earnings["previous"], grouping=True),
                "per_change": 0 if current_year_earnings["previous"] == 0 else accounts_util.change_percentage(
                    (current_year_earnings["current"]/current_year_earnings["previous"] - 1)*100
                )
            },
            {
                "account_header": "Retained Earnings",
                "current": locale.format("%d", retained_earnings["current"], grouping=True),
                "previous": locale.format("%d", retained_earnings["previous"], grouping=True),
                "per_change": 0 if retained_earnings["previous"] == 0 else accounts_util.change_percentage(
                    (retained_earnings["current"]/retained_earnings["previous"] - 1)*100
                )
            }
        ])
        
        return Response(bal_sheet_data_response)


class CashFlowData(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        selected_month = self.request.query_params.get('selected_date')
        logged_client_id = self.request.user.id

        if selected_month is None:
            selected_month = date(2022, 6, 30)
        else:
            selected_month = datetime.strptime(selected_month, '%Y-%m-%d').date()
        current_month, current_month_year = selected_month.month, selected_month.year
        previous_month = (selected_month.replace(day=1) + relativedelta(days=-1)).month
        previous_month_year = (selected_month.replace(day=1) + relativedelta(days=-1)).year

        cashflow_data = acc_gets.get_cashflow(selected_month, logged_client_id)
        
        cashflow_data_response = {}
        cashflow_data_response[current_period_str] = calendar.month_name[current_month] + '-' + str(current_month_year)[2:]
        cashflow_data_response[previous_period_str] = calendar.month_name[previous_month] + '-' + str(previous_month_year)[2:]
        cashflow_data_response[response_data_str] = accounts_util.convert_to_indian_comma_notation('cashflow', cashflow_data)
        
        return Response(cashflow_data_response)


class RatiosData(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        selected_month = self.request.query_params.get('selected_date')
        logged_client_id = self.request.user.id

        if selected_month is None:
            selected_month = date(2022, 6, 30)
        else:
            selected_month = datetime.strptime(selected_month, '%Y-%m-%d').date()

        current_month, current_month_year = selected_month.month, selected_month.year
        previous_month = (selected_month.replace(day=1) + relativedelta(days=-1)).month
        previous_month_year = (selected_month.replace(day=1) + relativedelta(days=-1)).year
        
        ratios_data = acc_gets.get_ratios(selected_month, logged_client_id)

        ratios_data_response = {}
        ratios_data_response[current_period_str] = calendar.month_name[current_month] + '-' + str(current_month_year)[2:]
        ratios_data_response[previous_period_str] = calendar.month_name[previous_month] + '-' + str(previous_month_year)[2:]
        ratios_data_response[response_data_str] = ratios_data
                    
        return Response(ratios_data_response)