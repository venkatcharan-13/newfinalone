from datetime import datetime, date
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from dateutil.relativedelta import relativedelta
from accounts.models import ZohoAccount, ZohoTransaction
from utility import analytics_util
import locale
from django.db.models import Sum

CURRENT_DATE = datetime.now()

# Create your views here.
def analytics(request):
    return render(request, 'analytics.html')


def insights(request):

    return render(request, 'insights.html')


def deep_insights(request):
    return render(request, 'deep_insights.html')


class ReportData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        monthly_sales, quarterly_sales, yearly_sales = analytics_util.get_sales_performance(CURRENT_DATE)
        tot_income_vs_tot_expenses = analytics_util.get_income_vs_expenses(CURRENT_DATE)
        cash_inflow_vs_outflow = analytics_util.get_cash_inflow_outflow(CURRENT_DATE)
        closing_bank_balance_trend = analytics_util.get_closing_bank_balance_trend(CURRENT_DATE)
        gross_profit_and_net_profit = analytics_util.get_gross_profit_and_net_profit(CURRENT_DATE)
        monthly_runaway = analytics_util.get_monthly_runaway(CURRENT_DATE)
        gp_vs_expenses_vs_ebitda = analytics_util.get_gp_vs_expenses_ebitda(CURRENT_DATE)
        gp_vs_expenses_vs_ebitda_values = tuple(gp_vs_expenses_vs_ebitda.values())
        monthly_cashflow_statements = analytics_util.get_monthly_cashflow_statement(CURRENT_DATE)
        pnl_summary = analytics_util.get_pnl_summary(CURRENT_DATE)
        balance_sheet_summary = analytics_util.get_balance_sheet_summary(CURRENT_DATE)
        cashflow_statement_summary = analytics_util.get_cashflow_summary(CURRENT_DATE)
        
        data = {
            "monthly_sales_performance": {
                "labels": monthly_sales.keys(),
                "chartLabel": "Monthly Sales Performance",
                "chartdata": monthly_sales.values(),
            },
            "quarterly_sales_performance": {
                "labels": quarterly_sales.keys(),
                "chartLabel": "Quarterly Sales Performance",
                "chartdata": quarterly_sales.values(),
            },
            "yearly_sales_performance": {
                "labels": yearly_sales.keys(),
                "chartLabel": "Yearly Sales Performance",
                "chartdata": yearly_sales.values(),
            },
            "income_vs_expenses": {
                "labels": tot_income_vs_tot_expenses.keys(),
                "chartLabel": "Income vs Expenses",
                "dataset": [
                    {
                        "label": "Income",
                        "profitData": [val['income'] for val in tot_income_vs_tot_expenses.values()]
                    },
                    {
                        "label": "Expenses",
                        "lossData": [val['expenses'] for val in tot_income_vs_tot_expenses.values()]
                    }
                ],
            },
            "cash_inflow_outflow": {
                "labels": cash_inflow_vs_outflow.keys(),
                "chartLabel": "Cash Inflow vs Outflow",
                "dataset": [
                    {
                        "label": "Credit",
                        "profitData": [val['credit'] for val in cash_inflow_vs_outflow.values()]
                    },
                    {
                        "label": "Debit",
                        "lossData": [val['debit'] for val in cash_inflow_vs_outflow.values()]
                    }
                ],
            },
             "closing_bank_balance_trend": {
                "labels": closing_bank_balance_trend.keys(),
                "chartLabel": "Closing Bank Balance Trend",
                "chartdata": closing_bank_balance_trend.values(),
            },
            "gross_and_net_profit": {
                "labels": gross_profit_and_net_profit.keys(),
                "chartLabel": "Gross Profit and Net Profit",
                "dataset": [
                    {
                        "label": "Gross Profit",
                        "grossProfitValues": [dic['gross_profit_per'] for dic in tuple(gross_profit_and_net_profit.values())]
                    },
                    {
                        "label": "Net Profit",
                        "netProfitValues": [dic['net_profit_per'] for dic in tuple(gross_profit_and_net_profit.values())]
                    }
                ]
            },
            "runaway": {
                "labels": monthly_runaway.keys(),
                "chartLabel": "Runaway for the last 6 months",
                "chartdata": monthly_runaway.values(),
            },
            "gp_vs_expenses_vs_ebitda": {
                "labels": gp_vs_expenses_vs_ebitda.keys(),
                "chartLabel": "Gross Profit vs Expenses vs EBITDA",
                "dataset": [
                    {
                        "label": "Gross Profit",
                        "data": [dic['gross_profit'] for dic in gp_vs_expenses_vs_ebitda_values]
                    },
                    {
                        "label": "Expenses",
                        "data": [dic['expenses'] for dic in gp_vs_expenses_vs_ebitda_values]
                    },
                    {
                        "label": "EBITDA",
                        "data": [dic['ebitda'] for dic in gp_vs_expenses_vs_ebitda_values]
                    }
                ],
            },
            "monthly_cashflow": {
                "labels": monthly_cashflow_statements.keys(),
                "chartLabel": "Gross Profit and Net Profit",
                "dataset": [
                    {
                        "label": "Cashflow from Operations",
                        "cashflowOperations": [dic['cf_from_operations'] for dic in tuple(monthly_cashflow_statements.values())]
                    },
                    {
                        "label": "Cashflow from Investing",
                        "cashflowInvesting": [dic['cf_from_investing'] for dic in tuple(monthly_cashflow_statements.values())]
                    },
                    {
                        "label": "Cashflow from Financing",
                        "cashflowFinancing": [dic['cf_from_financing'] for dic in tuple(monthly_cashflow_statements.values())]
                    },
                ]
            },
            "pnl_summary": pnl_summary,
            "bal_sheet_summary": balance_sheet_summary,
            "cashflow_summary": cashflow_statement_summary
        }
        
        return Response(data)


