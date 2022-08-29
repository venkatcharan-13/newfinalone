import calendar
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
import locale
from django.shortcuts import render
from utility import accounts_util, acc_gets
from rest_framework.views import APIView
from accounts.models import ClientNote
from authentication.models import Client
from rest_framework.response import Response
import json
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.models import account_for_coding_choice
from utility import accounts_str as strvar

locale.setlocale(locale.LC_ALL, 'en_IN.utf8')
CURRENT_DATE_PERIOD = accounts_util.get_current_date_period()

current_period_str = strvar.current_period
previous_period_str = strvar.previous_period
pre_previous_period_str  = strvar.pre_previous_period
current_str = strvar.current
previous_str = strvar.previous
per_change_str = strvar.per_change
response_data_str, totals_str = "response_data", "totals"
description = "description"
account_header_str = "account_header"
client_notes_str = "client_notes"

config_file = open("config/accounts_config.json")
config_data = json.load(config_file)
pnl_config_data = config_data['income_statement']
bs_config_data = config_data['balance_sheet']
cashflow_config_data = config_data['cashflow']
ratios_config_data = config_data['ratios']

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
@csrf_exempt
def add_client_note(request):
    written_note = json.loads(request.body)["note"]
    period = datetime.strptime(json.loads(request.body)["period"], '%Y-%m-%d').date()
    table_type = json.loads(request.body)["table"]
    logged_client = Client.objects.get(
        pk = request.user.id
    )
    client_note = ClientNote(
        client = logged_client,
        period = period,
        related_table = table_type,
        note = written_note,
    )
    client_note.save()
    return JsonResponse({'Message': 'Success'})

@login_required()
def pnl_transaction(request, account):
    selected_month = request.GET.get('selected_date')
    logged_client_id = request.user.id

    if selected_month is None:
        selected_month = CURRENT_DATE_PERIOD
    else:
        selected_month = datetime.strptime(selected_month, '%Y-%m-%d').date()

    # Fetching PNL transactions for each payee related to an account
    response_data, totals, prev_three_months = accounts_util.fetch_pnl_transactions(
        selected_month, logged_client_id, account
    )
    response_data_modified = accounts_util.convert_to_indian_comma_notation('pnl_trans', response_data)
    totals_modified = accounts_util.convert_to_indian_comma_notation('pnl_totals', totals)
    current_month = prev_three_months[0]
    previous_month = prev_three_months[1]
    pre_previous_month = prev_three_months[2]
    context = {
        'account': dict(account_for_coding_choice)[account],
        current_period_str: calendar.month_name[current_month.month] + '-' + str(current_month.year)[2:],
        previous_period_str: calendar.month_name[previous_month.month] + '-' + str(previous_month.year)[2:],
        pre_previous_period_str: calendar.month_name[pre_previous_month.month] + '-' + str(pre_previous_month.year)[2:],
        response_data_str: response_data_modified,
        totals_str: totals_modified
    }
    return render(request, 'pnl_trans.html', context)


