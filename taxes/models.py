from django.db import models
from django.contrib.auth.models import User
import calendar

PENDING = 'pending'
ACTION_REQUIRED = 'action_required'
QUALITY_CHECK = 'quality_check'
DONE = 'done'
status_choices = [
    (PENDING, 'Pending'),
    (ACTION_REQUIRED, 'Client Action Required'),
    (QUALITY_CHECK, 'Quality Check'),
    (DONE, 'Completed')
]

month_choices = []
for i in range(1, 13):
    month_name = calendar.month_name[i]
    month_choices.append(
        (month_name.lower(), month_name[:3])
    )

quarter_choices = []
for i in range(1, 12, 3):
    quarter_name = (calendar.month_name[i], calendar.month_name[i+2])
    quarter_choices.append(
        (quarter_name[0].lower(), quarter_name[0][:3] + '-' + quarter_name[1][:3])
    )

# Create your models here.
class TaxAlert(models.Model):
    def __str__(self):
        return self.alert

    INCOME_TAX = 'income_tax'
    GST = 'gst'
    OTHER_TAXES = 'other_taxes'
    tax_type_choices = [
        (INCOME_TAX, 'Income Tax'),
        (GST, 'GST'),
        (OTHER_TAXES, 'Other Taxes')
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE)
    alert = models.CharField(max_length=500, blank=True)
    raisedOn = models.DateTimeField(auto_now_add=True)
    taxType = models.CharField(max_length=20, choices= tax_type_choices, default='Income Tax')
    dueDate = models.DateField()

class ITMonthlyStatus(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    monthName = models.CharField(max_length=20, choices= month_choices, default='Jan')
    paymentStatus = models.CharField(max_length=30, choices=status_choices, default='Pending')

class ITQuarterlyStatus(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    quarter = models.CharField(max_length=20, choices= quarter_choices, default='Jan-Mar')
    paymentStatus = models.CharField(max_length=30, choices=status_choices, default='Pending')

class GSTMonthlyStatus(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    monthName = models.CharField(max_length=20, choices= month_choices, default='Jan')
    paymentStatus = models.CharField(max_length=30, choices=status_choices, default='Pending')

class GSTQuarterlyStatus(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    quarter = models.CharField(max_length=20, choices= quarter_choices, default='Jan-Mar')
    paymentStatus = models.CharField(max_length=30, choices=status_choices, default='Pending')
