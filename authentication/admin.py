from django.contrib import admin
from authentication.models import Client
from home.models import NextDeliveryDate, ClientNotification, ContactPerson, DashboardAccountStatus, PendingActionable, WatchOutPoint, StatutoryCompliance
from cprofile.models import Company
from accounts.models import Ratio
from taxes.models import TaxAlert, IncomeTaxMonthlyStatus, IncomeTaxQuarterlyStatus, IncomeTaxAdvanceStatus, GSTR1MonthlyStatus, GSTR3BMonthlyStatus, GSTR8MonthlyStatus, ProvidentFundMonthlyStatus, ESICMonthlyStatus

# Register your models here.

# Inlines related to Home App (Dashboard section)
class ContactPersonInline(admin.TabularInline):
    model = ContactPerson
    extra = 0
class NextDeliveryDateInline(admin.TabularInline):
    model = NextDeliveryDate
    extra = 0
class ClientNotificationInline(admin.TabularInline):
    model = ClientNotification
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

# Inline related to Accounts App (Ratio actions)
class RatioInline(admin.TabularInline):
    model = Ratio
    extra = 0

# Inline related to Taxes App (Tax section)
class TaxAlertInline(admin.TabularInline):
    model = TaxAlert
    extra = 0
class IncomeTaxMonthlyStatusInline(admin.TabularInline):
    model = IncomeTaxMonthlyStatus
    extra = 0
class IncomeTaxQuarterlyStatusInline(admin.TabularInline):
    model = IncomeTaxQuarterlyStatus
    extra = 0
class IncomeTaxAdvanceStatusInline(admin.TabularInline):
    model = IncomeTaxAdvanceStatus
    extra = 0
class GSTR1MonthlyStatusInline(admin.TabularInline):
    model = GSTR1MonthlyStatus
    extra = 0
class GSTR3BMonthlyStatusInline(admin.TabularInline):
    model = GSTR3BMonthlyStatus
    extra = 0
class GSTR8MonthlyStatusInline(admin.TabularInline):
    model = GSTR8MonthlyStatus
    extra = 0
class ProvidentFundMonthlyStatusInline(admin.TabularInline):
    model = ProvidentFundMonthlyStatus
    extra = 0
class ESICMonthlyStatusInline(admin.TabularInline):
    model = ESICMonthlyStatus
    extra = 0

# Inline related to Cprofile App (Company profile)
class CompanyInline(admin.TabularInline):
    model = Company
    extra = 0


class ClientAdmin(admin.ModelAdmin):
    inlines = [
        ContactPersonInline,
        NextDeliveryDateInline,
        ClientNotificationInline,
        CompanyInline,
        DashboardAccountStatusInline,
        PendingActionableInline,
        WatchOutPointInline,
        StatutoryComplianceInline,
        RatioInline,
        TaxAlertInline,
        IncomeTaxMonthlyStatusInline,
        IncomeTaxQuarterlyStatusInline,
        IncomeTaxAdvanceStatusInline,
        GSTR1MonthlyStatusInline,
        GSTR3BMonthlyStatusInline,
        GSTR8MonthlyStatusInline,
        ProvidentFundMonthlyStatusInline,
        ESICMonthlyStatusInline
    ]

admin.site.register(Client, ClientAdmin)