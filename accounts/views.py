import copy
from datetime import date
from dateutil.relativedelta import relativedelta
import locale
from django.shortcuts import render
from utility import acc_util, jsonobj
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import ZohoAccount, ZohoTransaction
from django.db.models import Sum, Count
from django.db.models.functions import Round

locale.setlocale(locale.LC_ALL, 'en_IN.utf8')
SELECTED_DATE = date(2022, 6, 30)
pnl_pbt = {
    'current': 0,
    'previous': 0,
    'per_change': 0
}
pnl_dep_exp = {
    'current': 0,
    'previous': 0,
    'per_change': 0
}
cashflow_accounts = (
    'Bank Balance',
    'Cash Balance',
    'Accounts Receivable',
    'Other Current Assets',
    'Other Non Current Assets',
    'Trade Payables',
    'Other long term Liabilities & Provisions',
    'Other Liabilities',
    'Other Current Liabilities & Provisions',
    'Tangible Assets',
    'Short Term Loans & Advances',
    'Long Term Loans & Advances',
    'Short-term borrowings',
    'Long Term Borrowing',
    'Share Capital'
)

# Create your views here.


def accounts(request):
    return render(request, 'accounts.html')


def balsheet(request):
    return render(request, 'balsheet.html')


def cashflow(request):
    return render(request, 'cashflow.html')


def pnl_transaction(request, account):

    # Fetching PNL transactions for each payee related to an account
    response_data, totals = acc_util.fetch_pnl_transactions(SELECTED_DATE, account)

    context = {
        'account': account,
        'response_data': response_data,
        'totals': totals
    }
    return render(request, 'pnl_trans.html', context)


