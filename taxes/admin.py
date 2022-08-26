from django.contrib import admin
from django.db.models import Q
from taxes.models import TaxAlert, IncomeTaxMonthlyStatus, IncomeTaxQuarterlyStatus, GSTMonthlyStatus, GSTQuarterlyStatus, OtherTaxesMonthlyStatus, OtherTaxesQuarterlyStatus
from django.utils.translation import gettext_lazy as _

# Register your models here.
class FinancialYearMonthlyListFilter(admin.SimpleListFilter):
    title = _('Financial Year')
    parameter_name = 'fy'

    def lookups(self, request, model_admin):
        return (
            ('2019', _('FY 2019-20')),
            ('2020', _('FY 2020-21')),
            ('2021', _('FY 2021-22')),
            ('2022', _('FY 2022-23')),
        )

    def queryset(self, request, queryset):
        if self.value():
            case1q1 = Q(month_name__gte=4)
            case1q2 = Q(year=int(self.value()))
            case2q1 = Q(month_name__lte=3) 
            case2q2 = Q(year=int(self.value())+1)
            filter = (case1q1 & case1q2)
            filter2 = (case2q1 & case2q2)
            return queryset.filter(
                filter|filter2
            )

class FinancialYearQuarterlyListFilter(admin.SimpleListFilter):
    title = _('Financial Year')
    parameter_name = 'fy'

    def lookups(self, request, model_admin):
        return (
            ('2019', _('FY 2019-20')),
            ('2020', _('FY 2020-21')),
            ('2021', _('FY 2021-22')),
            ('2022', _('FY 2022-23')),
        )

    def queryset(self, request, queryset):
        if self.value():
            case1q1 = Q(quarter__in=['Q1', 'Q2', 'Q3'])
            case1q2 = Q(year=int(self.value()))
            case2q1 = Q(quarter='Q4') 
            case2q2 = Q(year=int(self.value())+1)
            filter = (case1q1 & case1q2)
            filter2 = (case2q1 & case2q2)
            return queryset.filter(
                filter|filter2
            )

class TaxAlertAdmin(admin.ModelAdmin):
    date_hierarchy = 'raised_on'
admin.site.register(TaxAlert, TaxAlertAdmin)

class IncomeTaxMonthlyStatusAdmin(admin.ModelAdmin):
    list_filter = ['client', FinancialYearMonthlyListFilter]
    list_display = ['month_name', 'year', 'payment_status']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.order_by('year', 'month_name')
        return qs
admin.site.register(IncomeTaxMonthlyStatus, IncomeTaxMonthlyStatusAdmin)

class IncomeTaxQuarterlyStatusAdmin(admin.ModelAdmin):
    list_filter = ['client', FinancialYearQuarterlyListFilter]
    list_display = ['quarter', 'year', 'payment_status']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.order_by('year', 'quarter')
        return qs
admin.site.register(IncomeTaxQuarterlyStatus, IncomeTaxQuarterlyStatusAdmin)

class GSTMonthlyStatusAdmin(admin.ModelAdmin):
    list_filter = ['client', FinancialYearMonthlyListFilter]
    list_display = ['month_name', 'year', 'payment_status']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.order_by('year', 'month_name')
        return qs
admin.site.register(GSTMonthlyStatus, GSTMonthlyStatusAdmin)

class GSTQuarterlyStatusAdmin(admin.ModelAdmin):
    list_filter = ['client', FinancialYearQuarterlyListFilter]
    list_display = ['quarter', 'year', 'payment_status']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.order_by('year', 'quarter')
        return qs
admin.site.register(GSTQuarterlyStatus, GSTQuarterlyStatusAdmin)

class OtherTaxesMontlhyStatusAdmin(admin.ModelAdmin):
    list_filter = ['client', FinancialYearMonthlyListFilter]
    list_display = ['month_name', 'year', 'payment_status']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.order_by('year', 'month_name')
        return qs
admin.site.register(OtherTaxesMonthlyStatus, OtherTaxesMontlhyStatusAdmin)

class OtherTaxesQuarterlyStatusAdmin(admin.ModelAdmin):
    list_filter = ['client', FinancialYearQuarterlyListFilter]
    list_display = ['quarter', 'year', 'payment_status']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.order_by('year', 'quarter')
        return qs
admin.site.register(OtherTaxesQuarterlyStatus, OtherTaxesQuarterlyStatusAdmin)