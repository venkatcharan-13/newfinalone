from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import calendar
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from utility import analytics_util, insights_util, accounts_util
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

CURRENT_DATE_PERIOD = accounts_util.get_current_date_period()
current_period_str, previous_period_str  = "current_period", "previous_period"
response_data_str, totals_str = "response_data", "totals"

# Create your views here.
@login_required()
def analytics(request):
    return render(request, 'analytics.html')

@login_required()
def insights(request):
    return render(request, 'insights.html')

@login_required()
def insight_transactions(request, expense):
    selected_month = request.GET.get('selected_date')
    logged_client_id = request.user.id

    if selected_month is None:
        selected_month = CURRENT_DATE_PERIOD
    else:
        selected_month = datetime.strptime(selected_month, '%Y-%m-%d').date()
    
    # Fetching PNL transactions for each payee related to an account
    response_data, totals, prev_three_months = insights_util.fetch_insights_transaction(
        selected_month, logged_client_id, expense
    )
    response_data_modified = accounts_util.convert_to_indian_comma_notation('insights_trans', response_data)
    totals_modified = accounts_util.convert_to_indian_comma_notation('insights_totals', totals)

    current_month = prev_three_months[0]
    previous_month = prev_three_months[1]
    context = {
        'expense_head': expense,
        current_period_str: calendar.month_name[current_month.month] + '-' + str(current_month.year)[2:],
        previous_period_str: calendar.month_name[previous_month.month] + '-' + str(previous_month.year)[2:],
        response_data_str: response_data_modified,
        totals_str: totals
    }

    return render(request, 'insights_trans.html', context)

@login_required()
def deep_insights(request):
    return render(request, 'deep_insights.html')


class ReportData(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        selected_month = self.request.query_params.get('selected_date')
        logged_client_id = self.request.user.id

        monthly_sales, quarterly_sales, yearly_sales = analytics_util.get_sales_performance(logged_client_id, selected_month)
        tot_income_vs_tot_expenses = analytics_util.get_income_vs_expenses(logged_client_id, selected_month)
        cash_inflow_vs_outflow = analytics_util.get_cash_inflow_outflow(logged_client_id, selected_month)
        closing_bank_balance_trend = analytics_util.get_closing_bank_balance_trend(logged_client_id, selected_month)
        gross_profit_and_net_profit = analytics_util.get_gross_profit_and_net_profit(logged_client_id, selected_month)
        monthly_runaway = analytics_util.get_monthly_runaway(logged_client_id, selected_month)
        gp_vs_expenses_vs_ebitda = analytics_util.get_gp_vs_expenses_ebitda(logged_client_id, selected_month)
        gp_vs_expenses_vs_ebitda_values = tuple(gp_vs_expenses_vs_ebitda.values())
        monthly_cashflow_statements = analytics_util.get_monthly_cashflow_statement(logged_client_id, selected_month)
        pnl_summary = analytics_util.get_pnl_summary(logged_client_id, selected_month)
        balance_sheet_summary = analytics_util.get_balance_sheet_summary(logged_client_id, selected_month)
        cashflow_statement_summary = analytics_util.get_cashflow_summary(logged_client_id, selected_month)
        
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
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        selected_month = self.request.query_params.get('selected_date')
        logged_client_id = self.request.user.id

        if selected_month is None:
            selected_month = CURRENT_DATE_PERIOD
        else:
            selected_month = datetime.strptime(selected_month, '%Y-%m-%d').date()

        insights_data_response = {}
        current_month, current_month_year = selected_month.month, selected_month.year
        previous_month = (selected_month.replace(day=1) + relativedelta(days=-1)).month
        previous_month_year = (selected_month.replace(day=1) + relativedelta(days=-1)).year
        insights_data_response[current_period_str] = calendar.month_name[current_month] + '-' + str(current_month_year)[2:]
        insights_data_response[previous_period_str] = calendar.month_name[previous_month] + '-' + str(previous_month_year)[2:]
        insights_data_response[response_data_str] = insights_util.get_insights(logged_client_id, selected_month)

        return Response(insights_data_response)


class DeepInsightsData(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request, format=None):
        selected_month = self.request.query_params.get('selected_date')
        logged_client_id = self.request.user.id

        deep_insight_one = insights_util.get_deep_insight_one(logged_client_id, selected_month)
        deep_insight_two = insights_util.get_deep_insight_two(logged_client_id, selected_month)
        deep_insight_three = insights_util.get_deep_insight_three(logged_client_id, selected_month)
        deep_insight_four = insights_util.get_deep_insight_four(logged_client_id, selected_month)
        deep_insight_five = insights_util.get_deep_insight_five(logged_client_id, selected_month)
        deep_insight_six = insights_util.get_deep_insight_six(logged_client_id, selected_month)
        deep_insight_seven = insights_util.get_deep_insight_seven(logged_client_id, selected_month)
        deep_insight_eight = insights_util.get_deep_insight_eight(logged_client_id, selected_month)
        deep_insight_nine = insights_util.get_deep_insight_nine(logged_client_id, selected_month)
        deep_insight_ten = insights_util.get_deep_insight_ten(logged_client_id, selected_month)
        deep_insight_eleven = insights_util.get_deep_insight_eleven(logged_client_id, selected_month)
        deep_insight_twelve = insights_util.get_deep_insight_twelve(logged_client_id, selected_month)

        deep_insights_response = {
            'deep_insight_one': deep_insight_one,
            'deep_insight_two': deep_insight_two,
            'deep_insight_three': deep_insight_three,
            'deep_insight_four': deep_insight_four,
            'deep_insight_five': deep_insight_five,
            'deep_insight_six': deep_insight_six,
            'deep_insight_seven': deep_insight_seven,
            'deep_insight_eight': deep_insight_eight,
            'deep_insight_nine': deep_insight_nine,
            'deep_insight_ten': deep_insight_ten,
            'deep_insight_eleven': deep_insight_eleven,
            'deep_insight_twelve': deep_insight_twelve,
        }
        
        return Response(deep_insights_response)