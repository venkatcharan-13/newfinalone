from accounts.models import ZohoAccount, ZohoTransaction
from django.db.models import Q
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import calendar
import locale

locale.setlocale(locale.LC_ALL, 'en_IN.utf8')

def get_sales_performance(current_date):
    if current_date is None:
        current_date = date(2022, 6, 30)
    elif not isinstance(current_date, date):
        current_date = datetime.strptime(current_date, '%Y-%m-%d').date()

    accounts_related_to_income = list(ZohoAccount.objects.filter(
        account_type='income'
    ).values_list('account_id'))

    account_ids_for_income = []
    for acc in accounts_related_to_income:
        account_ids_for_income.append(acc[0])

    transactions_related_to_income = ZohoTransaction.objects.filter(
        account_id__in=account_ids_for_income
    )

    monthly_sale = {}

    prev_six_months = [current_date]
    temp = current_date
    for i in range(5):
        last_date_of_previous_month = temp.replace(
            day=1) + relativedelta(days=-1)
        prev_six_months.append(last_date_of_previous_month)
        temp = last_date_of_previous_month
    prev_six_months.sort()

    for period in prev_six_months:
        month = period.month
        year = period.year
        month_name = calendar.month_name[month]
        monthly_sale[month_name] = 0
        for transaction in transactions_related_to_income:
            trans_date = transaction.transaction_date
            if (trans_date.month, trans_date.year) == (month, year):
                monthly_sale[month_name] += (
                    transaction.credit_amount - transaction.debit_amount)
        monthly_sale[month_name] = round(monthly_sale[month_name])

    quarterly_sale = {
        'Jan-Mar': 0,
        'Apr-Jun': 0,
        'Jul-Sep': 0,
        'Oct-Dec': 0
    }

    # THIS PART HAS BEEN HARD CODED, WILL BE CHANGED LATER

    for transaction in transactions_related_to_income:
        trans_date = transaction.transaction_date
        if trans_date <= date(2022, 6, 30) and trans_date >= date(2022, 4, 1):
            quarterly_sale["Apr-Jun"] += (
                transaction.credit_amount - transaction.debit_amount)
    quarterly_sale["Apr-Jun"] = round(quarterly_sale["Apr-Jun"])

    for transaction in transactions_related_to_income:
        trans_date = transaction.transaction_date
        if trans_date <= date(2022, 3, 31) and trans_date >= date(2022, 1, 1):
            quarterly_sale["Jan-Mar"] += (
                transaction.credit_amount - transaction.debit_amount)
    quarterly_sale["Jan-Mar"] = round(quarterly_sale["Jan-Mar"])

    for transaction in transactions_related_to_income:
        trans_date = transaction.transaction_date
        if trans_date <= date(2021, 12, 31) and trans_date >= date(2021, 10, 1):
            quarterly_sale["Oct-Dec"] += (
                transaction.credit_amount - transaction.debit_amount)
    quarterly_sale["Oct-Dec"] = round(quarterly_sale["Oct-Dec"])

    for transaction in transactions_related_to_income:
        trans_date = transaction.transaction_date
        if trans_date <= date(2021, 9, 30) and trans_date >= date(2021, 7, 1):
            quarterly_sale["Jul-Sep"] += (
                transaction.credit_amount - transaction.debit_amount)
    quarterly_sale["Jul-Sep"] = round(quarterly_sale["Jul-Sep"])

    yearly_sale = {}

    for year in (2019, 2020, 2021, 2022):
        yearly_sale[year] = 0
        for transaction in transactions_related_to_income:
            if transaction.transaction_date.year == year:
                yearly_sale[year] += (transaction.credit_amount -
                                      transaction.debit_amount)
        yearly_sale[year] = round(yearly_sale[year])

    return (monthly_sale, quarterly_sale, yearly_sale)


