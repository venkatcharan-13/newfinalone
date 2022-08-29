from django.db import models
from authentication.models import Client
import calendar

PENDING = 'pending'
ACTION_REQUIRED = 'action_required'
NOT_APPLICABLE = 'not_applicable'
DONE = 'done'
status_choices = [
    (PENDING, 'Pending'),
    (ACTION_REQUIRED, 'Client Action Required'),
    (NOT_APPLICABLE, 'Not Applicable'),
    (DONE, 'Done')
]

month_choices = []
for i in range(1, 13):
    month_name = calendar.month_name[i]
    month_choices.append(
        (i, month_name[:3])
    )

year_choices = []
for i in range(2015, 2025):
    year_choices.append(
        (i, i)
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
    OTHER_COMPLIANCES = 'other_compliances'
    tax_type_choices = [
        (INCOME_TAX, 'Income Tax'),
        (GST, 'GST'),
        (OTHER_COMPLIANCES, 'Other Compliances')
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    alert = models.CharField(max_length=500, blank=True)
    raised_on = models.DateField(auto_now_add=True)
    tax_type = models.CharField(max_length=20, choices= tax_type_choices, default='income_tax')
    due_date = models.DateField()

class IncomeTaxMonthlyStatus(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    month_name = models.IntegerField(choices= month_choices, default=4)
    year = models.IntegerField(choices=year_choices, default=2022)
    payment_status = models.CharField(max_length=30, choices=status_choices, default='not_applicable')

    @property
    def fin_year(self):
        if int(self.month_name) > 3:
            return self.year
        else:
            return self.year - 1

class IncomeTaxQuarterlyStatus(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    quarter = models.CharField(max_length=20, choices= quarter_choices, default='Apr-Jun')
    year = models.IntegerField(choices=year_choices, default=2022)
    payment_status = models.CharField(max_length=30, choices=status_choices, default='not_applicable')

    @property
    def fin_year(self):
        if self.quarter in ('Q1', 'Q2', 'Q3'):
            return self.year
        else:
            return self.year - 1

class IncomeTaxAdvanceStatus(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    quarter = models.CharField(max_length=20, choices= quarter_choices, default='Apr-Jun')
    year = models.IntegerField(choices=year_choices, default=2022)
    payment_status = models.CharField(max_length=30, choices=status_choices, default='not_applicable')

    @property
    def fin_year(self):
        if self.quarter in ('Q1', 'Q2', 'Q3'):
            return self.year
        else:
            return self.year - 1

class GSTR1MonthlyStatus(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    month_name = models.IntegerField(choices= month_choices, default=4)
    year = models.IntegerField(choices=year_choices, default=2022)
    payment_status = models.CharField(max_length=30, choices=status_choices, default='not_applicable')

    @property
    def fin_year(self):
        if int(self.month_name) > 3:
            return self.year
        else:
            return self.year - 1

class GSTR3BMonthlyStatus(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    month_name = models.IntegerField(choices= month_choices, default=4)
    year = models.IntegerField(choices=year_choices, default=2022)
    payment_status = models.CharField(max_length=30, choices=status_choices, default='not_applicable')

    @property
    def fin_year(self):
        if int(self.month_name) > 3:
            return self.year
        else:
            return self.year - 1

class GSTR8MonthlyStatus(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    month_name = models.IntegerField(choices= month_choices, default=4)
    year = models.IntegerField(choices=year_choices, default=2022)
    payment_status = models.CharField(max_length=30, choices=status_choices, default='not_applicable')

    @property
    def fin_year(self):
        if int(self.month_name) > 3:
            return self.year
        else:
            return self.year - 1

class ProvidentFundMonthlyStatus(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    month_name = models.IntegerField(choices= month_choices, default=4)
    year = models.IntegerField(choices=year_choices, default=2022)
    payment_status = models.CharField(max_length=30, choices=status_choices, default='not_applicable')

    @property
    def fin_year(self):
        if int(self.month_name) > 3:
            return self.year
        else:
            return self.year - 1

class ESICMonthlyStatus(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    month_name = models.IntegerField(choices= month_choices, default=4)
    year = models.IntegerField(choices=year_choices, default=2022)
    payment_status = models.CharField(max_length=30, choices=status_choices, default='not_applicable')

    @property
    def fin_year(self):
        if int(self.month_name) > 3:
            return self.year
        else:
            return self.year - 1
