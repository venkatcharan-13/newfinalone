import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from utility.Zoho_scripts import dbservice
from django.views.decorators.csrf import csrf_exempt

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
        print(client_id)
        return Response({'kuch': client_id})
    