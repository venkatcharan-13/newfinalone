from django.db import models
from django.contrib.auth.models import User


statutory_compliance_choices = [
    ('tds', 'TDS'),
    ('gst', 'GST')
]

statutory_comp_status_choices = [
    ('not_started', 'Not Started'),
    ('ongoing', 'Ongoing'),
    ('not_applicable', 'Not Applicable'),
    ('completed', 'Completed')
]

# Create your models here.
class PendingActionable(models.Model):
    def __str__(self):
        return self.point

    client = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateField(auto_now_add=True)
    point = models.CharField(max_length=100)
    client_remarks = models.CharField(max_length=500, blank=True)
    status = models.BooleanField(default=False, blank=True)
    # attached_doc = models.FileField()

class WatchOutPoint(models.Model):
    def __str__(self):
        return self.point
        
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateField(auto_now_add=True)
    point = models.CharField(max_length=100)

class StatutoryCompliance(models.Model):
    def __str__(self):
        return self.compliance
    
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    compliance_type= models.CharField(max_length=20, choices=statutory_compliance_choices, default='TDS')
    compliance = models.CharField(max_length=100)
    current_month_due_date = models.DateField(auto_now=False, auto_now_add=False)
    current_month_status = models.CharField(max_length=20, choices=statutory_comp_status_choices, default='Not Started')
    last_month_status = models.CharField(max_length=20, choices=statutory_comp_status_choices, default='Not Started')
    last_month_completion_date = models.DateField(auto_now=False, auto_now_add=False)