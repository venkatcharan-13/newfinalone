from django.db import models

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
    taxType = models.CharField(max_length=20, choices= tax_type_choices, default='Income Tax'
    )
    dueDate = models.DateField()
