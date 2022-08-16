from django.contrib import admin
from home.models import Notification, DashboardAccountStatus, PendingActionable, WatchOutPoint, StatutoryCompliance
from django.contrib.auth.models import User
from cprofile.models import Company
from taxes.models import TaxAlert, ITMonthlyStatus, ITQuarterlyStatus, GSTMonthlyStatus, GSTQuarterlyStatus
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


# Defining inlines for User
class CompanyInline(admin.TabularInline):
    model = Company
    extra = 0

class NotificationInline(admin.TabularInline):
    model = Notification
    extra = 0
class DashboardAccountStatusInline(admin.TabularInline):
    model = DashboardAccountStatus
    extra = 0
class PendingActionableInline(admin.TabularInline):
    model = PendingActionable
    extra = 0
class WatchOutPointInline(admin.TabularInline):
    model = WatchOutPoint
    extra = 0
class StatutoryComplianceInline(admin.TabularInline):
    model = StatutoryCompliance
    extra = 0

class RatioInline(admin.TabularInline):
    model = Ratio
    extra = 0

class TaxAlertInline(admin.TabularInline):
    model = TaxAlert
    extra = 0
class ITMonthlyStatusInline(admin.TabularInline):
    model = ITMonthlyStatus
    extra = 0
class ITQuarterlyStatusInline(admin.TabularInline):
    model = ITQuarterlyStatus
    extra = 0
class GSTMonthlyStatusInline(admin.TabularInline):
    model = GSTMonthlyStatus
    extra = 0
class GSTQuarterlyStatusInline(admin.TabularInline):
    model = GSTQuarterlyStatus
    extra = 0

@admin.action(description='Mark selected object to delete')
def delete_object(modeladmin, request, queryset):
    queryset.delete()

class UserAdmin(admin.ModelAdmin):
    inlines = [
        NotificationInline,
        CompanyInline,
        DashboardAccountStatusInline,
        PendingActionableInline,
        WatchOutPointInline,
        StatutoryComplianceInline,
        RatioInline,
        TaxAlertInline,
        ITMonthlyStatusInline,
        ITQuarterlyStatusInline,
        GSTMonthlyStatusInline,
        GSTQuarterlyStatusInline
    ]
    exclude = ['groups','user_permissions']
    actions = [delete_object]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)