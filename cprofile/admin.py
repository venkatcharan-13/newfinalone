from django.contrib import admin
from cprofile.models import Company, CompanyAddress, CompanyContext, BankDetail

# Register your models here.
admin.site.register(Company)
admin.site.register(CompanyAddress)
admin.site.register(CompanyContext)
admin.site.register(BankDetail)