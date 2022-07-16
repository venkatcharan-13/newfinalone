from django.contrib import admin
from taxes.models import TaxAlert, ITMonthlyStatus, ITQuarterlyStatus, GSTMonthlyStatus, GSTQuarterlyStatus

# Register your models here.
admin.site.register(TaxAlert)
admin.site.register(ITMonthlyStatus)
admin.site.register(ITQuarterlyStatus)
admin.site.register(GSTMonthlyStatus)
admin.site.register(GSTQuarterlyStatus)