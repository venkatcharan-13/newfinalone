import copy
from datetime import date
import locale
from django.shortcuts import render
from utility import accounts_util, acc_gets
from rest_framework.views import APIView
from rest_framework.response import Response

locale.setlocale(locale.LC_ALL, 'en_IN.utf8')
SELECTED_DATE = date(2022, 6, 30)

# Create your views here.


def accounts(request):
    return render(request, 'accounts.html')


def balsheet(request):
    return render(request, 'balsheet.html')


def cashflow(request):
    return render(request, 'cashflow.html')


def pnl_transaction(request, account):

    # Fetching PNL transactions for each payee related to an account
    response_data, totals = accounts_util.fetch_pnl_transactions(
        SELECTED_DATE, account)

    context = {
        'account': account,
        'response_data': response_data,
        'totals': totals
    }
    return render(request, 'pnl_trans.html', context)


def ratios(request):
    return render(request, 'ratios.html')


class PnlData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        selected_month = self.request.query_params.get('selected_date')

        pnl_data = acc_gets.get_pnl(selected_month)[0]
        pnl_data_response = accounts_util.convert_to_indian_comma_notation('pnl', pnl_data)
        return Response(pnl_data_response)


class BalanceSheetData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        selected_month = self.request.query_params.get('selected_date')

        bal_sheet_data = acc_gets.get_balsheet(selected_month)
        bal_sheet_data_response = accounts_util.convert_to_indian_comma_notation('balsheet', bal_sheet_data)
        current_year_earnings, retained_earnings = acc_gets.get_earnings(selected_month)
        
        bal_sheet_data_response['equity'].extend([
            {
                "account_header": "Current Year earnings",
                "current": locale.format("%d", current_year_earnings["current"], grouping=True),
                "previous": locale.format("%d", current_year_earnings["previous"], grouping=True),
                "per_change": 0 if current_year_earnings["previous"] == 0 else round((current_year_earnings["current"]/current_year_earnings["previous"] - 1)*100)
            },
            {
                "account_header": "Retained Earnings",
                "current": locale.format("%d", retained_earnings["current"], grouping=True),
                "previous": locale.format("%d", retained_earnings["previous"], grouping=True),
                "per_change": 0 if retained_earnings["previous"] == 0 else round((retained_earnings["current"]/retained_earnings["previous"] - 1)*100)
            }
        ])
        return Response(bal_sheet_data_response)


class CashFlowData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        selected_month = self.request.query_params.get('selected_date')

        cashflow_data = acc_gets.get_cashflow(selected_month)
        cashflow_data_response = accounts_util.convert_to_indian_comma_notation('cashflow', cashflow_data)
        return Response(cashflow_data_response)