def get_income_vs_expenses(current_date):
    if current_date is None:
        current_date = date(2022, 6, 30)
    elif not isinstance(current_date, date):
        current_date = datetime.strptime(current_date, '%Y-%m-%d').date()

    accounts_related_to_income_expenses = ZohoAccount.objects.filter(
        account_type__in=('income', 'expense', 'other_expense')
    ).values_list('account_id', 'account_type')

    transactions_related_to_income_expenses = ZohoTransaction.objects.filter(
        account_id__in=(tup[0] for tup in accounts_related_to_income_expenses)
    )
    accounts_dic = {'income': [], 'expense': [], 'other_expense': []}
    for tup in accounts_related_to_income_expenses:
        accounts_dic[tup[1]].append(tup[0])

    prev_six_months = [current_date]
    for i in range(5):
        last_date_of_previous_month = current_date.replace(
            day=1) + relativedelta(days=-1)
        prev_six_months.append(last_date_of_previous_month)
        current_date = last_date_of_previous_month

    tot_income_vs_tot_expenses = {}

    for i in range(5, -1, -1):
        month = prev_six_months[i].month
        year = prev_six_months[i].year
        month_name = calendar.month_name[month][:3] + '-' + str(year)[2:]
        tot_income_vs_tot_expenses[month_name] = {'income': 0, 'expenses': 0}
        for transaction in transactions_related_to_income_expenses:
            trans_date = transaction.transaction_date
            credit_minus_debit =  transaction.credit_amount - transaction.debit_amount
            if transaction.account_id in accounts_dic['income'] and trans_date.month == month and trans_date.year == year:
                tot_income_vs_tot_expenses[month_name]['income'] += credit_minus_debit

            if (transaction.account_id in accounts_dic['expense'] or transaction.account_id in accounts_dic['other_expense']) and trans_date.month == month and trans_date.year == year:
                tot_income_vs_tot_expenses[month_name]['expenses'] += credit_minus_debit

        tot_income_vs_tot_expenses[month_name]['income'] = round(
            tot_income_vs_tot_expenses[month_name]['income'])
        tot_income_vs_tot_expenses[month_name]['expenses'] = round(
            tot_income_vs_tot_expenses[month_name]['expenses'])

    return tot_income_vs_tot_expenses


def get_cash_inflow_outflow(current_date):
    if current_date is None:
        current_date = date(2022, 6, 30)
    elif not isinstance(current_date, date):
        current_date = datetime.strptime(current_date, '%Y-%m-%d').date()

    accounts_related_to_bank = ZohoAccount.objects.filter(
        account_for_coding='Bank Balance'
    ).values_list('account_id')

    transactions_related_to_bank = ZohoTransaction.objects.filter(
        account_id__in=(tup[0] for tup in accounts_related_to_bank)
    )

    prev_six_months = [current_date]
    for i in range(5):
        last_date_of_previous_month = current_date.replace(
            day=1) + relativedelta(days=-1)
        prev_six_months.append(last_date_of_previous_month)
        current_date = last_date_of_previous_month

    cash_inflow_vs_outflow = {}

    for i in range(5, -1, -1):
        month = prev_six_months[i].month
        year = prev_six_months[i].year
        month_name = calendar.month_name[month][:3] + '-' + str(year)[2:]
        cash_inflow_vs_outflow[month_name] = {'credit': 0, 'debit': 0}
        for transaction in transactions_related_to_bank:
            trans_date = transaction.transaction_date
            if trans_date.month == month and trans_date.year == year:
                cash_inflow_vs_outflow[month_name]['credit'] += transaction.credit_amount
                cash_inflow_vs_outflow[month_name]['debit'] += transaction.debit_amount

        cash_inflow_vs_outflow[month_name]['credit'] = round(
            cash_inflow_vs_outflow[month_name]['credit'])
        cash_inflow_vs_outflow[month_name]['debit'] = - \
            round(cash_inflow_vs_outflow[month_name]['debit'])

    return cash_inflow_vs_outflow


