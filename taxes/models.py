from django.db import models

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

# Create your models here.
class TaxAlert(models.Model):
    INCOME_TAX = 'income_tax'
    GST = 'gst'
    OTHER_TAXES = 'other_taxes'
    tax_type_choices = [
        (INCOME_TAX, 'Income Tax'),
        (GST, 'GST'),
        (OTHER_TAXES, 'Other Taxes')
    ]
    alert = models.CharField(max_length=500, blank=True)
    raisedOn = models.DateTimeField(auto_now_add=True)
    taxType = models.CharField(max_length=20, choices= tax_type_choices, default='Income Tax')
    dueDate = models.DateField()

class ITMonthlyStatus(models.Model):
    monthName = models.CharField(max_length=20)
    paymentStatus = models.CharField(max_length=30, choices=status_choices, default='Pending')

class ITQuarterlyStatus(models.Model):
    quarter = models.CharField(max_length=20)
    paymentStatus = models.CharField(max_length=30, choices=status_choices, default='Pending')

class GSTMonthlyStatus(models.Model):
    monthName = models.CharField(max_length=20)
    paymentStatus = models.CharField(max_length=30, choices=status_choices, default='Pending')

class GSTQuarterlyStatus(models.Model):
    quarter = models.CharField(max_length=20)
    paymentStatus = models.CharField(max_length=30, choices=status_choices, default='Pending')
