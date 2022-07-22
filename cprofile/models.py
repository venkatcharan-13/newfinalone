from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User

# Create your models here.

class Company(models.Model):
    def __str__(self):
        return self.company_name

    client = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    entity_name = models.CharField(max_length=100)
    industry_name = models.CharField(max_length=100)
    contact_number = PhoneNumberField()
    company_email = models.CharField(max_length=30, null=True)
    gst_number = models.CharField(max_length=20)
    pan_number = models.CharField(max_length=20)
    pf_number = models.CharField(max_length=20, null=True)
    esic_number = models.CharField(max_length=20, null=True)


class CompanyAddress(models.Model):
    def __str__(self):
        return self.company.company_name

    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    address_line = models.TextField()
    locality = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    pin_code = models.CharField(max_length=6)


class CompanyContext(models.Model):
    def __str__(self):
        return self.company.company_name

    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    about = models.TextField(blank=True, null=True)
    work_profile = models.TextField(blank=True, null=True)
    key_info = models.TextField(blank=True, null=True)
    specific_request = models.TextField(blank=True, null=True)


class BankDetail(models.Model):
    def __str__(self):
        return self.bank_name

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=50)
    account_number = models.CharField(max_length=15)
    ifsc_code = models.CharField(max_length=15)
    location = models.CharField(max_length=50)
