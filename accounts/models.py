from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ZohoAccount(models.Model):
    def __str__(self):
        return self.account_name

    client = models.ForeignKey(User, on_delete=models.CASCADE)
    account_id = models.CharField(max_length=30, primary_key=True)
    account_name = models.CharField(max_length=100)
    account_for_coding = models.CharField(max_length=50, blank=True)
    account_code = models.CharField(max_length=30)
    account_type = models.CharField(max_length=100)
    description = models.TextField()
    is_user_created = models.BooleanField()
    is_system_account = models.BooleanField()
    is_active = models.BooleanField()
    can_show_in_ze = models.BooleanField()
    current_balance = models.DecimalField(max_digits=10, decimal_places=2)
    parent_account_id = models.CharField(max_length=100)
    parent_account_name = models.CharField(max_length=100)
    depth = models.IntegerField()
    has_attachment = models.BooleanField()
    is_child_present = models.BooleanField()
    child_count = models.CharField(max_length=3)
    created_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    is_standalone_account = models.BooleanField()
    last_modified_time = models.DateTimeField(auto_now=False, auto_now_add=False)

class ZohoTransaction(models.Model):
    def __str__(self):
        return self.categorized_transaction_id

    categorized_transaction_id = models.CharField(max_length=30, primary_key=True)
    transaction_type = models.CharField(max_length=100, null=True)
    transaction_status = models.CharField(max_length=50, null=True)
    transaction_status_formatted = models.CharField(max_length=50, null=True)
    transaction_source = models.CharField(max_length=50, null=True)
    transaction_id = models.CharField(max_length=30)
    transaction_date = models.DateField(auto_now=False, auto_now_add=False)
    transaction_type_formatted = models.CharField(max_length=100)
    account = models.ForeignKey(ZohoAccount, on_delete=models.CASCADE)
    parent_account_id = models.CharField(max_length=30)
    customer_id = models.CharField(max_length=30)
    payee = models.CharField(max_length=100)
    description = models.TextField()
    entry_number = models.CharField(max_length=50)
    currency_id = models.CharField(max_length=30)
    currency_code = models.CharField(max_length=20)
    debit_or_credit = models.CharField(max_length=20)
    offset_account_name = models.CharField(max_length=100)
    reference_number = models.CharField(max_length=100)
    debit_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    credit_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fcy_debit_amount = models.CharField(max_length=20, null=True)
    fcy_credit_amount = models.CharField(max_length=20, null=True)
    reconcile_status = models.CharField(max_length=20, null=True)
