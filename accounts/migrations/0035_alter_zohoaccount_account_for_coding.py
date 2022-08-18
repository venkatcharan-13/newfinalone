# Generated by Django 4.0.5 on 2022-08-18 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0034_alter_zohotransaction_currency_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zohoaccount',
            name='account_for_coding',
            field=models.CharField(choices=[('accounts_receivable', 'Accounts Receivable'), ('advertising_and_marketing_expenses', 'Advertising and Marketing Expenses'), ('bank_balance', 'Bank Balance'), ('bank_fees_and_charges', 'Bank fees & charges'), ('brokerage_and_commission_charges', 'Brokerage & Commission Charges'), ('cash_balance', 'Cash Balance'), ('cost_of_goods_sold', 'Cost of Goods Sold'), ('depreciation_expenses', 'Depreciation Expenses'), ('direct_income', 'Direct Income'), ('director_remuneration', 'Director Remuneration'), ('duties_and_taxes', 'Duties & Taxes'), ('exchange_gain_or_loss', 'Exchange Gain or Loss'), ('indirect_income', 'Indirect Income'), ('intangible_assets', 'Intangible Assets'), ('interest_expenses', 'Interest Expenses'), ('inventories', 'Inventories'), ('it_and_internet_expenses', 'IT and Internet Expenses'), ('legal_and_professional_fees', 'Legal & Professional fees'), ('long_term_borrowings', 'Long Term Borrowings'), ('long_term_loans', 'Long Term Loans'), ('office_expenses', 'Office Expenses'), ('other_current_assets', 'Other Current Assets'), ('other_non_current_assets', 'Other Non Current Assets'), ('other_current_liabilities_and_provisions', 'Other Current Liabilities & Provisions'), ('other_employee_related_expenses', 'Other Employee related expenses'), ('other_expenses', 'Other Expenses'), ('other_liabilities', 'Other Liabilities'), ('other_long_term_liabilities_and_provisions', 'Other long term Liabilities and Provisions'), ('rent_expenses', 'Rent Expenses'), ('repairs_and_maintenance_expenses', 'Repairs & Maintenance Expenses'), ('reserves_and_surplus', 'Reserves and Surplus'), ('salary_and_wages', 'Salary & Wages'), ('share_capital', 'Share Capital'), ('short_term_loans_and_advances', 'Short Term Loans & Advances'), ('short_term_borrowings', 'Short-term borrowings'), ('tangible_assets', 'Tangible Assets'), ('tax_expenses', 'Taxes'), ('trade_payables', 'Trade Payables'), ('training_expenses', 'Training Expenses'), ('travel_and_hotel_stay_expenses', 'Travel & Hotel Stay Expenses'), ('uncategorized', 'Uncategorized'), ('utilities_expenses', 'Utilities Expenses')], default='accounts_receivable', max_length=50),
        ),
    ]
