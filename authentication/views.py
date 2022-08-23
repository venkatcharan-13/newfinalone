from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from utility.Zoho_scripts.dbservice import dbservice
from utility.Zoho_scripts import newzoho

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, ("Invalid credentials! Please enter correct username and password"))
            return redirect(login_view)
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully")
    return render(request, 'registration/logout.html')


class ZohoApi(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, client_id):
        db_obj = dbservice()
        try:
            zoho_credentials = db_obj.get_zoho_creds(client_id)
            zoho_domain = zoho_credentials['zoho_domain']
            zoho_organization_id = zoho_credentials['zoho_organization_id']
            zoho_client_id = zoho_credentials['zoho_client_id']
            zoho_client_secret = zoho_credentials['zoho_client_secret']
            zoho_refresh_token = zoho_credentials['zoho_refresh_token']
        except Exception as e:
            print(e)
            messages.error(request, ("Error in fetching Client's Zoho credentials"))
        else:
            try:
                access_token = newzoho.generate_access_token(zoho_domain, zoho_refresh_token, zoho_client_id, zoho_client_secret)
                fetched_accounts_data = newzoho.request_for_accounts(zoho_domain, zoho_organization_id, access_token)
                fetched_transactions_data = newzoho.request_for_transactions(zoho_domain, fetched_accounts_data, zoho_organization_id, access_token)
                newzoho.add_fetched_accounts_to_db(fetched_accounts_data, client_id, db_obj)
                newzoho.add_fetched_transactions_to_db(fetched_transactions_data, db_obj)
            except Exception as e:
                print(e)
                messages.error(request, ("Error in updating Client's data from Zoho"))
            else:
                messages.success(request, "Client's data has been updated successfully from Zoho")

        return Response({})
    