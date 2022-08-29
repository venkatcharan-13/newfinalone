from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
import json
from cprofile.models import Company, CompanyAddress, CompanyContext, BankDetail
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
config_file = open("config/profile_config.json")
config_data = json.load(config_file)
overview_config_data = config_data['profile_overview']

@login_required()
def profiles(request):
    return render(request, 'overview.html')

@login_required()
def company(request):
    return render(request, 'company.html')

@csrf_exempt
def save_company_info(request):
    logged_client_id = request.user.id

    company = Company.objects.get(
        client_id=logged_client_id
    )
    company_address = CompanyAddress.objects.get(company=company.id)
    request_body = json.loads(request.body)
    
    company.company_name = request_body['edited_name']
    company.industry_name = request_body['edited_industry']
    company.entity_name = request_body['edited_entity']
    company.contact_person = request_body['edited_contact_person']
    company.company_email = request_body['edited_email']
    company.contact_number = request_body['edited_number']
    company.gst_number = request_body['edited_gst_no']
    company.pan_number = request_body['edited_pan_no']
    company.pf_number = request_body['edited_pf_no']
    company.esic_number = request_body['edited_esic_no']
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
    logged_client_id = request.user.id

    company = Company.objects.get(
        client_id=logged_client_id
    )
    company_context = CompanyContext.objects.get(company=company.id)
    request_body = json.loads(request.body)

    company_context.about = request_body['edited_about']
    company_context.work_profile = request_body['edited_work_profile']
    company_context.key_info = request_body['edited_key_info']
    company_context.specific_request = request_body['edited_specific_request']
    company_context.save()

    return JsonResponse({'Message': 'Success'})

@csrf_exempt
def save_bank_details(request):
    logged_client_id = request.user.id

    company = Company.objects.get(
        client_id=logged_client_id
    )

    BankDetail.objects.filter(company_id=company.id).delete()
    
    banks_list = json.loads(request.body)

    for bank in banks_list:
            new_bank = BankDetail.objects.create(company_id=company.id)
            new_bank.bank_name = bank['bank_name']
            new_bank.account_number = bank['bank_acc_num']
            new_bank.ifsc_code = bank['bank_ifsc_code']
            new_bank.location = bank['bank_branch']
            new_bank.save()
    
    return JsonResponse({'Message': 'Success'})

@login_required()
def connections(request):
    return render(request, 'connections.html')

@login_required()
def bank_details(request):
    return render(request, 'bankdet.html')
    

class Overview(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        response = {
            'add_ons_cards': []
        }
        for content in overview_config_data['add_ons_cards']:
            response['add_ons_cards'].append(content)
        
        return Response(response)


class CompanyInfo(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        logged_client_id = self.request.user.id
        company = Company.objects.get(
            client_id=logged_client_id
        )
        company_address = CompanyAddress.objects.get(company=company.id)
    
        company_information_response = {
            "name": company.company_name,
            "industry": company.industry_name,
            "entity_name": company.entity_name,
            "address": company_address.address_line,
            "city": company_address.city,
            "state": company_address.state,
            "zip": company_address.pin_code,
            "country": company_address.country,
            "contact_person": company.contact_person,
            "email": company.company_email,
            "phone": str(company.contact_number),
            "gst_no": company.gst_number,
            "pan_no": company.pan_number,
            "pf_no": company.pf_number,
            "esic_no": company.esic_number
        }

        return Response(company_information_response)

class ContextData(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        logged_client_id = self.request.user.id
        company = Company.objects.get(
            client_id=logged_client_id
        )
        company_context = CompanyContext.objects.get(company=company.id)

        context_response = {
            "about": company_context.about,
            "work_profile": company_context.work_profile,
            "key_info": company_context.key_info,
            "specific_request": company_context.specific_request
        }

        return Response(context_response)


class BanksData(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        logged_client_id = self.request.user.id
        company = Company.objects.get(
            client_id=logged_client_id
        )
        related_banks = BankDetail.objects.filter(
            company = company.id
        ).values()

        bank_details_response = []
        for bank in related_banks:
            bank_details_response.append(bank)
            
        return Response(bank_details_response)