class RatiosData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        selected_month = self.request.query_params.get('selected_date')

        pnl_data = acc_gets.get_pnl(selected_month)[0]
        balsheet_data = acc_gets.get_balsheet(selected_month)
        cashflow_data = acc_gets.get_cashflow(selected_month)

        ratios_data = {}
        ratio_head, current, previous, three_month_avg = "ratio_head", "current", "previous", "three_month_avg"

        gross_profit = pnl_data['gross_profit']
        ratios_data['gross_profit'] = {
            current: locale.format("%d", gross_profit[current], grouping=True),
            previous: locale.format("%d", gross_profit[previous], grouping=True),
            three_month_avg: locale.format("%d", gross_profit[three_month_avg], grouping=True)
        }

        pbt = pnl_data['pbt']
        ratios_data['pbt'] = {
            current: locale.format("%d", pbt[current], grouping=True),
            previous: locale.format("%d", pbt[previous], grouping=True),
            three_month_avg:  locale.format("%d", pbt[three_month_avg], grouping=True)
        }

        ratios_data['profit_ratios'] = []
        income = pnl_data['total_income']

        temporary_storage = {
            ratio_head: 'Gross Profit Margin',
            current: 0 if income[current] == 0 else gross_profit[current]/income[current],
            previous: 0 if income[previous] == 0 else gross_profit[previous]/income[previous],
            three_month_avg: 0 if income[three_month_avg] == 0 else gross_profit[three_month_avg]/income[three_month_avg]
        }
        ratios_data['profit_ratios'].append(temporary_storage)

        temporary_storage = {
            ratio_head: 'Net Profit Margin',
            current: 0 if income[current] == 0 else pbt[current]/income[current],
            previous: 0 if income[previous] == 0 else pbt[previous]/income[previous],
            three_month_avg: 0 if income[three_month_avg] == 0 else pbt[three_month_avg]/income[three_month_avg]
        }
        ratios_data['profit_ratios'].append(temporary_storage)

        equity = balsheet_data['equity'][0]
        temporary_storage = {
            ratio_head: 'Return on Equity',
            current: 0 if equity[current] == 0 else pbt[current]/equity[current],
            previous: 0 if equity[previous] == 0 else pbt[previous]/equity[previous],
            three_month_avg:0 if equity[three_month_avg] == 0 else pbt[three_month_avg]/equity[three_month_avg]
        }
        ratios_data['profit_ratios'].append(temporary_storage)

        cf_operations = cashflow_data['net_cash_a']
        temporary_storage = {
            ratio_head: 'Operating Cash Flow to Sales Ratio',
            current: 0 if income[current] == 0 else cf_operations[current]/income[current],
            previous: 0 if income[previous] == 0 else cf_operations[previous]/income[previous],
            three_month_avg: 0
        }
        ratios_data['profit_ratios'].append(temporary_storage)

        ratios_data['liquidity_ratio'] = []
        
        accrec = balsheet_data['accounts_receivable'][0]
        cash = balsheet_data['cash'][0]
        bank = balsheet_data['bank'][0]
        ocurra = balsheet_data['other_current_asset'][0]
        accpay = balsheet_data['accounts_payable'][0]
        
        ocurrl = {current: 0, previous: 0, three_month_avg: 0}
        for account in balsheet_data['other_current_liability']:
            ocurrl[current] += account[current]
            ocurrl[previous] += account[previous]
            ocurrl[three_month_avg] += account[three_month_avg]

        temporary_storage = {
            ratio_head: 'Working Capital Ratio / Current Ratio',
            current: 0 if (accpay[current]+ocurrl[current]) == 0 else (accrec[current]+cash[current]+bank[current]+ocurra[current])/(accpay[current]+ocurrl[current]),
            previous: 0 if (accpay[previous]+ocurrl[previous]) == 0 else (accrec[previous]+cash[previous]+bank[previous]+ocurra[previous])/(accpay[previous]+ocurrl[previous]),
            three_month_avg: 0 if (accpay[three_month_avg]+ocurrl[three_month_avg]) == 0 else (accrec[three_month_avg]+cash[three_month_avg]+bank[three_month_avg]+ocurra[three_month_avg])/(accpay[three_month_avg]+ocurrl[three_month_avg])
        }
        ratios_data['liquidity_ratio'].append(temporary_storage)

        for account in balsheet_data['other_current_liability']:
            if account['account_header'] == 'Short-term borrowings':
                st_borrow = copy.deepcopy(account)
                break
        else:
            st_borrow = {current: 0, previous: 0, three_month_avg: 0}
        for account in balsheet_data['long_term_liability']:
            if account['account_header'] == 'Long Term Borrowing':
                lt_borrow = copy.deepcopy(account)
                break
        else:
            lt_borrow = {current: 0, previous: 0, three_month_avg: 0}

        temporary_storage = {
            ratio_head: 'Cashflow to Debt Ratio',
            current: 0 if (st_borrow[current] + lt_borrow[current]) == 0 else cf_operations[current]/(st_borrow[current] + lt_borrow[current]),
            previous: 0 if (st_borrow[current] + lt_borrow[current]) == 0 else cf_operations[previous]/(st_borrow[previous] + lt_borrow[previous]),
            three_month_avg: 0
        }

        ratios_data['liquidity_ratio'].append(temporary_storage)

        ratios_data['op_eff_ratios'] = []
        
        if pnl_data['cost_of_goods_sold']:
            cogs = pnl_data['cost_of_goods_sold']
        else:
            cogs = {
                current: 0, previous: 0, 'pre_prev': 0, three_month_avg: 0
            }
        
        if balsheet_data['stock']:
            inventory = balsheet_data['stock']
        else:
            inventory = {
                current: 0, previous: 0, 'pre_prev': 0, three_month_avg: 0
            }

        temporary_storage = {
            ratio_head: 'Inventory turnover',
            current: 0 if (inventory[current] + inventory[previous]) == 0 else cogs[current]/(inventory[current] + inventory[previous]) * 2,
            previous: 0 if (inventory[previous] + inventory['pre_prev']) == 0 else cogs[previous]/(inventory[previous] + inventory['pre_prev']) * 2,
            three_month_avg: 0 if (inventory[three_month_avg]) == 0 else cogs[three_month_avg]/(inventory[three_month_avg])
        }
        ratios_data['op_eff_ratios'].append(temporary_storage)

        temporary_storage = {
            ratio_head: 'Accounts receivable turnover',
            current: 0 if (accrec[current] + accrec[previous]) == 0 else income[current]/((accrec[current] + accrec[previous])/2),
            previous: 0 if (accrec[previous] + accrec['pre_prev']) == 0 else income[previous]/((accrec[previous] + accrec['pre_prev'])/2),
            three_month_avg: 0 if (accrec[three_month_avg]) == 0 else income[three_month_avg]/(accrec[three_month_avg]),
        }
        ratios_data['op_eff_ratios'].append(temporary_storage)

        temporary_storage = {
            ratio_head: 'Days payable outstanding (DPO)',
            current: 0 if cogs[current] == 0 else (accpay[current] + accpay[previous])/(2*cogs[current])*365,
            previous: 0 if cogs[previous] == 0 else (accpay[previous] + accpay['pre_prev'])/(2*cogs[previous])*365,
            three_month_avg: 0 if cogs[three_month_avg] == 0 else (accpay[three_month_avg])/(cogs[three_month_avg])*365,
        }
        ratios_data['op_eff_ratios'].append(temporary_storage)
        

        ratios_data['solvency_ratios'] = []
        
        share_cap = balsheet_data['equity'][0]
        temporary_storage = {
            ratio_head: 'Debt to equity ratio',
            current: 0 if share_cap[current] == 0 else (st_borrow[current] + lt_borrow[current])/share_cap[current],
            previous: 0 if share_cap[previous] == 0 else (st_borrow[previous] + lt_borrow[previous])/share_cap[previous],
            three_month_avg: 0 if share_cap[three_month_avg] == 0 else (st_borrow[three_month_avg] + lt_borrow[three_month_avg])/share_cap[three_month_avg]
        }
        ratios_data['solvency_ratios'].append(temporary_storage)

        mbr = {
            ratio_head: 'Monthly Burn Rate',
            current: cash[current] + bank[current] - cash[previous] - bank[previous],
            previous: cash[previous] + bank[previous] - cash['pre_prev'] - bank['pre_prev'],
            three_month_avg: cash[three_month_avg] + bank[three_month_avg]
        }
        ratios_data['solvency_ratios'].append(mbr)

        temporary_storage = {
            ratio_head: 'Runaway',
            current: 0 if mbr[current] == 0 else (cash[current] + bank[current])/mbr[current],
            previous: 0 if mbr[previous] == 0 else (cash[previous] + bank[previous])/mbr[previous],
            three_month_avg: 0 if mbr[three_month_avg] == 0 else (cash[three_month_avg] + bank[three_month_avg])/mbr[three_month_avg],
        }
        ratios_data['solvency_ratios'].append(temporary_storage)

        for obj in ratios_data:
            if type(ratios_data[obj]) == list:
                for ratio in ratios_data[obj]:
                    ratio[current] = round(ratio[current], 2)
                    ratio[previous] = round(ratio[previous], 2)
                    ratio[three_month_avg] = round(ratio[three_month_avg], 2)
        
        mbr[current] = locale.format("%d", mbr[current], grouping=True)
        mbr[previous] = locale.format("%d", mbr[previous], grouping=True)
        mbr[three_month_avg] = locale.format("%d", mbr[three_month_avg], grouping=True)
                    
        return Response(ratios_data)