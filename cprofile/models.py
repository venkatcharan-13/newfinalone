from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from authentication.models import Client

# Create your models here.
industry_choice=[
    ('agency_sales_housing', 'Agency & Sales Housing'),
    ('art_and_design', 'Art & Design'),
    ('automation', 'Automation'),
    ('construction', 'Construction'),
    ('consulting', 'Consulting'),
    ('consumer_packaged_goods', 'Consumer Packaged Goods'),
    ('education', 'Education'),
    ('engineering', 'Engineering'),
    ('entertainment', 'Entertainment'),
    ('financial_services', 'Financial Services'),
    ('food_services', 'Food Services (Restaurants/Fast Food)'),
    ('gaming', 'Gaming'),
    ('government', 'Government'),
    ('healthcare', 'Health Care'),
    ('interior_design', 'Interior Design'),
    ('legal', 'Legal'),
    ('manufacturing', 'Manufacturing'),
    ('marketing', 'Marketing'),
    ('mining_and_logistics', 'Mining and Logistics'),
    ('non_profit', 'Non-Profit'),
    ('publishing_and_media', 'Publishing and Web Media'),
    ('real_estate', 'Real Estate'),
    ('retail', 'Retail (E-Commerce and Retails)'),
    ('services', 'Services'),
    ('technology', 'Technology'),
    ('telecommunications', 'Telecommunications'),
    ('travel_hospitality', 'Travel/Hospitality')
]

state_choice=[
    ('maharashtra', 'Maharashtra '),
    ('andhra_pradesh', 'Andhra Pradesh'),
    ('arunachal_pradesh', 'Arunachal Pradesh'),
    ('assam', 'Assam'),
    ('bihar', 'Bihar'),
    ('chhattisgarh', 'Chhattisgarh'),
    ('goa', 'Goa'),
    ('delhi', 'Delhi'),
    ('gujarat', 'Gujarat'),
    ('haryana', 'Haryana'),
    ('himachal_pradesh', 'Himachal Pradesh'),
    ('jammu_and_kashmir', 'Jammu and Kashmir'),
    ('jharkhand', 'Jharkhand'),
    ('karnataka', 'Karnataka'),
    ('kerala', 'Kerala'),
    ('madhya_pradesh', 'Madhya Pradesh'),
    ('manipur', 'Manipur'),
    ('meghalaya', 'Meghalaya'),
    ('mizoram', 'Mizoram'),
    ('nagaland', 'Nagaland'),
    ('odisha', 'Odisha'),
    ('punjab', 'Punjab'),
    ('rajasthan', 'Rajasthan'),
    ('sikkim', 'Sikkim'),
    ('tamil_nadu', 'Tamil Nadu'),
    ('telangana', 'Telangana'),
    ('tripura', 'Tripura'),
    ('uttar_pradesh', 'Uttar Pradesh'),
    ('uttarakhand', 'Uttarakhand'),
    ('west_bengal', 'West Bengal')
]


class Company(models.Model):
    def __str__(self):
        return self.company_name

    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    entity_name = models.CharField(max_length=100)
    industry_name = models.CharField(max_length=100, choices=industry_choice)
    contact_person = models.CharField(max_length=100)
    contact_number = PhoneNumberField()
    company_email = models.EmailField(max_length=50, null=True)
    gst_number = models.CharField(max_length=20, null=True, blank=True)
    pan_number = models.CharField(max_length=20, null=True, blank=True)
    pf_number = models.CharField(max_length=20, null=True, blank=True)
    esic_number = models.CharField(max_length=20, null=True, blank=True)


class CompanyAddress(models.Model):
    def __str__(self):
        return self.company.company_name

    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    address_line = models.TextField()
    locality = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30, choices=state_choice)
    country = models.CharField(max_length=30, default='India')
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