@login_required()
def cashflow_balances(request, activity):
    selected_month = request.GET.get('selected_date')
    logged_client_id = request.user.id

    for dic in cashflow_config_data.values():
        if type(dic) != dict:
            continue
        for val in dic.values():
            if type(val) != str and val['head'] == activity:
                codings_lst = val['accounts_for_coding']
                subtraction_logic = val['logic']
                break
    
    if selected_month is None:
        selected_month = CURRENT_DATE_PERIOD
    else:
        selected_month = datetime.strptime(selected_month, '%Y-%m-%d').date()

    # Fetching balance for each account related to an account for coding
    response_data, totals, two_periods = accounts_util.fetch_cashflow_balances(
        selected_month, logged_client_id, codings_lst, subtraction_logic
    )
    response_data_modified = accounts_util.convert_to_indian_comma_notation('cashflow_bal', response_data)
    totals_modified = accounts_util.convert_to_indian_comma_notation('cashflow_totals', totals)

    current_month = two_periods[0]
    previous_month = two_periods[1]

    context = {
        'activity': activity,
        current_period_str: calendar.month_name[current_month.month] + '-' + str(current_month.year)[2:],
        previous_period_str: calendar.month_name[previous_month.month] + '-' + str(previous_month.year)[2:],
        response_data_str: response_data_modified,
        totals_str: totals_modified
    }

    return render(request, 'cashflow_bal.html', context)


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
            'Depreciation Expenses'
        )

        if selected_month is None:
            selected_month = CURRENT_DATE_PERIOD
        else:
            selected_month = datetime.strptime(selected_month, '%Y-%m-%d').date()
        
        current_month, current_month_year = selected_month.month, selected_month.year
        previous_month = (selected_month.replace(day=1) + relativedelta(days=-1)).month
        previous_month_year = (selected_month.replace(day=1) + relativedelta(days=-1)).year

        client_notes_data = ClientNote.objects.filter(
            client_id=logged_client_id,
            period=selected_month,
            related_table='pnl'
        )
        client_notes = []
        for note in client_notes_data:
            client_notes.append({
                'created_on': datetime.strftime(note.created_on, "%d %b, %Y (%H:%M)"),
                'note': note.note,
                'admin_response': note.admin_response
            })

        pnl_data = acc_gets.get_pnl(selected_month, logged_client_id)[0]

        # sorting account heads in standard order
        pnl_data['income']['data'] = sorted(
            pnl_data['income']['data'],
            key=lambda x: x[account_header_str]
        )
        pnl_data['expense'] = dict(sorted(
            pnl_data['expense'].items(), 
            key=lambda x: expenses_order.index(x[0]) if x[0] in expenses_order else 10
        ))
        
        pnl_data_response = {}
        pnl_data_response[description] = pnl_config_data[description]
        pnl_data_response[current_period_str] = calendar.month_name[current_month] + '-' + str(current_month_year)[2:]
        pnl_data_response[previous_period_str] = calendar.month_name[previous_month] + '-' + str(previous_month_year)[2:]
        pnl_data_response[client_notes_str] = client_notes
        pnl_data_response[response_data_str] = accounts_util.convert_to_indian_comma_notation('pnl', pnl_data)

        return Response(pnl_data_response)


