from django.contrib import admin
from accounts.models import ZohoAccount, ZohoTransaction, ClientNote, Ratio
from django.utils.translation import gettext_lazy as _
from datetime import date

# Register your models here.
class ZohoAccountAdmin(admin.ModelAdmin):
    list_filter = ['client', 'account_type']
    list_display = ['account_name', 'account_for_coding', 'account_type', 'parent_account_name']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.order_by('account_name')
        return qs

class ZohoTransactionAdmin(admin.ModelAdmin):
    date_hierarchy = 'transaction_date'
    list_filter = ['account']
    list_display = ['categorized_transaction_id', 'account', 'get_account_for_coding',
    'transaction_date', 'debit_amount', 'credit_amount']

    @admin.display(description='Account for Coding')
    def get_account_for_coding(self, obj):
        return obj.account.get_account_for_coding_display()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.order_by('transaction_date')
        return qs

class ClientNoteAdmin(admin.ModelAdmin):
    date_hierarchy = 'period'
    list_filter = ['client']
    list_display = ['note', 'admin_response']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.order_by('period')
        return qs

class RatioAdmin(admin.ModelAdmin):
    date_hierarchy = 'period'
    list_filter = ['client']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.order_by('period')
        return qs


admin.site.register(ZohoAccount, ZohoAccountAdmin)
admin.site.register(ZohoTransaction, ZohoTransactionAdmin)
admin.site.register(ClientNote, ClientNoteAdmin)
admin.site.register(Ratio, RatioAdmin)