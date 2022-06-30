import decimal
from accounts.models import ZohoAccount, ZohoTransaction
from dateutil.relativedelta import relativedelta
import locale

locale.setlocale(locale.LC_ALL, 'en_IN.utf8')


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


def convert_to_indian_comma_notation(response_data):
    for key in response_data:

        obj = response_data[key]

        if type(obj) == dict and 'current' in obj:
            obj['current'] = locale.format(
                "%d", obj['current'], grouping=True)
            obj['previous'] = locale.format(
                "%d", obj['previous'], grouping=True)
            obj['per_change'] = round(obj['per_change'])
            if 'three_month_avg' in obj:
                obj['three_month_avg'] = locale.format(
                    "%d", obj['three_month_avg'], grouping=True)

        elif type(obj) == list and obj:
            for acc in obj:
                acc['current'] = locale.format(
                    "%d", acc['current'], grouping=True)
                acc['previous'] = locale.format(
                    "%d", acc['previous'], grouping=True)
                acc['per_change'] = round(acc['per_change'])
                if 'three_month_avg' in acc:
                    acc['three_month_avg'] = locale.format(
                        "%d", acc['three_month_avg'], grouping=True)

        elif type(obj) == dict:
            for k in obj:
                for acc in obj[k]:
                    acc['current'] = locale.format(
                        "%d", acc['current'], grouping=True)
                    acc['previous'] = locale.format(
                        "%d", acc['previous'], grouping=True)
                    acc['per_change'] = round(acc['per_change'])
                    acc['three_month_avg'] = locale.format(
                        "%d", acc['three_month_avg'], grouping=True)

        elif type(obj) == float or type(obj) == decimal.Decimal:
            response_data[key] = locale.format("%d", obj, grouping=True)

    return response_data


def fetch_pnl_transactions(period, account):
    accounts_for_account = ZohoAccount.objects.filter(
        account_for_coding=account
    )
    account_ids_lst = []
    for acc in accounts_for_account:
        account_ids_lst.append(acc.account_id)

    related_transactions = ZohoTransaction.objects.filter(
        account_id__in=account_ids_lst,
        transaction_date__gte=period + relativedelta(months=-3),
        transaction_date__lte=period
    ).values('transaction_date', 'payee', 'debit_amount', 'credit_amount')

    response_data = {}

    for t in related_transactions:
        if t['payee'] not in response_data:
            response_data[t['payee']] = {
                'current': 0,
                'previous': 0,
                'per_change': 0,
                'three_month_avg': 0
            }

        if t['transaction_date'].month == period.month:
            response_data[t['payee']
                          ]['current'] += (t['debit_amount'] - t['credit_amount'])

        elif t['transaction_date'].month == (period.replace(day=1) + relativedelta(days=-1)).month:
            response_data[t['payee']
                          ]['previous'] += (t['debit_amount'] - t['credit_amount'])

        response_data[t['payee']
                      ]['three_month_avg'] += (t['debit_amount'] - t['credit_amount'])

    total = {
        'current': 0,
        'previous': 0,
        'per_change': 0,
        'three_month_avg': 0
    }

    for k in response_data:
        obj = response_data[k]
        obj['per_change'] = 0 if obj['previous'] == 0 \
            else round((obj['current']/obj['previous']-1)*100)
        obj['three_month_avg'] = round(obj['three_month_avg']/3)
        obj['current'] = round(obj['current'])
        obj['previous'] = round(obj['previous'])
        total['current'] += obj['current']
        total['previous'] += obj['previous']
        total['per_change'] += obj['per_change']
        total['three_month_avg'] += obj['three_month_avg']

    return (response_data, total)