class BalanceSheetData(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        selected_month = self.request.query_params.get('selected_date')
        logged_client_id = self.request.user.id

        if selected_month is None:
            selected_month = CURRENT_DATE_PERIOD
        else:
            selected_month = datetime.strptime(selected_month, '%Y-%m-%d').date()

        current_month, current_month_year = selected_month.month, selected_month.year
        previous_month = (selected_month.replace(day=1) + relativedelta(days=-1)).month
        previous_month_year = (selected_month.replace(day=1) + relativedelta(days=-1)).year

        client_notes_data = ClientNote.objects.filter(
            client_id=logged_client_id,
            period=selected_month,
            related_table='balsheet'
        )
        client_notes = []
        for note in client_notes_data:
            client_notes.append({
                'created_on': datetime.strftime(note.created_on, "%d %b, %Y (%H:%M)"),
                'note': note.note,
                'admin_response': note.admin_response
            })

        bal_sheet_data = acc_gets.get_balsheet(selected_month, logged_client_id)
        current_year_earnings, retained_earnings = acc_gets.get_earnings(selected_month, logged_client_id)

        bal_sheet_data['equity']['data'].extend([
            {
                account_header_str: "Current Year earnings",
                current_str: current_year_earnings[current_str],
                previous_str: current_year_earnings[previous_str],
                per_change_str: 0 if current_year_earnings[previous_str] == 0 else 
                    round((current_year_earnings[current_str]/current_year_earnings[previous_str] - 1)*100)
            },
            {
                account_header_str: "Retained Earnings",
                current_str: retained_earnings[current_str],
                previous_str: retained_earnings[previous_str],
                per_change_str: 0 if retained_earnings[previous_str] == 0 else 
                    round((retained_earnings[current_str]/retained_earnings[previous_str] - 1)*100)
            }
        ])
        
        bal_sheet_data['total_equity'][current_str] += (current_year_earnings[current_str] + retained_earnings[current_str])
        bal_sheet_data['total_equity'][previous_str] += (current_year_earnings[previous_str] + retained_earnings[previous_str])
        bal_sheet_data['total_equity'][per_change_str] = 0 if bal_sheet_data['total_equity'][previous_str] == 0 else round(
            (bal_sheet_data['total_equity'][current_str]/bal_sheet_data['total_equity'][previous_str]-1)*100)

        bal_sheet_data_response = {}
        bal_sheet_data_response[description] = bs_config_data[description]
        bal_sheet_data_response[current_period_str] = calendar.month_name[current_month] + '-' + str(current_month_year)[2:]
        bal_sheet_data_response[previous_period_str] = calendar.month_name[previous_month] + '-' + str(previous_month_year)[2:]
        bal_sheet_data_response[client_notes_str] = client_notes
        bal_sheet_data_response[response_data_str] = accounts_util.convert_to_indian_comma_notation('balsheet', bal_sheet_data)
       
       
        return Response(bal_sheet_data_response)


class CashFlowData(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        selected_month = self.request.query_params.get('selected_date')
        logged_client_id = self.request.user.id

        if selected_month is None:
            selected_month = CURRENT_DATE_PERIOD
        else:
            selected_month = datetime.strptime(selected_month, '%Y-%m-%d').date()
        current_month, current_month_year = selected_month.month, selected_month.year
        previous_month = (selected_month.replace(day=1) + relativedelta(days=-1)).month
        previous_month_year = (selected_month.replace(day=1) + relativedelta(days=-1)).year

        client_notes_data = ClientNote.objects.filter(
            client_id=logged_client_id,
            period=selected_month,
            related_table='cashflow'
        )
        client_notes = []
        for note in client_notes_data:
            client_notes.append({
                'created_on': datetime.strftime(note.created_on, "%d %b, %Y (%H:%M)"),
                'note': note.note,
                'admin_response': note.admin_response
            })

        cashflow_data = acc_gets.get_cashflow(selected_month, logged_client_id)
        
        cashflow_data_response = {}
        cashflow_data_response[description] = cashflow_config_data[description]
        cashflow_data_response[current_period_str] = calendar.month_name[current_month] + '-' + str(current_month_year)[2:]
        cashflow_data_response[previous_period_str] = calendar.month_name[previous_month] + '-' + str(previous_month_year)[2:]
        cashflow_data_response[client_notes_str] = client_notes
        cashflow_data_response[response_data_str] = accounts_util.convert_to_indian_comma_notation('cashflow', cashflow_data)
        cashflow_data_response['cashflow_A_info'] = cashflow_config_data['cashflow_from_operating_activities']['info_title']
        cashflow_data_response['cashflow_B_info'] = cashflow_config_data['cashflow_from_investing_activities']['info_title']
        cashflow_data_response['cashflow_C_info'] = cashflow_config_data['cashflow_from_financing_activities']['info_title']
        
        return Response(cashflow_data_response)


class RatiosData(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        selected_month = self.request.query_params.get('selected_date')
        logged_client_id = self.request.user.id

        if selected_month is None:
            selected_month = CURRENT_DATE_PERIOD
        else:
            selected_month = datetime.strptime(selected_month, '%Y-%m-%d').date()

        current_month, current_month_year = selected_month.month, selected_month.year
        previous_month = (selected_month.replace(day=1) + relativedelta(days=-1)).month
        previous_month_year = (selected_month.replace(day=1) + relativedelta(days=-1)).year

        client_notes_data = ClientNote.objects.filter(
            client_id=logged_client_id,
            period=selected_month,
            related_table='ratio'
        )
        client_notes = []
        for note in client_notes_data:
            client_notes.append({
                'created_on': datetime.strftime(note.created_on, "%d %b, %Y (%H:%M)"),
                'note': note.note,
                'admin_response': note.admin_response
            })
        
        ratios_data = acc_gets.get_ratios(selected_month, logged_client_id)

        ratios_data_response = {}
        ratios_data_response[description] = ratios_config_data[description]
        ratios_data_response[current_period_str] = calendar.month_name[current_month] + '-' + str(current_month_year)[2:]
        ratios_data_response[previous_period_str] = calendar.month_name[previous_month] + '-' + str(previous_month_year)[2:]
        ratios_data_response[client_notes_str] = client_notes
        ratios_data_response[response_data_str] = ratios_data
                    
        return Response(ratios_data_response)