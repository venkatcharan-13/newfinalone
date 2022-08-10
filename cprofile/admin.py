from django.contrib import admin
from cprofile.models import Company, CompanyAddress, CompanyContext, BankDetail

# Register your models here.
class CompanyContextInline(admin.TabularInline):
    model = CompanyContext
class CompanyAddressInline(admin.TabularInline):
    model = CompanyAddress
class BankDetailsInline(admin.TabularInline):
    model = BankDetail
    extra = 0
    

admin.site.register(CompanyAddress)
admin.site.register(CompanyContext)

class BankDetailAdmin(admin.ModelAdmin):
    list_filter = ['company']

admin.site.register(BankDetail, BankDetailAdmin)

class CompanyAdmin(admin.ModelAdmin):
    list_filter = ['client']
    list_display = ['company_name', 'entity_name', 'industry_name', 'contact_number', 'company_email']
    inlines = [
        CompanyContextInline,
        CompanyAddressInline,
        BankDetailsInline
    ]

admin.site.register(Company, CompanyAdmin)