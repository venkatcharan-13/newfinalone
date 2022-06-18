from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

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
        data = {
            "sales_performance": {
                "labels": ['April', 'May', 'June', 'July'],
                "chartLabel": "Sales Performance",
                "chartdata": [17, 26, 53, 96],
            },
            "profit_and_loss": {
                "labels": ['April', 'May', 'June', 'July'],
                "chartLabel": "Profit vs Loss",
                "dataset": [
                    {
                        "label": "Profit",
                        "profitData": [17, 26, 53, 96]
                    },
                    {
                        "label": "Loss",
                        "lossData": [-5, -15, -45, -85]
                    }
                ],
            },
            "cash_inflow_outflow": {
                "labels": ['April', 'May', 'June', 'July'],
                "chartLabel": "Cash Inflow vs Outflow",
                "dataset": [
                    {
                        "label": "Inflow",
                        "inflowData": [17, 26, 53, 96]
                    },
                    {
                        "label": "Outflow",
                        "outflowData": [-5, -15, -45, -85]
                    }
                ],
            },
            "runaway": {
                "labels": ['April', 'May', 'June', 'July', 'August'],
                "chartLabel": "Runaway for the Month",
                "chartdata": [17, 26, 53, 96, 47],
            },
            "cogs_breakdown": {
                "labels": ['April', 'May', 'June', 'July', 'August'],
                "chartLabel": "COGS breakdown for the Month",
                "chartdata": [1745, 2908, 539, 969, 437],
            },
            "productwise_revenue": {
                "labels": ['April', 'May', 'June', 'July'],
                "chartLabel": "Productwise revenue contribution",
                "dataset": [
                    {
                        "label": "LabelA",
                        "aData": [17, 26, 53, 96]
                    },
                    {
                        "label": "LabelB",
                        "bData": [5, 15, 45, 85]
                    }
                ],
            },
        }
        return Response(data)
