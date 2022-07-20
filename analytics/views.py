from datetime import date
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from utility import analytics_util, insights_util

SELECTED_DATE = date(2022, 6, 30)

# Create your views here.
@login_required()
def analytics(request):
    return render(request, 'analytics.html')

@login_required()
def insights(request):
    return render(request, 'insights.html')

@login_required()
def deep_insights(request):
    return render(request, 'deep_insights.html')


class ReportData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        selected_month = self.request.query_params.get('selected_date')

        monthly_sales, quarterly_sales, yearly_sales = analytics_util.get_sales_performance(selected_month)
        tot_income_vs_tot_expenses = analytics_util.get_income_vs_expenses(selected_month)
        cash_inflow_vs_outflow = analytics_util.get_cash_inflow_outflow(selected_month)
        closing_bank_balance_trend = analytics_util.get_closing_bank_balance_trend(selected_month)
        gross_profit_and_net_profit = analytics_util.get_gross_profit_and_net_profit(selected_month)
        monthly_runaway = analytics_util.get_monthly_runaway(selected_month)
        gp_vs_expenses_vs_ebitda = analytics_util.get_gp_vs_expenses_ebitda(selected_month)
        gp_vs_expenses_vs_ebitda_values = tuple(gp_vs_expenses_vs_ebitda.values())
        monthly_cashflow_statements = analytics_util.get_monthly_cashflow_statement(selected_month)
        pnl_summary = analytics_util.get_pnl_summary(selected_month)
        balance_sheet_summary = analytics_util.get_balance_sheet_summary(selected_month)
        cashflow_statement_summary = analytics_util.get_cashflow_summary(selected_month)
        
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
        selected_month = self.request.query_params.get('selected_date')

        insights_data_response = insights_util.get_insights(selected_month)
        return Response(insights_data_response)


class DeepInsightsData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        selected_month = self.request.query_params.get('selected_date')

        deep_insight_one = insights_util.get_deep_insight_one(selected_month)
        deep_insight_two = insights_util.get_deep_insight_two(selected_month)
        deep_insight_three = insights_util.get_deep_insight_three(selected_month)
        deep_insight_four = insights_util.get_deep_insight_four(selected_month)
        deep_insight_five = insights_util.get_deep_insight_five(selected_month)
        deep_insight_six = insights_util.get_deep_insight_six(selected_month)
        deep_insight_seven = insights_util.get_deep_insight_seven(selected_month)
        deep_insight_eight = insights_util.get_deep_insight_eight(selected_month)
        deep_insight_nine = insights_util.get_deep_insight_nine(selected_month)
        deep_insight_ten = insights_util.get_deep_insight_ten(selected_month)
        deep_insight_eleven = insights_util.get_deep_insight_eleven(selected_month)
        deep_insight_twelve = insights_util.get_deep_insight_twelve(selected_month)

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