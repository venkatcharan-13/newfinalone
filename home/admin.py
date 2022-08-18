from django.contrib import admin
from home.models import Notification, DashboardAccountStatus, PendingActionable, WatchOutPoint, StatutoryCompliance
# from accounts.admin import ZohoAccountInline
from accounts.models import Ratio

# Register your models here.

class NotificationAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    list_filter = ['client']
    list_display = ['content', 'created_on']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.order_by('created_on')
        return qs

admin.site.register(Notification, NotificationAdmin)


class DashboardAccountStatusAdmin(admin.ModelAdmin):
    date_hierarchy = 'period'
    list_filter = ['client']
    list_display = ['status_desc', 'status']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.order_by('status_desc', 'created_on')
        return qs

admin.site.register(DashboardAccountStatus, DashboardAccountStatusAdmin)

class PendingActionableAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    list_filter = ['client']
    list_display = ['point', 'client_remarks', 'status']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.order_by('created_on')
        return qs

admin.site.register(PendingActionable, PendingActionableAdmin)


class WatchOutPointAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    list_filter = ['client']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.order_by('created_on')
        return qs

admin.site.register(WatchOutPoint, WatchOutPointAdmin)


class StatutoryComplianceAdmin(admin.ModelAdmin):
    date_hierarchy = 'due_date'
    list_filter = ['client']

admin.site.register(StatutoryCompliance, StatutoryComplianceAdmin)
