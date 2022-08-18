from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
gender_choice=[
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Others'),
    ('NA', 'Prefer not to say')
]
class Client(models.Model):
    def __str__(self):
        return self.client_name

    client_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    client_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(auto_now=False)
    gender = models.CharField(max_length=20, choices=gender_choice, default='NA')
    email_id = models.EmailField(max_length=254)
    contact_number = PhoneNumberField()
    zoho_organization_id = models.CharField(max_length=20, null=True)
    zoho_client_id = models.CharField(max_length=200, null=True)
    zoho_client_secret = models.CharField(max_length=200, null=True)
    zoho_redirect_uri = models.URLField(max_length=50, null=True)
    zoho_refresh_token = models.CharField(max_length=100, null=True)
    