class PnlData(APIView):
    authentication_classes = []
    permission_classes = []

    # Fetching accounts and transactions from database
    pnl_accounts_data, transactions_data = acc_util.fetch_data_from_db(
        'pnl',
        SELECTED_DATE,
        ['income', 'expense', 'other_expense', 'cost_of_goods_sold']
    )

    def get(self, request, format=None):
        accounts_map, transactions_map = {}, {}

        # Generating accounts_map to map account IDs with their account_type and account_for_coding
        for account in self.pnl_accounts_data:
            if account.account_for_coding == 'Interest Expenses':
                accounts_map[account.account_id] = (
                    'interest_expenses', account.account_for_coding)
                continue

            if account.account_for_coding == 'Depreciation expenses':
                accounts_map[account.account_id] = (
                    'depreciation_expenses', account.account_for_coding)
                continue

            if account.account_type in ('other_expense', 'expense'):
                accounts_map[account.account_id] = (
                    'expense', account.account_for_coding, account.parent_account_name)
            else:
                accounts_map[account.account_id] = (
                    account.account_type, account.account_for_coding)

        # Generating transaction_map to map account headers with the corresponding list of transactions
        for transaction in self.transactions_data:
            if transaction.account_id in accounts_map:
                account_header = accounts_map[transaction.account_id]
                if account_header not in transactions_map:
                    transactions_map[account_header] = []
                transactions_map[account_header].append(transaction)

        # Defining structure for API response
        pnl_data = copy.deepcopy(jsonobj.json_structure['pnl_data'])

        # Filling up API response with relevant data
        for account_header in transactions_map:

            temp = {
                "account_header": account_header[1],
                "current": 0,
                "previous": 0,
                "per_change": 0,
                "three_month_avg": 0
            }

            # Calculating total amount for current, previous period and average of last 3 months for each account header
            for transaction in transactions_map[account_header]:
                if transaction.transaction_date.month == SELECTED_DATE.month:
                    temp["current"] += transaction.credit_amount - \
                        transaction.debit_amount
                elif transaction.transaction_date.month == SELECTED_DATE.month-1:
                    temp["previous"] += transaction.credit_amount - \
                        transaction.debit_amount
                temp["three_month_avg"] += transaction.credit_amount - \
                    transaction.debit_amount

            temp['three_month_avg'] /= 3

            # Calculating percentage change
            if temp['previous'] == 0:
                temp['per_change'] = 0
            else:
                temp['per_change'] = (
                    temp['current']/temp['previous'] - 1) * 100

            # Finally updating the data in response
            if len(account_header) == 2:
                pnl_data[account_header[0]].append(temp)

            else:
                if account_header[2] not in pnl_data[account_header[0]]:
                    pnl_data[account_header[0]][account_header[2]] = []
                pnl_data[account_header[0]][account_header[2]].append(temp)

        # Calculating total income and costs of goods sold
        income_total, cogs_total = {
            'current': 0,
            'previous': 0,
            'per_change': 0,
            'three_month_avg': 0
        }, {
            'current': 0,
            'previous': 0,
            'per_change': 0,
            'three_month_avg': 0
        }

        for acc in pnl_data['income']:
            income_total['current'] += acc['current']
            income_total['previous'] += acc['previous']
            income_total['three_month_avg'] += acc['three_month_avg']
        income_total['per_change'] = 0 if income_total['previous'] == 0 else (
            income_total['current'] / income_total['previous'] - 1) * 100

        for k in ('current', 'previous', 'per_change', 'three_month_avg'):
            pnl_data['total_income'][k] = income_total[k]

        for acc in pnl_data['cost_of_goods_sold']:
            cogs_total['current'] += acc['current']
            cogs_total['previous'] += acc['previous']
            cogs_total['three_month_avg'] += acc['three_month_avg']
        cogs_total['per_change'] = 0 if cogs_total['previous'] == 0 else round((
            cogs_total['current'] / cogs_total['previous'] - 1) * 100)

        # Changing sign for expenses
        for cat in pnl_data['expense']:
            for acc in pnl_data['expense'][cat]:
                acc['current'] = -acc['current']
                acc['previous'] = -acc['previous']
                acc['three_month_avg'] = -acc['three_month_avg']

        # Calculating total expense
        expense_total = {
            'current': 0,
            'previous': 0,
            'per_change': 0,
            'three_month_avg': 0
        }

        for cat in pnl_data['expense']:
            for acc in pnl_data['expense'][cat]:
                expense_total['current'] += acc['current']
                expense_total['previous'] += acc['previous']
                expense_total['three_month_avg'] += acc['three_month_avg']
        expense_total['per_change'] = 0 if expense_total['previous'] == 0 else (
            expense_total['current'] / expense_total['previous'] - 1) * 100

        # Calculating gross profit and EBITDA
        for k in income_total:
            pnl_data['gross_profit'][k] = income_total[k] - cogs_total[k]
            pnl_data['ebitda'][k] = pnl_data['gross_profit'][k] - \
                expense_total[k]

        # Calculating PBIT
        if pnl_data['depreciation_expenses']:
            pnl_data['depreciation_expenses'] = pnl_data['depreciation_expenses'][0]
            for k in income_total:
                pnl_data['pbit'][k] = pnl_data['ebitda'][k] - \
                    pnl_data['depreciation_expenses'][k]
        else:
            pnl_data['depreciation_expenses'] = {
                'current': 0,
                'previous': 0,
                'per_change': 0,
                'three_month_avg': 0
            }
            pnl_data['pbit'] = {
                'current': pnl_data['ebitda']['current'],
                'previous': pnl_data['ebitda']['previous'],
                'per_change': pnl_data['ebitda']['per_change'],
                'three_month_avg': pnl_data['ebitda']['three_month_avg']
            }
        # Calculating PBT
        if pnl_data['interest_expenses']:
            pnl_data['interest_expenses'] = pnl_data['interest_expenses'][0]
            for k in income_total:
                pnl_data['pbt'][k] = pnl_data['pbit'][k] - \
                    pnl_data['interest_expenses'][k]
        else:
            pnl_data['interest_expenses'] = {
                'current': 0,
                'previous': 0,
                'per_change': 0,
                'three_month_avg': 0
            }
            pnl_data['pbt'] = {
                'current': pnl_data['pbit']['current'],
                'previous': pnl_data['pbit']['previous'],
                'per_change': pnl_data['pbit']['per_change'],
                'three_month_avg': pnl_data['pbit']['three_month_avg']
            }
        pnl_data['pbt'] = copy.deepcopy(pnl_data['pbit'])

        for k in ('gross_profit', 'ebitda', 'depreciation_expenses', 'pbit', 'interest_expenses', 'pbt'):
            pnl_data[k]['curr_per'] = round(
                pnl_data[k]['current']/income_total['current'] * 100)
            pnl_data[k]['prev_per'] = round(
                pnl_data[k]['previous']/income_total['previous'] * 100)

        global pnl_pbt, pnl_dep_exp
        pnl_pbt = copy.deepcopy(pnl_data['pbt'])
        pnl_dep_exp = copy.deepcopy(pnl_data['depreciation_expenses'])

        pnl_data_response = acc_util.convert_to_indian_comma_notation(pnl_data)
        return Response(pnl_data_response)