def get_closing_bank_balance_trend(current_date):
    if current_date is None:
        current_date = date(2022, 6, 30)
    elif not isinstance(current_date, date):
        current_date = datetime.strptime(current_date, '%Y-%m-%d').date()

    accounts_related_to_bank = ZohoAccount.objects.filter(
        account_for_coding='Bank Balance'
    ).values_list('account_id')

    transactions_related_to_bank = ZohoTransaction.objects.filter(
        account_id__in=(tup[0] for tup in accounts_related_to_bank)
    )

    prev_six_months = [current_date]
    for i in range(5):
        last_date_of_previous_month = current_date.replace(
            day=1) + relativedelta(days=-1)
        prev_six_months.append(last_date_of_previous_month)
        current_date = last_date_of_previous_month

    closing_bank_balance_trend = {}

    for i in range(5, -1, -1):
        month = prev_six_months[i].month
        year = prev_six_months[i].year
        month_name = calendar.month_name[month][:3] + '-' + str(year)[2:]
        closing_bank_balance_trend[month_name] = 0
        for transaction in transactions_related_to_bank:
            if transaction.transaction_date <= prev_six_months[i]:
                closing_bank_balance_trend[month_name] += (
                    transaction.debit_amount - transaction.credit_amount)

        closing_bank_balance_trend[month_name] = round(
            closing_bank_balance_trend[month_name])

    return closing_bank_balance_trend


def get_gross_profit_and_net_profit(current_date):
    if current_date is None:
        current_date = date(2022, 6, 30)
    elif not isinstance(current_date, date):
        current_date = datetime.strptime(current_date, '%Y-%m-%d').date()

    accounts_related_to_profit = ZohoAccount.objects.filter(
        account_type__in=['income', 'expense',
                          'other_expense', 'cost_of_goods_sold']
    ).values_list('account_id', 'account_type', 'account_for_coding')

    accounts_map = {}
    for account in accounts_related_to_profit:
        key = (account[1])
        if key not in accounts_map:
            accounts_map[key] = {}
        if account[2] not in accounts_map[key]:
            accounts_map[key][account[2]] = []
        accounts_map[key][account[2]].append(account[0])
    
    transactions_related_to_profit = ZohoTransaction.objects.filter(
        account_id__in=(tup[0] for tup in accounts_related_to_profit)
    )

    prev_six_months = [current_date]
    for i in range(5):
        last_date_of_previous_month = current_date.replace(
            day=1) + relativedelta(days=-1)
        prev_six_months.append(last_date_of_previous_month)
        current_date = last_date_of_previous_month

    gross_profit_and_net_profit = {}
    income_accounts = accounts_map['income']['Direct Income'] + \
        accounts_map['income']['Indirect Income']
    direct_income_accounts = accounts_map['income']['Direct Income']
    cogs_accounts = accounts_map['cost_of_goods_sold']['Cost of Goods Sold']
    expenses_accounts = []
    for account in accounts_map['expense']:
        expenses_accounts.extend(accounts_map['expense'][account])
    for account in accounts_map['other_expense']:
        expenses_accounts.extend(accounts_map['other_expense'][account])

    for i in range(5, -1, -1):
        month = prev_six_months[i].month
        year = prev_six_months[i].year
        month_name = calendar.month_name[month][:3] + '-' + str(year)[2:]
        gross_profit_and_net_profit[month_name] = {
            'gross_profit_per': 0, 'net_profit_per': 0}
        tot_income, direct_income, expenses, cogs = 0, 0, 0, 0
        for transaction in transactions_related_to_profit:
            trans_date = transaction.transaction_date
            credit_minus_debit = transaction.credit_amount - transaction.debit_amount
            debit_minus_credit = transaction.debit_amount - transaction.credit_amount
            if trans_date.month == month and trans_date.year == year:
                if transaction.account_id in income_accounts:
                    tot_income += credit_minus_debit
                if transaction.account_id in direct_income_accounts:
                    direct_income += credit_minus_debit
                if transaction.account_id in expenses_accounts:
                    expenses += debit_minus_credit
                if transaction.account_id in cogs_accounts:
                    cogs += debit_minus_credit
        gross_profit = tot_income - cogs
        pbt = gross_profit - expenses
        gross_profit_and_net_profit[month_name]['gross_profit_per'] = round(
            0 if direct_income == 0 else (gross_profit/direct_income)*100)
        gross_profit_and_net_profit[month_name]['net_profit_per'] = round(
            0 if direct_income == 0 else (pbt/direct_income)*100)

    return gross_profit_and_net_profit