class InsightsData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        parent_summary = {
            'Advertising and Marketing Expenses': 0, 
            'Employment Expenses': 0, 
            'General & Admin Charges': 0, 
            'Brokerage & Commission Charges': 0, 
            'Rent, Rates & Repairs Expenses': 0
        }

        accounts_related_to_expenses = ZohoAccount.objects.filter(
            account_type__in = ('expense', 'other_expense')
        ).values_list('account_id', 'account_for_coding', 'parent_account_name')

        accounts_map = {}
        for account in accounts_related_to_expenses:
            accounts_map[account[0]] = account[2]
        
        prev_three_months = []
        current_date = CURRENT_DATE
        for i in range(3):
            last_date_of_previous_month = current_date.replace(
                day=1) + relativedelta(days=-1)
            prev_three_months.append(last_date_of_previous_month.date())
            current_date = last_date_of_previous_month
        
        transactions_for_last_three_months = ZohoTransaction.objects.filter(
            transaction_date__gte = prev_three_months[-1], account_id__in = accounts_map
        )

        transactions_map = {}
        for transaction in transactions_for_last_three_months:
            parent_account = accounts_map[transaction.account_id]
            if parent_account not in transactions_map:
                transactions_map[parent_account] = []
            transactions_map[parent_account].append(transaction)

        current, previous = prev_three_months[0], prev_three_months[1]
        for expense_head in parent_summary:
            temp = {
                "current": 0,
                "previous": 0,
                "per_change": 0,
                "three_month_avg": 0
            }
            if expense_head in transactions_map:
                for transaction in transactions_map[expense_head]:
                    if transaction.transaction_date.month == current.month and transaction.transaction_date.year == current.year:
                        temp['current'] += (transaction.debit_amount - transaction.credit_amount)
                    if transaction.transaction_date.month == previous.month and transaction.transaction_date.year == previous.year:
                        temp['previous'] += (transaction.debit_amount - transaction.credit_amount)
                    temp['three_month_avg'] += (transaction.debit_amount - transaction.credit_amount)

            temp['per_change'] = 0 if temp['previous'] == 0 else round((temp['current']/temp['previous']-1)*100)
            temp['three_month_avg'] = locale.format("%d", temp['three_month_avg'] / 3, grouping=True)
            temp['change'] = locale.format("%d", temp['current'] -  temp['previous'], grouping=True)
            temp['current'] = locale.format("%d", temp['current'], grouping=True)
            temp['previous'] = locale.format("%d", temp['previous'], grouping=True)
            parent_summary[expense_head] = temp

        current_month_payees = {}
        previous_month_payees = {}
        for expense_head in parent_summary:
            current_month_payees[expense_head] = {}
            previous_month_payees[expense_head] = {}
            if expense_head in transactions_map:
                temp_curr = current_month_payees[expense_head]
                temp_prev = previous_month_payees[expense_head]
                for transaction in transactions_map[expense_head]:
                    if transaction.transaction_date.month == current.month and transaction.transaction_date.year == current.year:
                        if transaction.payee not in temp_curr:
                            temp_curr[transaction.payee] = 0
                        temp_curr[transaction.payee] += (transaction.debit_amount - transaction.credit_amount)
                    if transaction.transaction_date.month == previous.month and transaction.transaction_date.year == previous.year:
                        if transaction.payee not in temp_prev:
                            temp_prev[transaction.payee] = 0
                        temp_prev[transaction.payee] += (transaction.debit_amount - transaction.credit_amount)
        
        insights_data = {}
        for key in parent_summary:
            insights_data[key] = []
            curr_dic = current_month_payees[key]
            prev_dic = previous_month_payees[key]
            for k in curr_dic:
                if k not in prev_dic:
                    insights_data[key].append(
                        {
                            'payee': k,
                            'additional': locale.format("%d", curr_dic[k], grouping=True)
                        }
                    )
                elif curr_dic[k] > prev_dic[k]:
                    insights_data[key].append(
                        {
                            'payee': k,
                            'additional': locale.format("%d", curr_dic[k] - prev_dic[k], grouping=True)
                        }
                    )

        data = {
            'advt_and_marketing_header': parent_summary['Advertising and Marketing Expenses'],
            'advt_and_marketing_insights': insights_data['Advertising and Marketing Expenses'],
            'employement_header':parent_summary['Employment Expenses'],
            'employement_insights':insights_data['Employment Expenses'],
            'rent_rates_and_repairs_header':parent_summary['Rent, Rates & Repairs Expenses'],
            'rent_rates_and_repairs_insights':insights_data['Rent, Rates & Repairs Expenses'],
            'brokerage_and_commission_header': parent_summary['Brokerage & Commission Charges'],
            'brokerage_and_commission_insights':insights_data['Brokerage & Commission Charges'],
            'general_and_admin_header': parent_summary['General & Admin Charges'],
            'general_and_admin_insights':insights_data['General & Admin Charges']
        }

        return Response(data)