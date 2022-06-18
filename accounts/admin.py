from django.contrib import admin
from accounts.models import ZohoAccount, ZohoTransaction

# Register your models here.
admin.site.register(ZohoAccount)
admin.site.register(ZohoTransaction)