def get_monthly_runaway(current_date):
    if current_date is None:
        current_date = date(2022, 6, 30)
    elif not isinstance(current_date, date):
        current_date = datetime.strptime(current_date, '%Y-%m-%d').date()

    accounts_related_to_balance = ZohoAccount.objects.filter(
        account_for_coding__in=('Bank Balance', 'Cash Balance')
    ).values_list('account_id')

    transactions_related_to_balance = ZohoTransaction.objects.filter(
        account_id__in=(tup[0] for tup in accounts_related_to_balance)
    )

    prev_seven_months = [current_date]
    for i in range(6):
        last_date_of_previous_month = current_date.replace(
            day=1) + relativedelta(days=-1)
        prev_seven_months.append(last_date_of_previous_month)
        current_date = last_date_of_previous_month

    monthly_runway = {}

    for i in range(5, -1, -1):
        month = prev_seven_months[i].month
        year = prev_seven_months[i].year
        month_name = calendar.month_name[month][:3] + '-' + str(year)[2:]
        monthly_runway[month_name] = 0
        curr, prev = 0, 0
        for transaction in transactions_related_to_balance:
            trans_date = transaction.transaction_date
            debit_minus_credit = (transaction.debit_amount - transaction.credit_amount)
            if trans_date <= prev_seven_months[i]:
                curr += debit_minus_credit
            if trans_date <= prev_seven_months[i+1]:
                prev += debit_minus_credit
        monthly_runway[month_name] = round(0 if curr-prev == 0 else curr/(curr-prev))

    return monthly_runway


def get_gp_vs_expenses_ebitda(current_date):
    if current_date is None:
        current_date = date(2022, 6, 30)
    elif not isinstance(current_date, date):
        current_date = datetime.strptime(current_date, '%Y-%m-%d').date()

    accounts_related_to_income = ZohoAccount.objects.filter(
        account_type = 'income'
    ).values_list('account_id')

    accounts_related_to_direct_income = ZohoAccount.objects.filter(
        account_for_coding = 'Direct Income'
    ).values_list('account_id')

    accounts_related_to_cogs = ZohoAccount.objects.filter(
        account_type = 'cogs'
    ).values_list('account_id')

    filter1 = Q(account_type__in = ('expense', 'other_expense'))
    filter2 = ~Q(account_for_coding__in = ('Depreciation expenses', 'Interest Expenses'))
    accounts_related_to_expenses = ZohoAccount.objects.filter(
        filter1, filter2
    ).values_list('account_id')

    transactions_related_to_income = ZohoTransaction.objects.filter(
        account_id__in = (tup[0] for tup in accounts_related_to_income)
    )

    transactions_related_to_direct_income = ZohoTransaction.objects.filter(
        account_id__in = (tup[0] for tup in accounts_related_to_direct_income)
    )

    transactions_related_to_cogs = ZohoTransaction.objects.filter(
        account_id__in = (tup[0] for tup in accounts_related_to_cogs)
    )

    transactions_related_to_expenses = ZohoTransaction.objects.filter(
        account_id__in = (tup[0] for tup in accounts_related_to_expenses)
    )
    
    prev_six_months = [current_date]
    for i in range(5):
        last_date_of_previous_month = current_date.replace(
            day=1) + relativedelta(days=-1)
        prev_six_months.append(last_date_of_previous_month)
        current_date = last_date_of_previous_month

    gp_vs_expenses_ebitda = {}
    for i in range(5, -1, -1):
        month = prev_six_months[i].month
        year = prev_six_months[i].year
        month_name = calendar.month_name[month][:3] + '-' + str(year)[2:]
        gp_vs_expenses_ebitda[month_name] = {
            'gross_profit': 0, 'expenses': 0, 'ebitda': 0
        }
        income, direct_income, cogs, expenses = 0, 0, 0, 0
        for transaction in transactions_related_to_income:
            trans_date = transaction.transaction_date
            if trans_date.month == month and trans_date.year == year:
                income += (transaction.credit_amount - transaction.debit_amount)
        for transaction in transactions_related_to_direct_income:
            trans_date = transaction.transaction_date
            if trans_date.month == month and trans_date.year == year:
                direct_income += (transaction.credit_amount - transaction.debit_amount)
        for transaction in transactions_related_to_cogs:
            trans_date = transaction.transaction_date
            if trans_date.month == month and trans_date.year == year:
                cogs += (transaction.debit_amount - transaction.credit_amount)
        for transaction in transactions_related_to_expenses:
            trans_date = transaction.transaction_date
            if trans_date.month == month and trans_date.year == year:
                expenses += (transaction.debit_amount - transaction.credit_amount)
        
        pbt = income - cogs - expenses
        gp_vs_expenses_ebitda[month_name]['gross_profit'] = round(income-cogs)
        gp_vs_expenses_ebitda[month_name]['expenses'] = round(expenses)
        gp_vs_expenses_ebitda[month_name]['ebitda'] = 0 if direct_income == 0 else round(pbt/direct_income * 100)
        
    return gp_vs_expenses_ebitda


