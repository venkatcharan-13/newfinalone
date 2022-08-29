from django.db import models
from authentication.models import Client

dashboard_acc_status_choices = [
    ('completed', 'Completed'),
    ('pending', 'Pending')
]

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
class GeneralNotification(models.Model):
    def __str__(self):
        return self.content

    content = models.TextField(max_length=100)
    created_on = models.DateField(auto_now_add=True)


class NextDeliveryDate(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    period = models.DateField(auto_now=False)
    delivery_date = models.DateField(auto_now=False)


class ContactPerson(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    person_name = models.CharField(max_length=50)
    profile = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=14)


class ClientNotification(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=100)
    link = models.URLField(blank=True, null=True)
    created_on = models.DateField(auto_now_add=True)


class DashboardAccountStatus(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    status_desc = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=dashboard_acc_status_choices, default='pending')
    period = models.DateField()
    modified_on = models.DateField(auto_now=True)


class PendingActionable(models.Model):
    def __str__(self):
        return self.point

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    created_on = models.DateField(auto_now_add=True)
    point = models.CharField(max_length=100)
    client_remarks = models.CharField(max_length=500, blank=True)
    status = models.BooleanField(default=False, blank=True)


class WatchOutPoint(models.Model):
    def __str__(self):
        return self.point

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    created_on = models.DateField(auto_now_add=True)
    point = models.CharField(max_length=100)


class StatutoryCompliance(models.Model):
    def __str__(self):
        return self.compliance

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    compliance_type = models.CharField(max_length=20, choices=statutory_compliance_choices, default='TDS')
    compliance = models.CharField(max_length=100)
    due_date = models.DateField(auto_now=False, auto_now_add=False)
