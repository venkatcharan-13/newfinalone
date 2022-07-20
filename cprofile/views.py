from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
import json
from cprofile.models import Company, CompanyAddress, CompanyContext, BankDetail
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@login_required()
def profiles(request):
    return render(request, 'overview.html')

@login_required()
def company(request):
    return render(request, 'company.html')

@csrf_exempt
def save_company_info(request):
    company = Company.objects.get(id=1)
    company_address = CompanyAddress.objects.get(company=company.id)
    request_body = json.loads(request.body)
    
    company.company_name = request_body['edited_name']
    company.industry_name = request_body['edited_industry']
    company.company_email = request_body['edited_email']
    company.contact_number = request_body['edited_number']
    company.save()

    company_address.address_line = request_body['edited_address']
    company_address.city = request_body['edited_city']
    company_address.state = request_body['edited_state']
    company_address.pin_code = request_body['edited_zip']
    company_address.save()

    return JsonResponse({'Message': 'Success'})

@login_required()
def context(request):
    return render(request, 'context.html')

@csrf_exempt
def save_company_context(request):
    company = Company.objects.get(id=1)
    company_context = CompanyContext.objects.get(company=company.id)
    request_body = json.loads(request.body)

    company_context.about = request_body['edited_about']
    company_context.work_profile = request_body['edited_work_profile']
    company_context.key_info = request_body['edited_key_info']
    company_context.specific_request = request_body['edited_specific_request']
    company_context.save()

    return JsonResponse({'Message': 'Success'})

@login_required()
def connections(request):
    return render(request, 'connections.html')

@login_required()
def bank_details(request):
    return render(request, 'bankdet.html')
    

class CompanyInfo(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        company = Company.objects.get(id=1)
        company_address = CompanyAddress.objects.get(company=company.id)
    
        company_information_response = {
            "name": company.company_name,
            "industry": company.industry_name,
            "address": company_address.address_line,
            "city": company_address.city,
            "state": company_address.state,
            "zip": company_address.pin_code,
            "country": company_address.country,
            "email": company.company_email,
            "phone": str(company.contact_number),
            "gst_no": company.gst_number,
            "pan_no": company.pan_number,
            "pf_no": company.pf_number,
            "esic_no": company.esic_number
        }

        return Response(company_information_response)

class ContextData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        company = Company.objects.get(id=1)
        company_context = CompanyContext.objects.get(company=company.id)

        context_response = {
            "about": company_context.about,
            "work_profile": company_context.work_profile,
            "key_info": company_context.key_info,
            "specific_request": company_context.specific_request
        }

        return Response(context_response)


class BanksData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        company = Company.objects.get(id=1)
        related_banks = BankDetail.objects.filter(
            company = company.id
        ).values()

        bank_details_response = []
        for bank in related_banks:
            bank_details_response.append(bank)
            
        return Response(bank_details_response)