def get_monthly_cashflow_statement(current_date):
    if current_date is None:
        current_date = date(2022, 6, 30)
    elif not isinstance(current_date, date):
        current_date = datetime.strptime(current_date, '%Y-%m-%d').date()

    cashflow_accounts = (
        'Bank Balance',
        'Cash Balance',
        'Accounts Receivable',
        'Other Current Assets',
        'Other Non Current Assets',
        'Trade Payables',
        'Other long term Liabilities & Provisions',
        'Other Liabilities',
        'Other Current Liabilities & Provisions',
        'Tangible Assets',
        'Short Term Loans & Advances',
        'Long Term Loans & Advances',
        'Short-term borrowings',
        'Long Term Borrowing',
        'Share Capital'
    )

    # Fetching data related to cashflow accounts
    cashflow_accounts_data = ZohoAccount.objects.filter(
        account_for_coding__in = cashflow_accounts
    ).values_list('account_id', 'account_for_coding', 'account_type')

    cashflow_transactions_data = ZohoTransaction.objects.filter(
        account_id__in = (tup[0] for tup in cashflow_accounts_data)
    )

    accounts_related_to_pbt = ZohoAccount.objects.filter(
        account_type__in = ('income', 'expense', 'other_expense', 'cost_of_goods_sold')
    ).values_list('account_id', 'account_type')

    accounts_map = dict(accounts_related_to_pbt)
    
    transactions_related_to_pbt = ZohoTransaction.objects.filter(
        account_id__in = accounts_map
    )
    
    prev_six_months = [current_date]
    temp_date = current_date
    for i in range(5):
        last_date_of_previous_month = temp_date.replace(
            day=1) + relativedelta(days=-1)
        prev_six_months.append(last_date_of_previous_month)
        temp_date = last_date_of_previous_month

    pbt_lst = []
    for i in range(5, -1, -1):
        month = prev_six_months[i].month
        year = prev_six_months[i].year
        income, cogs, expenses = 0, 0, 0,
        for transaction in transactions_related_to_pbt:
            trans_date = transaction.transaction_date
            credit_minus_debit = (transaction.credit_amount - transaction.debit_amount)
            debit_mius_credit = (transaction.debit_amount - transaction.credit_amount)
            if trans_date.month == month and trans_date.year == year:
                if accounts_map[transaction.account_id] == 'income':
                    income += credit_minus_debit
                if accounts_map[transaction.account_id] == 'cost_of_goods_sold':
                    cogs += debit_mius_credit
                if accounts_map[transaction.account_id] in ('expense', 'other_expense'):
                    expenses += debit_mius_credit
        pbt_lst.append(round(income-cogs-expenses))
 
    # Defining structure for API response
    cashflow_data = {
        'cashflow_from_operating_activities': [],
        'net_cash_a': [],
        'cashflow_from_investing_activities': [],
        'net_cash_b': [],
        'cashflow_from_financing_activities': [],
        'net_cash_c': [],
    }

    accounts_map, transactions_map = {}, {}
    cashflow_data_uncategorized = {}  # To store data related to all cashflow accounts

    for account in cashflow_accounts:
        cashflow_data_uncategorized[account] = []

    for account in cashflow_accounts_data:
        accounts_map[account[0]] = (account[1], account[2])

    for transaction in cashflow_transactions_data:
        if transaction.account_id in accounts_map:
            acccount_header = accounts_map[transaction.account_id]
            if acccount_header not in transactions_map:
                transactions_map[acccount_header] = []
            transactions_map[acccount_header].append(transaction)

    prev_seven_months = [current_date]
    for i in range(6):
        last_date_of_previous_month = current_date.replace(
            day=1) + relativedelta(days=-1)
        prev_seven_months.append(last_date_of_previous_month)
        current_date = last_date_of_previous_month
    prev_seven_months.reverse()
    assets_related_types = ('fixed_asset', 'accounts_receivable', 'other_asset', 'bank', 'cash', 'other_current_asset', 'stock')

    for account_head in transactions_map:
        temp = [0]*7

        for i in range(6, -1, -1):
            for transaction in transactions_map[account_head]:
                if transaction.transaction_date <= prev_seven_months[i]:
                    if account_head[1] in assets_related_types:
                        temp[i] += transaction.debit_amount - transaction.credit_amount
                    else:
                        temp[i] += transaction.credit_amount - transaction.debit_amount

        cashflow_data_uncategorized[account_head[0]] = temp


    cashflow_data['cashflow_from_operating_activities'].append(pbt_lst)
    temp = cashflow_data_uncategorized['Accounts Receivable']
    lst = [0]*6
    for i in range(5, -1, -1):
        lst[i] = temp[i]- temp[i+1]
    cashflow_data['cashflow_from_operating_activities'].append(lst)
   

    temp = cashflow_data_uncategorized['Other Current Assets'] if cashflow_data_uncategorized['Other Current Assets'] else [0]*7
    temp2 = cashflow_data_uncategorized['Other Non Current Assets'] if cashflow_data_uncategorized['Other Non Current Assets'] else [0]*7
    lst = [0]*6
    for i in range(5, -1, -1):
        lst[i] = temp[i] + temp2[i] - (temp[i+1] + temp2[i+1])
    cashflow_data['cashflow_from_operating_activities'].append(lst)

    temp = cashflow_data_uncategorized['Trade Payables'] if cashflow_data_uncategorized['Trade Payables'] else [0]*7
    lst = [0]*6
    for i in range(5, -1, -1):
        lst[i] = temp[i+1] - temp[i]
    cashflow_data['cashflow_from_operating_activities'].append(lst)

    temp = cashflow_data_uncategorized['Other long term Liabilities & Provisions'] if cashflow_data_uncategorized['Other long term Liabilities & Provisions'] else [0]*7
    temp2 = cashflow_data_uncategorized['Other Liabilities'] if cashflow_data_uncategorized['Other Liabilities'] else [0]*7
    temp3 = cashflow_data_uncategorized['Other Current Liabilities & Provisions'] if cashflow_data_uncategorized['Other Current Liabilities & Provisions'] else [0]*7
    lst = [0]*6
    for i in range(5, -1, -1):
        lst[i] = (temp[i+1] + temp2[i+1] + temp3[i+1]) - (temp[i] + temp2[i] + temp3[i]) 
    cashflow_data['cashflow_from_operating_activities'].append(lst)

    cashflow_data['net_cash_a'] = [0]*6
    for lst in cashflow_data['cashflow_from_operating_activities']:
        for i in range(6):
            cashflow_data['net_cash_a'][i] += lst[i]
    

    temp = cashflow_data_uncategorized['Tangible Assets'] if cashflow_data_uncategorized['Tangible Assets'] else [0]*7
    lst = [0]*6
    for i in range(5,-1,-1):
        lst[i] = temp[i] - temp[i+1]
    cashflow_data['cashflow_from_investing_activities'].append(lst)

    cashflow_data['cashflow_from_investing_activities'].append([0]*6)

    cashflow_data['net_cash_b'] = [0]*6
    for lst in cashflow_data['cashflow_from_investing_activities']:
        for i in range(6):
            cashflow_data['net_cash_b'][i] += lst[i]


    temp = cashflow_data_uncategorized['Short-term borrowings'] if cashflow_data_uncategorized['Short-term borrowings'] else [0]*7
    temp2 = cashflow_data_uncategorized['Long Term Borrowing'] if cashflow_data_uncategorized['Long Term Borrowing'] else [0]*7
    temp3 = cashflow_data_uncategorized['Short Term Loans & Advances'] if cashflow_data_uncategorized['Short Term Loans & Advances'] else [0]*7
    temp4 = cashflow_data_uncategorized['Long Term Loans & Advances'] if cashflow_data_uncategorized['Long Term Loans & Advances'] else [0]*7
    lst = [0]*6
    for i in range(5,-1,-1):
        lst[i] = (temp[i+1]+temp2[i+1]) - (temp[i]+temp2[i]) + (temp3[i]+temp4[i]) - (temp3[i+1]+temp4[i+1])
    cashflow_data['cashflow_from_financing_activities'].append(lst)

    temp = cashflow_data_uncategorized['Share Capital']
    lst = [0]*6
    for i in range(5,-1,-1):
        lst[i] = temp[i+1] - temp[i]
    cashflow_data['cashflow_from_financing_activities'].append(lst)
    
    cashflow_data['net_cash_c'] = [0]*6
    for lst in cashflow_data['cashflow_from_financing_activities']:
        for i in range(6):
            cashflow_data['net_cash_c'][i] += lst[i]

    monthly_cashflow_statement = {}
    for i in range(0, 6):
        month = prev_seven_months[i+1].month
        month_name = calendar.month_name[month]
        monthly_cashflow_statement[month_name] = {
            'cf_from_operations': round(cashflow_data['net_cash_a'][i]),
            'cf_from_investing': round(cashflow_data['net_cash_b'][i]),
            'cf_from_financing': round(cashflow_data['net_cash_c'][i])
        }
    return monthly_cashflow_statement