class BalanceSheetData(APIView):
    authentication_classes = []
    permission_classes = []

    # Fetching accounts and transactions from database
    bal_accounts_data, transactions_data = acc_util.fetch_data_from_db(
        'balsheet',
        SELECTED_DATE,
        (
            'accounts_payable',
            'accounts_receivable',
            'bank',
            'cash',
            'equity',
            'fixed_asset',
            'long_term_liability',
            'other_asset',
            'other_current_asset',
            'other_current_liability',
            'other_liability',
            'stock'
        )
    )

    def get(self, request, format=None):
        accounts_map, transactions_map = {}, {}

        for account in self.bal_accounts_data:
            accounts_map[account.account_id] = (
                account.account_type, account.account_for_coding
            )
        # Finding transactions related to each account header
        for transaction in self.transactions_data:
            if transaction.account_id in accounts_map:
                account_header = accounts_map[transaction.account_id]
                if account_header not in transactions_map:
                    transactions_map[account_header] = []
                transactions_map[account_header].append(transaction)

        # Defining structure of API response for balance sheet data
        bal_sheet_data = copy.deepcopy(
            jsonobj.json_structure['bal_sheet_data'])

        # Filling up response with appropriate values
        for account_header in transactions_map:
            temp = {
                "account_header": account_header[1],
                "current": 0,
                "previous": 0,
                "per_change": 0
            }

            for transaction in transactions_map[account_header]:
                temp["current"] += transaction.credit_amount - \
                    transaction.debit_amount
                if transaction.transaction_date <= SELECTED_DATE + relativedelta(months=-1):
                    temp['previous'] += transaction.credit_amount - \
                        transaction.debit_amount

            if temp['previous'] == 0:
                temp['per_change'] = 0
            else:
                temp['per_change'] = (
                    temp['current']/temp['previous'] - 1) * 100

            bal_sheet_data[account_header[0]].append(temp)

        for k in ('accounts_receivable', 'fixed_asset', 'other_asset', 'other_current_asset', 'stock', 'cash', 'bank'):
            for acc in bal_sheet_data[k]:
                bal_sheet_data['total_assets'] += acc['current']

        for k in ('accounts_payable', 'long_term_liability', 'other_current_liability', 'other_liability'):
            for acc in bal_sheet_data[k]:
                bal_sheet_data['total_liabilities'] += acc['current']

        for acc in bal_sheet_data['equity']:
            bal_sheet_data['total_equity'] = acc['current']

        bal_sheet_data_response = acc_util.convert_to_indian_comma_notation(
            bal_sheet_data)
        return Response(bal_sheet_data_response)


