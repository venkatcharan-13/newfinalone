from django.contrib import admin
from home.models import PendingActionable, WatchOutPoint, StatutoryCompliance
from django.contrib.auth.models import User
from cprofile.models import Company
from taxes.models import TaxAlert, ITMonthlyStatus, ITQuarterlyStatus, GSTMonthlyStatus, GSTQuarterlyStatus
# from accounts.admin import ZohoAccountInline

# Register your models here.
class PendingActionableAdmin(admin.ModelAdmin):
    list_filter = ['client']
    list_display = ['point', 'clientRemarks', 'status']

admin.site.register(PendingActionable, PendingActionableAdmin)

class WatchOutPointAdmin(admin.ModelAdmin):
    list_filter = ['client']

admin.site.register(WatchOutPoint, WatchOutPointAdmin)

class StatutoryComplianceAdmin(admin.ModelAdmin):
    list_filter = ['client']

admin.site.register(StatutoryCompliance, StatutoryComplianceAdmin)

# Defining inlines for User
class CompanyInline(admin.TabularInline):
    model = Company

class PendingActionableInline(admin.TabularInline):
    model = PendingActionable
class WatchOutPointInline(admin.TabularInline):
    model = WatchOutPoint
class StatutoryComplianceInline(admin.TabularInline):
    model = StatutoryCompliance

class TaxAlertInline(admin.TabularInline):
    model = TaxAlert
class ITMonthlyStatusInline(admin.TabularInline):
    model = ITMonthlyStatus
class ITQuarterlyStatusInline(admin.TabularInline):
    model = ITQuarterlyStatus
class GSTMonthlyStatusInline(admin.TabularInline):
    model = GSTMonthlyStatus
class GSTQuarterlyStatusInline(admin.TabularInline):
    model = GSTQuarterlyStatus

class UserAdmin(admin.ModelAdmin):
    inlines = [
        CompanyInline,
        PendingActionableInline,
        WatchOutPointInline,
        StatutoryComplianceInline,
        TaxAlertInline,
        ITMonthlyStatusInline,
        ITQuarterlyStatusInline,
        GSTMonthlyStatusInline,
        GSTQuarterlyStatusInline
    ]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)