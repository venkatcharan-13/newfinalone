from accounts.models import ZohoAccount, ZohoTransaction
from dateutil.relativedelta import relativedelta
from datetime import date, datetime
import locale

locale.setlocale(locale.LC_ALL, 'en_IN.utf8')
current_str, previous_str, pre_prev_str = "current", "previous", "pre_prev"
curr_per_str, prev_per_str = "curr_per", "prev_per"
per_change_str, prev_per_change_str, three_month_avg_str = "per_change", "prev_per_change", "three_month_avg"


def fetch_data_from_db(table, period, account_filter):
    if table == 'cashflow':
        accounts_data = ZohoAccount.objects.filter(
            account_for_coding__in=account_filter)
    else:
        accounts_data = ZohoAccount.objects.filter(
            account_type__in=account_filter)

    if table == 'pnl':
        transactions_data = ZohoTransaction.objects.filter(
            transaction_date__gte=period + relativedelta(months=-3), transaction_date__lte=period
        ).all()
    else:
        transactions_data = ZohoTransaction.objects.filter(
            transaction_date__lte=period
        ).all()
    return accounts_data, transactions_data

def change_percentage(percent):
    if percent > 100:
        return '>100'
    elif percent < -100:
        return '<-100'
    else:
        return str(round(percent))

def convert_to_indian_comma_notation(table, response_data):
    if table == 'pnl':
        income_obj = response_data['income']
        for key in income_obj:
            if key == 'data':
                for acc in income_obj['data']:
                    acc[current_str] = locale.format(
                    "%d", acc[current_str], grouping=True)
                    acc[previous_str] = locale.format(
                        "%d", acc[previous_str], grouping=True)
                    acc[per_change_str] = change_percentage(acc[per_change_str])
                    acc[three_month_avg_str] = locale.format(
                        "%d", acc[three_month_avg_str], grouping=True)
            else:
                income_obj[key] = locale.format(
                    "%d", income_obj[key], grouping=True)
        
        expense_obj = response_data['expense']
        for category in expense_obj:
            dic = expense_obj[category]
            for key in dic:
                if key == 'data':
                    for acc in dic['data']:
                        acc[current_str] = locale.format(
                        "%d", acc[current_str], grouping=True)
                        acc[previous_str] = locale.format(
                            "%d", acc[previous_str], grouping=True)
                        acc[per_change_str] = change_percentage(acc[per_change_str])
                        acc[three_month_avg_str] = locale.format(
                            "%d", acc[three_month_avg_str], grouping=True)
                else:
                    if key in (curr_per_str, prev_per_str):
                        dic[key] = change_percentage(dic[key])
                    else:
                        dic[key] = locale.format(
                            "%d", dic[key], grouping=True)
        
        for object in response_data:
            content = response_data[object]
            if object not in ('income', 'expense'):
                content[current_str] = locale.format(
                    "%d", content[current_str], grouping=True)
                content[previous_str] = locale.format(
                    "%d", content[previous_str], grouping=True)
                content[per_change_str] = change_percentage(content[per_change_str])
                if curr_per_str in content:
                    content[curr_per_str] = change_percentage(content[curr_per_str])
                    content[prev_per_str] = change_percentage(content[prev_per_str])
                content[three_month_avg_str] = locale.format(
                    "%d", content[three_month_avg_str], grouping=True)

    elif table == 'balsheet':
        for acc_type in response_data:
            obj = response_data[acc_type]
            if type(obj) == list:
                for acc in obj:
                    acc[current_str] = locale.format(
                        "%d", acc[current_str], grouping=True)
                    acc[previous_str] = locale.format(
                        "%d", acc[previous_str], grouping=True)
                    acc[per_change_str] = change_percentage(acc[per_change_str])
                    if three_month_avg_str in acc:
                        acc[three_month_avg_str] = locale.format(
                            "%d", acc[three_month_avg_str], grouping=True)
            else:
                response_data[acc_type] = locale.format("%d", response_data[acc_type], grouping=True)

    elif table == 'cashflow':
        for head in response_data:
            obj = response_data[head]
            if type(obj) == dict:
                obj[current_str] = locale.format("%d", obj[current_str], grouping=True)
                obj[previous_str] = locale.format("%d", obj[previous_str], grouping=True)
                obj[per_change_str] = change_percentage(obj[per_change_str])
            else:
                for activity in obj:
                    activity[current_str] = locale.format("%d", activity[current_str], grouping=True)
                    activity[previous_str] = locale.format("%d", activity[previous_str], grouping=True)
                    activity[per_change_str] = change_percentage(activity[per_change_str])

    return response_data


def fetch_pnl_transactions(period, account):

    accounts_for_pnl_account = ZohoAccount.objects.filter(
        account_for_coding=account
    ).values_list('account_id', 'account_for_coding')

    account_ids = dict(accounts_for_pnl_account)

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

        if account in ('Direct Income', 'Indirect Income'):
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
            else change_percentage((obj[current_str]/obj[previous_str]-1)*100)
        obj[prev_per_change_str] = 0 if obj[pre_prev_str] == 0 \
            else change_percentage((obj[previous_str]/obj[pre_prev_str]-1)*100)

        obj[three_month_avg_str] = round(obj[three_month_avg_str]/3)
        obj[current_str] = round(obj[current_str])
        obj[previous_str] = round(obj[previous_str])
        obj[pre_prev_str] = round(obj[pre_prev_str])
        total[current_str] += obj[current_str]
        total[previous_str] += obj[previous_str]
        total[pre_prev_str] += obj[pre_prev_str]
    
    total[per_change_str] = 0 if total[previous_str] == 0 \
        else change_percentage((total[current_str]/total[previous_str]-1)*100)
    total[prev_per_change_str] = 0 if total[pre_prev_str] == 0 \
        else change_percentage((total[previous_str]/total[pre_prev_str]-1)*100)
    
    response_data_filtered = {}
    for k in response_data:
        obj = response_data[k]
        if not account in ('Direct Income', 'Indirect Income'):
            if (abs(round(obj[current_str])), abs(round(obj[previous_str]))) == (0,0):
                continue
        total[three_month_avg_str] += obj[three_month_avg_str]
        response_data_filtered[k.title()] = obj

    response_data_filtered = dict(sorted(
        response_data_filtered.items(), 
        key=lambda x: (x[1][current_str], x[1][previous_str]),
        reverse=True
        ))

    return (response_data_filtered, total, prev_three_months)