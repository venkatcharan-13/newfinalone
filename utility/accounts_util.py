from accounts.models import ZohoAccount, ZohoTransaction
from dateutil.relativedelta import relativedelta
from utility import accounts_str as strvar
from datetime import date, datetime
import locale
import json

locale.setlocale(locale.LC_ALL, 'en_IN.utf8')
curr_per_str, prev_per_str = strvar.current_per, strvar.previous_per
prev_per_change_str = strvar.prev_per_change
change_str = "change"
current_str = strvar.current
previous_str = strvar.previous
pre_prev_str = strvar.pre_previous
per_change_str = strvar.per_change
three_month_avg_str = strvar.three_month_avg

config_file = open("config/accounts_config.json")
config_data = json.load(config_file)
bs_config_data = config_data['balance_sheet']


def fetch_data_from_db(table, client_id, period, account_filter):
    three_month_before_date = period
    for i in range(2):
        last_date_of_previous_month = three_month_before_date.replace(
            day=1) + relativedelta(days=-1)   
        three_month_before_date = last_date_of_previous_month
    three_month_before_date = three_month_before_date.replace(day=1)


    if table == 'cashflow':
        accounts_data = ZohoAccount.objects.filter(
            account_for_coding__in=account_filter, client_id=client_id
        )
    else:
        accounts_data = ZohoAccount.objects.filter(
            account_type__in=account_filter, client_id=client_id
        )

    if table == 'pnl':
        transactions_data = ZohoTransaction.objects.filter(
            transaction_date__gte=three_month_before_date, transaction_date__lte=period
        ).all()
    else:
        transactions_data = ZohoTransaction.objects.filter(
            transaction_date__lte=period
        ).all()
    return accounts_data, transactions_data

def change_percentage(percent, trans_flag=False):
    if trans_flag:
        if percent > 100:
            return '>100'
        elif percent < -100:
            return '<-100'
    return str(round(percent))

def convert_to_indian_comma_notation(table, response_data):
    if table == 'pnl':
        income_obj = response_data[strvar.income]
        for key in income_obj:
            if key == 'data':
                for acc in income_obj['data']:
                    acc[current_str] = locale.format(
                    "%.2f", acc[current_str], grouping=True)
                    acc[previous_str] = locale.format(
                        "%.2f", acc[previous_str], grouping=True)
                    acc[three_month_avg_str] = locale.format(
                        "%.2f", acc[three_month_avg_str], grouping=True)
            elif key in (current_str, previous_str, three_month_avg_str):
                income_obj[key] = locale.format(
                    "%.2f", income_obj[key], grouping=True)
        
        expense_obj = response_data[strvar.expense]
        for category in expense_obj:
            dic = expense_obj[category]
            for key in dic:
                if key == 'data':
                    for acc in dic['data']:
                        acc[current_str] = locale.format(
                        "%.2f", acc[current_str], grouping=True)
                        acc[previous_str] = locale.format(
                            "%.2f", acc[previous_str], grouping=True)
                        acc[three_month_avg_str] = locale.format(
                            "%.2f", acc[three_month_avg_str], grouping=True)
                elif key in (current_str, previous_str, three_month_avg_str):
                    dic[key] = locale.format(
                    "%.2f", dic[key], grouping=True)
        
        for object in response_data:
            content = response_data[object]
            if object not in (strvar.income, strvar.expense):
                content[current_str] = locale.format(
                    "%.2f", content[current_str], grouping=True)
                content[previous_str] = locale.format(
                    "%.2f", content[previous_str], grouping=True)
                content[three_month_avg_str] = locale.format(
                    "%.2f", content[three_month_avg_str], grouping=True)

    elif table == 'balsheet':
        for acc_type in response_data:
            obj = response_data[acc_type]
            if type(obj) == list:
                for acc in obj:
                    acc[current_str] = locale.format(
                        "%.2f", acc[current_str], grouping=True)
                    acc[previous_str] = locale.format(
                        "%.2f", acc[previous_str], grouping=True)
            elif type(obj) == dict and 'data' in obj:
                obj['current_total'] = locale.format("%.2f", obj['current_total'], grouping=True)
                obj['previous_total'] = locale.format("%.2f", obj['previous_total'], grouping=True)
                account_lst = obj['data']
                for acc in account_lst:
                    acc[current_str] = locale.format(
                        "%.2f", acc[current_str], grouping=True)
                    acc[previous_str] = locale.format(
                        "%.2f", acc[previous_str], grouping=True)
            else:
                response_data[acc_type][current_str] = locale.format("%.2f", response_data[acc_type][current_str], grouping=True)
                response_data[acc_type][previous_str] = locale.format("%.2f", response_data[acc_type][previous_str], grouping=True)

    elif table == 'cashflow':
        for head in response_data:
            obj = response_data[head]
            if type(obj) == dict:
                obj[current_str] = locale.format("%.2f", obj[current_str], grouping=True)
                obj[previous_str] = locale.format("%.2f", obj[previous_str], grouping=True)
                obj[per_change_str] = change_percentage(obj[per_change_str])
            else:
                for activity in obj:
                    activity[current_str] = locale.format("%.2f", activity[current_str], grouping=True)
                    activity[previous_str] = locale.format("%.2f", activity[previous_str], grouping=True)
                    activity[per_change_str] = change_percentage(activity[per_change_str])
    
    elif table == 'pnl_trans':
        for key in response_data:
            trans_obj = response_data[key]
            trans_obj[current_str] = locale.format("%.2f", trans_obj[current_str], grouping=True)
            trans_obj[previous_str] = locale.format("%.2f", trans_obj[previous_str], grouping=True)
            trans_obj[pre_prev_str] = locale.format("%.2f", trans_obj[pre_prev_str], grouping=True)
            trans_obj[three_month_avg_str] = locale.format("%.2f", trans_obj[three_month_avg_str], grouping=True)
    
    elif table == 'pnl_totals':
        response_data[current_str] = locale.format("%.2f", response_data[current_str], grouping=True)
        response_data[previous_str] = locale.format("%.2f", response_data[previous_str], grouping=True)
        response_data[pre_prev_str] = locale.format("%.2f", response_data[pre_prev_str], grouping=True)
        response_data[three_month_avg_str] = locale.format("%.2f", response_data[three_month_avg_str], grouping=True)

    elif table == 'cashflow_bal':
        for key in response_data:
            trans_obj = response_data[key]
            trans_obj[current_str] = locale.format("%.2f", trans_obj[current_str], grouping=True)
            trans_obj[previous_str] = locale.format("%.2f", trans_obj[previous_str], grouping=True)
            trans_obj[change_str] = locale.format("%.2f", trans_obj[change_str], grouping=True)

    elif table == 'cashflow_totals':
        response_data[current_str] = locale.format("%.2f", response_data[current_str], grouping=True)
        response_data[previous_str] = locale.format("%.2f", response_data[previous_str], grouping=True)
        response_data[change_str] = locale.format("%.2f", response_data[change_str], grouping=True)

    elif table == 'insights_trans':
        for key in response_data:
            trans_obj = response_data[key]
            trans_obj[current_str] = locale.format("%.2f", trans_obj[current_str], grouping=True)
            trans_obj[previous_str] = locale.format("%.2f", trans_obj[previous_str], grouping=True)
            trans_obj[three_month_avg_str] = locale.format("%.2f", trans_obj[three_month_avg_str], grouping=True)

    elif table == 'insights_totals':
        response_data[current_str] = locale.format("%.2f", response_data[current_str], grouping=True)
        response_data[previous_str] = locale.format("%.2f", response_data[previous_str], grouping=True)
        response_data[three_month_avg_str] = locale.format("%.2f", response_data[three_month_avg_str], grouping=True)
    
    return response_data