def get_pnl_summary(current_date):
    if current_date is None:
        current_date = date(2022, 6, 30)
    elif not isinstance(current_date, date):
        current_date = datetime.strptime(current_date, '%Y-%m-%d').date()

    accounts_related_to_pnl = ZohoAccount.objects.filter(
        account_type__in = ('income', 'expense', 'other_expense', 'cost_of_goods_sold')
    ).values_list('account_id', 'account_type')

    accounts_map = dict(accounts_related_to_pnl)
    
    transactions_related_to_pnl = ZohoTransaction.objects.filter(
        account_id__in = accounts_map
    )

    
    prev_six_months = [current_date]
    for i in range(5):
        last_date_of_previous_month = current_date.replace(
            day=1) + relativedelta(days=-1)
        prev_six_months.append(last_date_of_previous_month)
        current_date = last_date_of_previous_month
    prev_six_months.reverse()

    pnl_summary = {
        'months': [0]*6,
        'Income': [0]*6,
        'Cost of Goods Sold': [0]*6,
        'Gross profit': [0]*6,
        'Expenses': [0]*6,
        'Net Profit': [0]*6
    }
    for i in range(5, -1, -1):
        month = prev_six_months[i].month
        year = prev_six_months[i].year
        pnl_summary['months'][i] = calendar.month_name[month][:3] + '-' + str(year % 100)
        income, cogs, expenses = 0, 0, 0,
        for transaction in transactions_related_to_pnl:
            trans_date = transaction.transaction_date
            credit_minus_debit = transaction.credit_amount - transaction.debit_amount
            debit_minus_credit = transaction.debit_amount - transaction.credit_amount
            if trans_date.month == month and trans_date.year == year:
                if accounts_map[transaction.account_id] == 'income':
                    income += credit_minus_debit
                if accounts_map[transaction.account_id] == 'cost_of_goods_sold':
                    cogs += debit_minus_credit
                if accounts_map[transaction.account_id] in ('expense', 'other_expense'):
                    expenses += debit_minus_credit
        pnl_summary['Income'][i] = locale.format("%d", income, grouping=True)
        pnl_summary['Cost of Goods Sold'][i] = locale.format("%d", cogs, grouping=True)
        pnl_summary['Expenses'][i] = locale.format("%d", expenses, grouping=True)
        pnl_summary['Gross profit'][i] = locale.format("%d", income-cogs, grouping=True)
        pnl_summary['Net Profit'][i]  = locale.format("%d", income-cogs-expenses, grouping=True)
    
    return pnl_summary


