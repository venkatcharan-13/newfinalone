from datetime import date
import locale
from django.shortcuts import render
from accounts.models import ZohoAccount, ZohoTransaction
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
def accounts(request):
    return render(request, 'accounts.html')

def balsheet(request):
    return render(request, 'balsheet.html')


class PnlData(APIView):
    authentication_classes = []
    permission_classes = []
    locale.setlocale(locale.LC_ALL, 'en_IN.utf8')

    # Fetching accounts and transactions from database
    accounts_data = ZohoAccount.objects.all()
    transactions_data = ZohoTransaction.objects.filter(
        transaction_date__gte='2022-03-01', transaction_date__lte='2022-05-31'
    ).all()

    def get(self, request, format=None):
        accounts_map, transactions_map = {}, {}

        # Generating accounts_map to map account IDs with their account_type and account_for_coding
        for account in self.accounts_data:
            if account.account_type in ('income', 'expense', 'other_expense', 'cost_of_goods_sold'):
                if account.account_type == 'other_expense':
                    accounts_map[account.account_id] = ('expense', account.account_for_coding)
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
        pnl_data = {
            'income': [],
            'expense': [],
            'cost_of_goods_sold': [],
            'gross_profit': 0,
            'ebitda': 0,
            'ebtd': 0
        }

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
                if transaction.transaction_date.month == 5:
                    temp["current"] += transaction.credit_amount - \
                        transaction.debit_amount
                elif transaction.transaction_date.month == 4:
                    temp["previous"] += transaction.credit_amount - \
                        transaction.debit_amount
                temp["three_month_avg"] += (
                    transaction.credit_amount - transaction.debit_amount)/3
            
            # Calculating percentage change
            if temp['previous'] == 0:
                temp['per_change'] = 0
            else:
                temp['per_change'] = (temp['previous']-temp['current'])/temp['current'] * 100
            # Rounding off all values
            temp['per_change'] = abs(round(float(temp["per_change"])))    
            temp['current'] = round(float(temp["current"]), 2)
            temp["previous"] = round(float(temp["previous"]), 2)
            temp["three_month_avg"] = round(float(temp["three_month_avg"]), 2)

            # Finally updating the data in response
            pnl_data[account_header[0]].append(temp)

        # Calculating total income and costs of goods sold
        income_total, cogs_total = 0, 0

        for acc in pnl_data['income']:
            income_total += acc['current']
        for acc in pnl_data['cost_of_goods_sold']:
            cogs_total += acc['current']
        # Changing sign for expenses
        for acc in pnl_data['expense']:
            acc['current'] = -acc['current']
            acc['previous'] = -acc['previous']
            acc['three_month_avg'] = -acc['three_month_avg']
        
        # Calculating total expense
        expense_total = 0
        for acc in pnl_data['expense']:
            expense_total += acc['current']
        
        # Calculating gross profit and EBITDA
        pnl_data['gross_profit'] = income_total - cogs_total
        pnl_data['ebitda'] = pnl_data['gross_profit'] - expense_total

        # Changing value to Indian comma notation
        for k in pnl_data:
            if k != 'gross_profit' and k != 'ebitda' and k != 'ebtd':
                for acc in pnl_data[k]:
                    acc['current'] = locale.format("%d", acc['current'], grouping=True)
                    acc['previous'] = locale.format("%d", acc['previous'], grouping=True)
                    acc['three_month_avg'] = locale.format("%d", acc['three_month_avg'], grouping=True)

        return Response(pnl_data)

class BalanceSheetData(APIView):
    authentication_classes = []
    permission_classes = []
    locale.setlocale(locale.LC_ALL, 'en_IN.utf8')

    # Fetching accounts and transactions from database
    accounts_data = ZohoAccount.objects.all()
    transactions_data = ZohoTransaction.objects.filter(
        transaction_date__lte='2022-06-23'
    ).all()
    
    def get(self, request, format=None):
        accounts_map, transactions_map = {}, {}
        balance_sheet_types = (
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

        for account in self.accounts_data:
            if account.account_type in balance_sheet_types:
                if account.account_type == 'bank':
                    accounts_map[account.account_id] = (
                    'cash', account.account_for_coding
                )
                else:
                    accounts_map[account.account_id] = (
                        account.account_type, account.account_for_coding
                    )
        
        for transaction in self.transactions_data:
            if transaction.account_id in accounts_map:
                account_header = accounts_map[transaction.account_id]
                if account_header not in transactions_map:
                    transactions_map[account_header] = []
                transactions_map[account_header].append(transaction)
        
        bal_sheet_data = {
            'accounts_payable': [],
            'accounts_receivable': [],
            'cash': [],
            'equity': [],
            'fixed_asset': [],
            'long_term_liability': [],
            'other_asset': [],
            'other_current_asset': [],
            'other_current_liability': [],
            'other_liability': [],
            'stock': []
        }

        for account_header in transactions_map:
            temp = {
                "account_header": account_header[1],
                "current": 0,
                "previous": 0,
                "per_change": 0,
                "three_month_avg": 0
            }

            for transaction in transactions_map[account_header]:
                temp["current"] += transaction.credit_amount - transaction.debit_amount
                if transaction.transaction_date < date(2022, 5, 1):
                    temp['previous'] += transaction.credit_amount - transaction.debit_amount
                temp["three_month_avg"] += (
                    transaction.credit_amount - transaction.debit_amount)/3
                
            if temp['previous'] == 0:
                temp['per_change'] = 0
            else:
                temp['per_change'] = (temp['previous']-temp['current'])/temp['current'] * 100
            # Rounding off all values
            temp['per_change'] = abs(round(float(temp["per_change"])))    
            temp['current'] = abs(round(float(temp["current"]), 2))
            temp["previous"] = abs(round(float(temp["previous"]), 2))
            temp["three_month_avg"] = abs(round(float(temp["three_month_avg"]), 2))

            bal_sheet_data[account_header[0]].append(temp)

        for k in bal_sheet_data:
            for acc in bal_sheet_data[k]:
                acc['current'] = locale.format("%d", acc['current'], grouping=True)
                acc['previous'] = locale.format("%d", acc['previous'], grouping=True)
                acc['three_month_avg'] = locale.format("%d", acc['three_month_avg'], grouping=True)
            
        return Response(bal_sheet_data)