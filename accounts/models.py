from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ZohoAccount(models.Model):
    account_for_coding_choice=[
        ('accounts_receivable','Accounts Receivable'),
        ('advertising_and_marketing_expenses','Advertising and Marketing Expenses'),
        ('bank_balance','Bank Balance'),
        ('bank_fees_and_charges','Bank fees & charges'),
        ('brokerage_and_commission_charges','Brokerage & Commission Charges'),
        ('cash_balance','Cash Balance'),
        ('cost_of_goods_sold','Cost of Goods Sold'),
        ('depreciation_expenses','Depreciation expenses'),
        ('direct_income','Direct Income'),
        ('director_remuneration','Director Remuneration'),
        ('duties_and_taxes','Duties & Taxes'),
        ('exchange_gain_or_loss','Exchange Gain or Loss'),
        ('indirect_income','Indirect Income'),
        ('intangible_assets','Intangible Assets'),
        ('interest_expenses','Interest Expenses'),
        ('inventories','Inventories'),
        ('it_and_internet_expenses','IT and Internet Expenses'),
        ('legal_and_professional_fees','Legal & Professional fees'),
        ('long_term_borrowings','Long Term Borrowings'),
        ('office_expenses','Office Expenses'),
        ('other_current_assets','Other Current Assets'),
        ('other_non_current_assets','Other Non Current Assets'),
        ('other_current_liabilities_and_provisions','Other Current Liabilities & Provisions'),
        ('other_employee_related_expenses','Other Employee related expenses'),
        ('other_expenses','Other Expenses'),
        ('other_liabilities','Other Liabilities'),
        ('rent_expenses','Rent Expenses'),
        ('repairs_and_maintenance_expenses','Repairs & Maintenance Expenses'),
        ('reserves_and_surplus','Reserves and Surplus'),
        ('salary_and_wages','Salary & Wages'),
        ('share_capital','Share Capital'),
        ('short_term_loans_and_advances','Short Term Loans & Advances'),
        ('short_term_borrowings','Short-term borrowings'),
        ('tangible_assets','Tangible Assets'),
        ('trade_payables','Trade Payables'),
        ('training_expenses','Training Expenses'),
        ('travel_and_hotel_stay_expenses','Travel & Hotel Stay Expenses'),
        ('uncategorized','Uncategorized'),
        ('utilities_expenses','Utilities Expenses')
    ]
    def __str__(self):
        return self.account_name

    client = models.ForeignKey(User, on_delete=models.CASCADE)
    account_id = models.CharField(max_length=30, primary_key=True)
    account_name = models.CharField(max_length=100)
    account_for_coding = models.CharField(max_length=50, choices=account_for_coding_choice, default='accounts_receivable')
    account_code = models.CharField(max_length=30, blank=True, null=True)
    account_type = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_user_created = models.BooleanField(blank=True, null=True)
    is_system_account = models.BooleanField(blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)
    can_show_in_ze = models.BooleanField(blank=True, null=True)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2)
    parent_account_id = models.CharField(max_length=100, blank=True, null=True)
    parent_account_name = models.CharField(max_length=100, blank=True, null=True)
    depth = models.IntegerField(blank=True, null=True)
    has_attachment = models.BooleanField(blank=True, null=True)
    is_child_present = models.BooleanField()
    child_count = models.CharField(max_length=3, blank=True, null=True)
    created_time = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    is_standalone_account = models.BooleanField(blank=True, null=True)
    last_modified_time = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)

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