class CashFlowData(APIView):
    authentication_classes = []
    permission_classes = []

    # Fetching data related to cashflow accounts
    cashflow_accounts_data, transactions_data = acc_util.fetch_data_from_db(
        'cashflow',
        SELECTED_DATE,
        cashflow_accounts
    )

    def get(self, request, format=None):

        # Defining structure for API response
        cashflow_data = copy.deepcopy(jsonobj.json_structure['cashflow_data'])

        accounts_map, transactions_map = {}, {}
        cashflow_data_uncategorized = {} # To store data related to all cashflow accounts

        for account in cashflow_accounts:
            cashflow_data_uncategorized[account] = {
                'current': 0,
                'previous': 0,
                'pre_prev': 0
            }

        for account in self.cashflow_accounts_data:
            accounts_map[account.account_id] = account.account_for_coding

        for transaction in self.transactions_data:
            if transaction.account_id in accounts_map:
                acccount_header = accounts_map[transaction.account_id]
                if acccount_header not in transactions_map:
                    transactions_map[acccount_header] = []
                transactions_map[acccount_header].append(transaction)

        for account_head in transactions_map:
            temp = {
                'current': 0,
                'previous': 0,
                'pre_prev': 0,
            }

            for transaction in transactions_map[account_head]:
                temp["current"] += transaction.credit_amount - \
                    transaction.debit_amount
                if transaction.transaction_date <= SELECTED_DATE + relativedelta(months=-1):
                    temp['previous'] += transaction.credit_amount - \
                        transaction.debit_amount
                if transaction.transaction_date <= SELECTED_DATE + relativedelta(months=-2):
                    temp['pre_prev'] += transaction.credit_amount - \
                        transaction.debit_amount

            temp['current'] = abs(round(float(temp['current'])))
            temp['previous'] = abs(round(float(temp['previous'])))
            temp['pre_prev'] = abs(round(float(temp['pre_prev'])))

            cashflow_data_uncategorized[account_head] = temp

        # Filling up response data with uncategorized and combined data
        temp = cashflow_data_uncategorized['Bank Balance']
        temp2 = cashflow_data_uncategorized['Cash Balance']
        cashflow_data['beginning_cash_balance'] = {
            'current': temp['previous'] + temp2['previous'],
            'previous': temp['pre_prev'] + temp2['pre_prev'],
            'per_change': 0 if temp['pre_prev'] == 0 else round(((temp['previous'] + temp2['previous']) / (temp['pre_prev'] + temp2['pre_prev'])-1) * 100)
        }

        for act, val in {'Net Income': pnl_pbt, 'Plus: Depreciation & Amortization': pnl_dep_exp}.items():
            cashflow_data['cashflow_from_operating_activities'].append({
                'activity': act,
                'current': round(val['current']),
                'previous': round(val['previous']),
                'per_change': round(val['per_change'])
            })

        temp = cashflow_data_uncategorized['Accounts Receivable']
        cashflow_data['cashflow_from_operating_activities'].append({
            'activity': 'Increase / decrease in sundry debtors',
            'current': temp['previous'] - temp['current'],
            'previous': temp['pre_prev'] - temp['previous'],
            'per_change': 0 if (temp['pre_prev'] - temp['previous']) == 0 else round(((temp['previous'] - temp['current'])/(temp['pre_prev'] - temp['previous'])-1) * 100)
        })

        temp = cashflow_data_uncategorized['Other Current Assets']
        temp2 = cashflow_data_uncategorized['Other Non Current Assets']
        cashflow_data['cashflow_from_operating_activities'].append({
            'activity': 'Increase / Decrease in Other Assets',
            'current': temp['previous'] + temp2['previous'] - (temp['current'] + temp2['current']),
            'previous': temp['pre_prev'] + temp2['pre_prev'] - (temp['previous'] + temp2['previous']),
            'per_change': 0 if temp['pre_prev'] + temp2['pre_prev'] - (temp['previous'] + temp2['previous']) == 0 else round(((temp['previous'] + temp2['previous'] - (temp['current'] + temp2['current']))/(temp['pre_prev'] + temp2['pre_prev'] - (temp['previous'] + temp2['previous']))-1)*100)
        })

        temp = cashflow_data_uncategorized['Trade Payables']
        cashflow_data['cashflow_from_operating_activities'].append({
            'activity': 'Increase / Decrease in sundry creditors',
            'current': temp['current'] - temp['previous'],
            'previous': temp['previous'] - temp['pre_prev'],
            'per_change': 0 if temp['previous'] - temp['pre_prev'] == 0 else round(((temp['current'] - temp['previous'])/(temp['previous'] - temp['pre_prev']) - 1) * 100)
        })

        temp = cashflow_data_uncategorized['Other long term Liabilities & Provisions']
        temp2 = cashflow_data_uncategorized['Other Liabilities']
        temp3 = cashflow_data_uncategorized['Other Current Liabilities & Provisions']
        a = temp['current'] + temp2['current'] + temp3['current'] - \
            (temp['previous'] + temp2['previous'] + temp3['previous'])
        b = temp['previous'] + temp2['previous'] + temp3['previous'] - \
            (temp['pre_prev'] + temp2['pre_prev'] + temp3['pre_prev'])
        cashflow_data['cashflow_from_operating_activities'].append({
            'activity': 'Increase / Decrease in Other Liability',
            'current': temp['current'] + temp2['current'] + temp3['current'] - (temp['previous'] + temp2['previous'] + temp3['previous']),
            'previous':  temp['previous'] + temp2['previous'] + temp3['previous'] - (temp['pre_prev'] + temp2['pre_prev'] + temp3['pre_prev']),
            'per_change': 0 if b == 0 else round((a/b-1)*100)
        })

        for key in cashflow_data['cashflow_from_operating_activities']:
            cashflow_data['net_cash_a']['current'] += key['current']
            cashflow_data['net_cash_a']['previous'] += key['previous']
        cashflow_data['net_cash_a']['per_change'] = 0 if cashflow_data['net_cash_a']['previous'] == 0 else round(
            cashflow_data['net_cash_a']['current']/cashflow_data['net_cash_a']['previous']-1) * 100

        temp = cashflow_data_uncategorized['Tangible Assets']
        cashflow_data['cashflow_from_investing_activities'].append({
            'activity': 'Investments in Property & Equipment',
            'current': temp['previous'] - temp['current'],
            'previous': temp['pre_prev'] - temp['previous'],
            'per_change': 0 if (temp['pre_prev'] - temp['previous']) == 0 else round((temp['previous'] - temp['current'])/(temp['pre_prev'] - temp['previous'])-1) * 100
        })

        cashflow_data['cashflow_from_investing_activities'].append({
            'activity': 'Purchase / Sale of investments',
            'current': 0,
            'previous': 0,
            'per_change': 0
        })

        for key in cashflow_data['cashflow_from_investing_activities']:
            cashflow_data['net_cash_b']['current'] += key['current']
            cashflow_data['net_cash_b']['previous'] += key['previous']
        cashflow_data['net_cash_b']['per_change'] = 0 if cashflow_data['net_cash_b']['previous'] == 0 else round(
            cashflow_data['net_cash_b']['current']/cashflow_data['net_cash_b']['previous']-1) * 100

        temp = cashflow_data_uncategorized['Short-term borrowings']
        temp2 = cashflow_data_uncategorized['Long Term Borrowing']
        temp3 = cashflow_data_uncategorized['Short Term Loans & Advances']
        temp4 = cashflow_data_uncategorized['Long Term Loans & Advances']
        a = temp['current'] + temp2['current'] - temp['previous'] - temp2['previous'] + \
            temp3['previous'] + temp4['previous'] - \
            temp3['current'] - temp4['current']
        b = temp['previous'] + temp2['previous'] - temp['pre_prev'] - temp2['pre_prev'] + \
            temp3['pre_prev'] + temp4['pre_prev'] - \
            temp3['previous'] - temp4['previous']
        cashflow_data['cashflow_from_financing_activities'].append({
            'activity': 'Issuance (repayment) of debt',
            'current': a,
            'previous': b,
            'per_change': 0 if b == 0 else round(a/b-1)*100
        })

        temp = cashflow_data_uncategorized['Share Capital']
        cashflow_data['cashflow_from_financing_activities'].append({
            'activity': 'Issuance (repayment) of equity',
            'current': temp['current'] - temp['previous'],
            'previous': temp['previous'] - temp['pre_prev'],
            'per_change': 0 if temp['previous'] - temp['pre_prev'] == 0 else round((temp['current'] - temp['previous'])/(temp['previous'] - temp['pre_prev'])-1)*100
        })

        for key in cashflow_data['cashflow_from_financing_activities']:
            cashflow_data['net_cash_c']['current'] += key['current']
            cashflow_data['net_cash_c']['previous'] += key['previous']
        cashflow_data['net_cash_c']['per_change'] = 0 if cashflow_data['net_cash_c']['previous'] == 0 else round(
            cashflow_data['net_cash_c']['current']/cashflow_data['net_cash_c']['previous']-1) * 100

        for k in ('current', 'previous'):
            cashflow_data['net_change_abc'][k] = (
                cashflow_data['net_cash_a'][k] + cashflow_data['net_cash_b'][k] + cashflow_data['net_cash_c'][k])
        cashflow_data['net_change_abc']['per_change'] = 0 if cashflow_data['net_change_abc']['previous'] == 0 else round(
            cashflow_data['net_change_abc']['current']/cashflow_data['net_change_abc']['previous']-1)*100

        cashflow_data['ending_cash_balance'] = {
            'current': cashflow_data['beginning_cash_balance']['current'] + cashflow_data['net_change_abc']['current'],
            'previous': cashflow_data['beginning_cash_balance']['previous'] + cashflow_data['net_change_abc']['previous']
        }
        cashflow_data['ending_cash_balance']['per_change'] = 0 if cashflow_data['ending_cash_balance']['previous'] == 0 else round(
            (cashflow_data['ending_cash_balance']['current'])/(cashflow_data['ending_cash_balance']['previous'])-1)*100

        cashflow_data_response = acc_util.convert_to_indian_comma_notation(
            cashflow_data)
        return Response(cashflow_data_response)
