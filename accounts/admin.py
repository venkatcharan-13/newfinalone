from django.contrib import admin
from accounts.models import ZohoAccount, ZohoTransaction
from django.contrib.auth.models import User

# Register your models here.
class ZohoAccountAdmin(admin.ModelAdmin):
    list_filter = ['client', 'account_name']
    list_display = ['account_name', 'account_for_coding']

# class ZohoAccountInline(admin.TabularInline):
#     model = ZohoAccount

admin.site.register(ZohoAccount, ZohoAccountAdmin)
admin.site.register(ZohoTransaction)