def fetch_pnl_transactions(period, client_id, account):

    accounts_for_pnl_account = ZohoAccount.objects.filter(
        client_id=client_id,
        account_for_coding=account
    )

    account_ids = dict((acc.account_id, acc.get_account_for_coding_display()) for acc in accounts_for_pnl_account)

    prev_three_months = [period]
    current_date = period
    for i in range(2):
        last_date_of_previous_month = current_date.replace(
            day=1) + relativedelta(days=-1)
        prev_three_months.append(last_date_of_previous_month)
        current_date = last_date_of_previous_month

    related_transactions = ZohoTransaction.objects.filter(
        account_id__in=account_ids,
        transaction_date__gte=prev_three_months[2].replace(day=1),
        transaction_date__lte=period
    ).values('transaction_date', 'payee', 'debit_amount', 'credit_amount')

    response_data = {}

    for transaction in related_transactions:
        payee = transaction['payee']
        trans_date = transaction['transaction_date']

        if account in (strvar.direct_income, strvar.indirect_income):
            amount = transaction['credit_amount'] - transaction['debit_amount']
        else:
            amount = transaction['debit_amount'] - transaction['credit_amount']

        if payee not in response_data:
            response_data[payee] = {
                current_str: 0,
                previous_str: 0,
                pre_prev_str: 0,
                per_change_str: 0,
                prev_per_change_str: 0,
                three_month_avg_str: 0
            }

        if prev_three_months[1] < trans_date <= prev_three_months[0]:
            response_data[payee][current_str] += amount

        elif prev_three_months[2] < trans_date <= prev_three_months[1]:
            response_data[payee][previous_str] += amount
        
        else:
            response_data[payee][pre_prev_str] += amount

        response_data[payee][three_month_avg_str] += amount

    total = {
        current_str: 0,
        previous_str: 0,
        pre_prev_str: 0,
        per_change_str: 0,
        prev_per_change_str: 0,
        three_month_avg_str: 0
    }

    for k in response_data:
        obj = response_data[k]
        obj[per_change_str] = 0 if obj[previous_str] == 0 \
            else change_percentage((obj[current_str]/obj[previous_str]-1)*100, trans_flag=True)
        obj[prev_per_change_str] = 0 if obj[pre_prev_str] == 0 \
            else change_percentage((obj[previous_str]/obj[pre_prev_str]-1)*100, trans_flag=True)

        obj[three_month_avg_str] = obj[three_month_avg_str]/3
        total[current_str] += obj[current_str]
        total[previous_str] += obj[previous_str]
        total[pre_prev_str] += obj[pre_prev_str]
    
    total[per_change_str] = 0 if total[previous_str] == 0 \
        else change_percentage((total[current_str]/total[previous_str]-1)*100, trans_flag=True)
    total[prev_per_change_str] = 0 if total[pre_prev_str] == 0 \
        else change_percentage((total[previous_str]/total[pre_prev_str]-1)*100, trans_flag=True)
    
    # defining distinct payees for current financial year to check category or status of payee
    if period.month >= 4:
        curr_fy_start = f'{period.year}-04-01'
    else:
        curr_fy_start = f'{period.year-1}-04-01'

    curr_fy_prev = period.replace(day=1) + relativedelta(days=-1)
    distict_payees_in_cfy = ZohoTransaction.objects.filter(transaction_date__gte=curr_fy_start, transaction_date__lte=curr_fy_prev).values('payee').distinct()
    payees_for_cfy = dict((dic['payee'], 0) for dic in distict_payees_in_cfy)
    
    response_data_filtered = {}
    for k in response_data:
        obj = response_data[k]
        # defining status of payee
        if k in payees_for_cfy:
            obj['payee_category'] = 'Regular'
        else:
            obj['payee_category'] = 'New'

        if not account in (strvar.direct_income, strvar.indirect_income):
            if (abs(round(obj[current_str])), abs(round(obj[previous_str]))) == (0,0):
                continue
        total[three_month_avg_str] += obj[three_month_avg_str]
        response_data_filtered[k.title()] = obj

    response_data_filtered = dict(sorted(
        response_data_filtered.items(), 
        key=lambda x: (x[1]['payee_category'], x[1][current_str], x[1][previous_str]),
        reverse=True
        ))

    return (response_data_filtered, total, prev_three_months)


