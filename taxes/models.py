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
        (str(i), month_name[:3])
    )

year_choices = []
for i in range(2015, 2025):
    year_choices.append(
        (str(i), str(i))
    )

quarter_choices = [
    ('Q1', 'Apr-Jun'),
    ('Q2', 'Jul-Sep'),
    ('Q3', 'Oct-Dec'),
    ('Q4', 'Jan-Mar')
]

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
    raised_on = models.DateTimeField(auto_now_add=True)
    tax_type = models.CharField(max_length=20, choices= tax_type_choices, default='Income Tax')
    due_date = models.DateField()

class ITMonthlyStatus(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    month_name = models.CharField(max_length=20, choices= month_choices, default='Jan')
    year = models.CharField(max_length=4, choices=year_choices)
    payment_status = models.CharField(max_length=30, choices=status_choices, default='Pending')

class ITQuarterlyStatus(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    quarter = models.CharField(max_length=20, choices= quarter_choices, default='Apr-Jun')
    year = models.CharField(max_length=4, choices=year_choices)
    payment_status = models.CharField(max_length=30, choices=status_choices, default='Pending')

class GSTMonthlyStatus(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    month_name = models.CharField(max_length=20, choices= month_choices, default='Jan')
    year = models.CharField(max_length=4, choices=year_choices)
    payment_status = models.CharField(max_length=30, choices=status_choices, default='Pending')

class GSTQuarterlyStatus(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    quarter = models.CharField(max_length=20, choices= quarter_choices, default='Apr-Jun')
    year = models.CharField(max_length=4, choices=year_choices)
    payment_status = models.CharField(max_length=30, choices=status_choices, default='Pending')
