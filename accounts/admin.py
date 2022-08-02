from django.contrib import admin
from accounts.models import ZohoAccount, ZohoTransaction, Ratio

# Register your models here.
class ZohoAccountAdmin(admin.ModelAdmin):
    list_filter = ['client', 'account_name']
    list_display = ['account_name', 'account_for_coding']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.order_by('account_name')
        return qs

class ZohoTransactionAdmin(admin.ModelAdmin):
    list_filter = ['account']
    list_display = ['categorized_transaction_id', 'account', 'payee', 
    'transaction_date', 'debit_amount', 'credit_amount']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.order_by('transaction_date')
        return qs


admin.site.register(ZohoAccount, ZohoAccountAdmin)
admin.site.register(ZohoTransaction, ZohoTransactionAdmin)
admin.site.register(Ratio)