def get_accounts_from_account_for_coding(acc_for_codings):
    
    related_accounts = ZohoAccount.objects.filter(
        account_for_coding__in = acc_for_codings
    ).values_list('account_id')

    related_account_ids_lst = [acc_id[0] for acc_id in related_accounts]
    return related_account_ids_lst


def fetch_cashflow_balances(period, client_id, codings_list, sub_logic):
    accounts_according_to_coding = ZohoAccount.objects.filter(
        client_id=client_id,
        account_for_coding__in=codings_list
    )

    assets_related_types = bs_config_data['asset_related_accounts']

    account_ids = dict((acc.account_id, (acc.account_name, acc.account_type)) for acc in accounts_according_to_coding)

    prev_two_months = [period]
    current_date = period
    last_date_of_previous_month = current_date.replace(
        day=1) + relativedelta(days=-1)
    prev_two_months.append(last_date_of_previous_month)

    related_transactions = ZohoTransaction.objects.filter(
        account_id__in=account_ids,
        transaction_date__lte=period
    )

    response_data = {}

    for account in account_ids:
        account_name = account_ids[account][0]
        account_type = account_ids[account][1]
        current_period_total, previous_period_total = 0, 0
        response_data[account_name] = {
            current_str: 0,
            previous_str: 0,
            change_str: 0
        }
        for transaction in related_transactions:
            if account_type in assets_related_types:
                amount = transaction.debit_amount - transaction.credit_amount
            else:
                amount = transaction.credit_amount - transaction.debit_amount

            if transaction.account_id == account:
                if transaction.transaction_date <= prev_two_months[1]:
                    previous_period_total += amount
                current_period_total += amount
        
        if sub_logic == 0:
            response_data[account_name][change_str] = previous_period_total - current_period_total
        else:
            response_data[account_name][change_str] = current_period_total - previous_period_total
        response_data[account_name][current_str] = current_period_total
        response_data[account_name][previous_str] = previous_period_total


    total = {
        current_str: 0,
        previous_str: 0,
        change_str: 0,
    }

    response_data_filtered = {}

    for k in response_data:
        obj = response_data[k]
        
        total[current_str] += obj[current_str]
        total[previous_str] += obj[previous_str]
        total[change_str] += obj[change_str]

        if obj[current_str] == 0 and obj[previous_str] == 0:
            continue
        response_data_filtered[k] = obj
    
    response_data_filtered = dict(sorted(
        response_data_filtered.items(), 
        key=lambda x: (x[1][current_str], x[1][previous_str]),
        reverse=True
    ))
    

    return (response_data_filtered, total, prev_two_months)