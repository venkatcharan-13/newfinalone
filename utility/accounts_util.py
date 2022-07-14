import decimal
from accounts.models import ZohoAccount, ZohoTransaction
from dateutil.relativedelta import relativedelta
from datetime import date, datetime
import locale

locale.setlocale(locale.LC_ALL, 'en_IN.utf8')
current_str, previous_str, per_change_str, three_month_avg_str = "current", "previous", "per_change", "three_month_avg"


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
                    acc[per_change_str] = round(acc[per_change_str])
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
                        acc[per_change_str] = round(acc[per_change_str])
                        acc[three_month_avg_str] = locale.format(
                            "%d", acc[three_month_avg_str], grouping=True)
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
                content[per_change_str] = round(content[per_change_str])
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
                    acc[per_change_str] = round(acc[per_change_str])
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
            else:
                for activity in obj:
                    activity[current_str] = locale.format("%d", activity[current_str], grouping=True)
                    activity[previous_str] = locale.format("%d", activity[previous_str], grouping=True)
    else:
        for key in response_data:

            obj = response_data[key]

            if type(obj) == dict and current_str in obj:
                obj[current_str] = locale.format(
                    "%d", obj[current_str], grouping=True)
                obj[previous_str] = locale.format(
                    "%d", obj[previous_str], grouping=True)
                obj[per_change_str] = round(obj[per_change_str])
                if three_month_avg_str in obj:
                    obj[three_month_avg_str] = locale.format(
                        "%d", obj[three_month_avg_str], grouping=True)

            elif type(obj) == list and obj:
                for acc in obj:
                    acc[current_str] = locale.format(
                        "%d", acc[current_str], grouping=True)
                    acc[previous_str] = locale.format(
                        "%d", acc[previous_str], grouping=True)
                    acc[per_change_str] = round(acc[per_change_str])
                    if three_month_avg_str in acc:
                        acc[three_month_avg_str] = locale.format(
                            "%d", acc[three_month_avg_str], grouping=True)

            elif type(obj) == dict:
                for k in obj:
                    for acc in obj[k]:
                        acc[current_str] = locale.format(
                            "%d", acc[current_str], grouping=True)
                        acc[previous_str] = locale.format(
                            "%d", acc[previous_str], grouping=True)
                        acc[per_change_str] = round(acc[per_change_str])
                        acc[three_month_avg_str] = locale.format(
                            "%d", acc[three_month_avg_str], grouping=True)

            elif type(obj) == float or type(obj) == decimal.Decimal:
                response_data[key] = locale.format("%d", obj, grouping=True)

    return response_data


def fetch_pnl_transactions(period, account):
    if period is None:
        period = date(2022, 6, 30)
    elif not isinstance(period, date):
        period = datetime.strptime(period, '%Y-%m-%d').date()

    accounts_for_pnl_account = ZohoAccount.objects.filter(
        account_for_coding=account
    ).values_list('account_id', 'account_for_coding')

    account_ids = dict(accounts_for_pnl_account)

    related_transactions = ZohoTransaction.objects.filter(
        account_id__in=account_ids,
        transaction_date__gte=period + relativedelta(months=-3),
        transaction_date__lte=period
    ).values('transaction_date', 'payee', 'debit_amount', 'credit_amount')

    response_data = {}

    for transaction in related_transactions:
        if account in ('Direct Income', 'Indirect Income'):
            amount = transaction['credit_amount'] - transaction['debit_amount']
        else:
            amount = transaction['debit_amount'] - transaction['credit_amount']

        if transaction['payee'] not in response_data:
            response_data[transaction['payee']] = {
                current_str: 0,
                previous_str: 0,
                per_change_str: 0,
                three_month_avg_str: 0
            }

        if transaction['transaction_date'].month == period.month:
            response_data[transaction['payee']][current_str] += amount

        elif transaction['transaction_date'].month == (period.replace(day=1) + relativedelta(days=-1)).month:
            response_data[transaction['payee']][previous_str] += amount

        response_data[transaction['payee']][three_month_avg_str] += amount

    total = {
        current_str: 0,
        previous_str: 0,
        per_change_str: 0,
        three_month_avg_str: 0
    }

    for k in response_data:
        obj = response_data[k]
        obj[per_change_str] = 0 if obj[previous_str] == 0 \
            else round((obj[current_str]/obj[previous_str]-1)*100)
        obj[three_month_avg_str] = round(obj[three_month_avg_str]/3)
        obj[current_str] = round(obj[current_str])
        obj[previous_str] = round(obj[previous_str])
        total[current_str] += obj[current_str]
        total[previous_str] += obj[previous_str]
        total[per_change_str] += obj[per_change_str]
        total[three_month_avg_str] += obj[three_month_avg_str]

    return (response_data, total)