def get_balance_sheet_summary(current_date):
    if current_date is None:
        current_date = date(2022, 6, 30)
    elif not isinstance(current_date, date):
        current_date = datetime.strptime(current_date, '%Y-%m-%d').date()

    accounts_related_to_balancesheet = ZohoAccount.objects.filter(
        account_type__in = (
            'accounts_payable',
            'accounts_receivable',
            'bank',
            'cash',
            'equity',
            'fixed_asset',
            'long_term_liability',
            'other_asset',
            'other_current_asset',
            'other_current_liability',
            'other_liability',
            'stock'
        )
    ).values_list('account_id', 'account_type')

    accounts_map = dict(accounts_related_to_balancesheet)

    transactions_related_to_balancesheet = ZohoTransaction.objects.filter(
        account_id__in = accounts_map
    )
    
    prev_six_months = [current_date]
    for i in range(5):
        last_date_of_previous_month = current_date.replace(
            day=1) + relativedelta(days=-1)
        prev_six_months.append(last_date_of_previous_month)
        current_date = last_date_of_previous_month
    prev_six_months.reverse()

    balance_sheet_summary = {
        'months': [0]*6,
        'Assets': [0]*6,
        'Liabilities': [0]*6,
        'Equity': [0]*6
    }
    for i in range(5, -1, -1):
        month = prev_six_months[i].month
        year = prev_six_months[i].year
        balance_sheet_summary['months'][i] = calendar.month_name[month][:3] + '-' + str(year)[2:]
        assets, liabilities, equity = 0, 0, 0,
        for transaction in transactions_related_to_balancesheet:
            debit_minus_credit = transaction.debit_amount - transaction.credit_amount
            credit_minus_debit = transaction.credit_amount - transaction.debit_amount
            if transaction.transaction_date <= prev_six_months[i]:
                if accounts_map[transaction.account_id] in ('fixed_asset', 'accounts_receivable', 'other_asset', 'bank', 'cash', 'other_current_asset', 'stock'):
                    assets += debit_minus_credit
                if accounts_map[transaction.account_id] in ('accounts_payable', 'long_term_liability', 'other_liability', 'other_current_liability'):
                    liabilities += credit_minus_debit
                if accounts_map[transaction.account_id] in ('equity'):
                    equity += credit_minus_debit

        balance_sheet_summary['Assets'][i] = locale.format("%d", assets, grouping=True)
        balance_sheet_summary['Liabilities'][i] = locale.format("%d", liabilities, grouping=True)
        balance_sheet_summary['Equity'][i] = locale.format("%d", equity, grouping=True)
    
    return balance_sheet_summary

