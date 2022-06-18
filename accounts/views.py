from urllib import response
from django.shortcuts import render
from accounts.models import ZohoAccount, ZohoTransaction
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
def accounts(request):
    return render(request, 'accounts.html')


class ZohoData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        data = {
            "d": 88
        }
        return Response(data)
