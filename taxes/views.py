from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
def taxes(request):
    return render(request, 'taxes.html')


def gst(request):
    return render(request, 'gst.html')


def other_taxes(request):
    return render(request, 'other_taxes.html')


class TaxesData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        print('Request Aa ri')
        income_tax_data_response = {}
        return Response(income_tax_data_response)