def get_cashflow_summary(current_date):
    if current_date is None:
        current_date = date(2022, 6, 30)
    elif not isinstance(current_date, date):
        current_date = datetime.strptime(current_date, '%Y-%m-%d').date()
        
    monthly_cashflow_data = get_monthly_cashflow_statement(current_date)
    prev_six_months = [current_date]
    for i in range(5):
        last_date_of_previous_month = current_date.replace(
            day=1) + relativedelta(days=-1)
        prev_six_months.append(last_date_of_previous_month)
        current_date = last_date_of_previous_month
    prev_six_months.reverse()

    cashflow_summary = {
        'months': [0]*6,
        'Cashflow from Operations': [],
        'Cashflow from Investing': [],
        'Cashflow from Financing': []
    }
    for i in range(5, -1, -1):
        month = prev_six_months[i].month
        year = prev_six_months[i].year
        cashflow_summary['months'][i] = calendar.month_name[month][:3] + '-' + str(year % 100)

    for key in monthly_cashflow_data:
        cashflow_summary['Cashflow from Operations'].append(locale.format("%d", monthly_cashflow_data[key]['cf_from_operations'], grouping=True))
        cashflow_summary['Cashflow from Investing'].append(locale.format("%d", monthly_cashflow_data[key]['cf_from_investing'], grouping=True))
        cashflow_summary['Cashflow from Financing'].append(locale.format("%d", monthly_cashflow_data[key]['cf_from_financing'], grouping=True))

    return cashflow_summary