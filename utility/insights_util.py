from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from accounts.models import ZohoAccount, ZohoTransaction
from utility import accounts_util
from utility import accounts_str as strvar
import locale
import json

current_str, previous_str, pre_prev_str = strvar.current, strvar.previous, strvar.pre_previous
curr_per_str, prev_per_str = strvar.current_per, strvar.previous_per
per_change_str, prev_per_change_str, three_month_avg_str = strvar.per_change, strvar.prev_per_change, strvar.three_month_avg
change_str, account_header_str = "change", "account_header"

config_file = open("config/analytics_config.json")
config_data = json.load(config_file)
insights_config_data = config_data['insights']

def get_insights(client_id, current_period):
    if current_period is None:
        current_period = date(2022, 6, 30)
    elif not isinstance(current_period, date):
        current_period = datetime.strptime(current_period, '%Y-%m-%d').date()

    parent_summary = {
        'Advertising and Marketing Expenses': 0, 
        'Employment Expenses': 0, 
        'General & Admin Charges': 0, 
        'Brokerage & Commission Charges': 0, 
        'Rent, Rates & Repairs Expenses': 0
    }
    

    accounts_related_to_expenses = ZohoAccount.objects.filter(
        client_id=client_id,
        account_type__in = insights_config_data['expense_related_types']
    ).values_list('account_id', 'parent_account_name')

    accounts_map = dict(accounts_related_to_expenses)
    
    prev_three_months = [current_period]
    current_date = current_period
    for i in range(2):
        last_date_of_previous_month = current_date.replace(
            day=1) + relativedelta(days=-1)
        prev_three_months.append(last_date_of_previous_month)
        current_date = last_date_of_previous_month
    
    transactions_for_last_three_months = ZohoTransaction.objects.filter(
        transaction_date__gte = prev_three_months[-1], account_id__in = accounts_map
    )

    transactions_map = {}
    for transaction in transactions_for_last_three_months:
        parent_account = accounts_map[transaction.account_id]
        if parent_account not in transactions_map:
            transactions_map[parent_account] = []
        transactions_map[parent_account].append(transaction)

    current, previous = prev_three_months[0], prev_three_months[1]
    for expense_head in parent_summary:
        temporary_storage = {
            current_str: 0,
            previous_str: 0,
            per_change_str: 0,
            three_month_avg_str: 0
        }
        if expense_head in transactions_map:
            for transaction in transactions_map[expense_head]:
                trans_date = transaction.transaction_date
                debit_minus_credit = transaction.debit_amount - transaction.credit_amount
                if trans_date.month == current.month and trans_date.year == current.year:
                    temporary_storage[current_str] += debit_minus_credit
                if trans_date.month == previous.month and trans_date.year == previous.year:
                    temporary_storage[previous_str] += debit_minus_credit
                temporary_storage[three_month_avg_str] += debit_minus_credit

        temporary_storage[per_change_str] = 0 if temporary_storage[previous_str] == 0 else round((temporary_storage[current_str]/temporary_storage[previous_str]-1)*100)
        temporary_storage[three_month_avg_str] = locale.format("%.2f", temporary_storage[three_month_avg_str] / 3, grouping=True)
        temporary_storage[change_str] = locale.format("%.2f", temporary_storage[current_str] -  temporary_storage[previous_str], grouping=True)
        temporary_storage[current_str] = locale.format("%.2f", temporary_storage[current_str], grouping=True)
        temporary_storage[previous_str] = locale.format("%.2f", temporary_storage[previous_str], grouping=True)
        parent_summary[expense_head] = temporary_storage

    current_month_payees = {}
    previous_month_payees = {}
    for expense_head in parent_summary:
        current_month_payees[expense_head] = {}
        previous_month_payees[expense_head] = {}
        if expense_head in transactions_map:
            temporary_storage_curr = current_month_payees[expense_head]
            temporary_storage_prev = previous_month_payees[expense_head]
            for transaction in transactions_map[expense_head]:
                trans_date = transaction.transaction_date
                debit_minus_credit = transaction.debit_amount - transaction.credit_amount
                payee = transaction.payee
                if trans_date.month == current.month and trans_date.year == current.year:
                    if payee not in temporary_storage_curr:
                        temporary_storage_curr[payee] = 0
                    temporary_storage_curr[payee] += debit_minus_credit
                if trans_date.month == previous.month and trans_date.year == previous.year:
                    if payee not in temporary_storage_prev:
                        temporary_storage_prev[payee] = 0
                    temporary_storage_prev[payee] += debit_minus_credit
    
    insights_data = {}
    for key in parent_summary:
        insights_data[key] = []
        curr_dic = current_month_payees[key]
        prev_dic = previous_month_payees[key]
        for k in curr_dic:
            new_amount = curr_dic[k]
            if k not in prev_dic:
                if new_amount >= 5000:
                    insights_data[key].append(
                        {
                            'payee': k,
                            'additional': locale.format("%.2f", new_amount, grouping=True)
                        }
                    )
            else:
                addn_amount =  curr_dic[k] - prev_dic[k]
                if addn_amount >= 5000:
                    insights_data[key].append(
                        {
                            'payee': k,
                            'additional': locale.format("%.2f", curr_dic[k] - prev_dic[k], grouping=True)
                        }
                    )

    insights_data = {
        'advt_and_marketing_header': parent_summary['Advertising and Marketing Expenses'],
        'advt_and_marketing_insights': insights_data['Advertising and Marketing Expenses'],
        'employement_header':parent_summary['Employment Expenses'],
        'employement_insights':insights_data['Employment Expenses'],
        'rent_rates_and_repairs_header':parent_summary['Rent, Rates & Repairs Expenses'],
        'rent_rates_and_repairs_insights':insights_data['Rent, Rates & Repairs Expenses'],
        'brokerage_and_commission_header': parent_summary['Brokerage & Commission Charges'],
        'brokerage_and_commission_insights':insights_data['Brokerage & Commission Charges'],
        'general_and_admin_header': parent_summary['General & Admin Charges'],
        'general_and_admin_insights':insights_data['General & Admin Charges']
    }

    return insights_data


def fetch_insights_transaction(period, client_id, exp_head):

    accounts_for_expense = ZohoAccount.objects.filter(
        client_id=client_id,
        parent_account_name=exp_head
    )

    account_ids = dict((acc.account_id, acc.parent_account_name) for acc in accounts_for_expense)
    
    prev_three_months = [period]
    current_date = period
    for i in range(2):
        last_date_of_previous_month = current_date.replace(
            day=1) + relativedelta(days=-1)
        prev_three_months.append(last_date_of_previous_month)
        current_date = last_date_of_previous_month

    related_transactions = ZohoTransaction.objects.filter(
        account_id__in=account_ids,
        transaction_date__gte=prev_three_months[2].replace(day=1),
        transaction_date__lte=period
    ).values('transaction_date', 'payee', 'debit_amount', 'credit_amount')

    response_data = {}

    for transaction in related_transactions:
        payee = transaction['payee']
        trans_date = transaction['transaction_date']

        amount = transaction['debit_amount'] - transaction['credit_amount']

        if payee not in response_data:
            response_data[payee] = {
                current_str: 0,
                previous_str: 0,
                per_change_str: 0,
                three_month_avg_str: 0
            }

        if prev_three_months[1] < trans_date <= prev_three_months[0]:
            response_data[payee][current_str] += amount

        elif prev_three_months[2] < trans_date <= prev_three_months[1]:
            response_data[payee][previous_str] += amount

        response_data[payee][three_month_avg_str] += amount

    total = {
        current_str: 0,
        previous_str: 0,
        per_change_str: 0,
        three_month_avg_str: 0
    }
    for k in response_data:
        obj = response_data[k]

        obj[per_change_str] = 0 if obj[previous_str] == 0 \
            else accounts_util.change_percentage((obj[current_str]/obj[previous_str]-1)*100, trans_flag=True)
        obj[three_month_avg_str] = obj[three_month_avg_str]/3
        obj[current_str] = obj[current_str]
        obj[previous_str] = obj[previous_str]
        total[current_str] += obj[current_str]
        total[previous_str] += obj[previous_str]
    
    total[per_change_str] = 0 if total[previous_str] == 0 \
        else accounts_util.change_percentage((total[current_str]/total[previous_str]-1)*100, trans_flag=True)
    
    # defining distinct payees for current financial year to check category or status of payee
    if period.month >= 4:
        curr_fy_start = f'{period.year}-04-01'
    else:
        curr_fy_start = f'{period.year-1}-04-01'

    curr_fy_prev = period.replace(day=1) + relativedelta(days=-1)
    distict_payees_in_cfy = ZohoTransaction.objects.filter(transaction_date__gte=curr_fy_start, transaction_date__lte=curr_fy_prev).values('payee').distinct()
    payees_for_cfy = dict((dic['payee'], 0) for dic in distict_payees_in_cfy)
    
    response_data_filtered = {}
    for k in response_data:
        obj = response_data[k]
        # defining status of payee
        if k in payees_for_cfy:
            obj['payee_category'] = 'Regular'
        else:
            obj['payee_category'] = 'New'

        if (abs(round(obj[current_str])), abs(round(obj[previous_str]))) == (0,0):
            continue
        total[three_month_avg_str] += obj[three_month_avg_str]
        response_data_filtered[k.title()] = obj

    response_data_filtered = dict(sorted(
        response_data_filtered.items(), 
        key=lambda x: (x[1][current_str], x[1][previous_str]),
        reverse=True
    ))

    return (response_data_filtered, total, prev_three_months)


def get_deep_insight_one(client_id, current_period):
    if current_period is None:
        current_period = date(2022, 6, 30)
    elif not isinstance(current_period, date):
        current_period = datetime.strptime(current_period, '%Y-%m-%d').date()

    accounts_related_to_cash = ZohoAccount.objects.filter(
        client_id=client_id,
        account_type = strvar.cash
    ).values_list('account_id', 'account_name')

    accounts_map = dict(accounts_related_to_cash)

    curr_month_start_date = current_period.replace(day=1)
    curr_month_end_date = current_period

    transactions_related_to_cash = ZohoTransaction.objects.filter(
        account_id__in = accounts_map, 
        transaction_date__gte = curr_month_start_date,
    )

    datewise_transactions = {}
    
    current_date = curr_month_start_date
    while current_date <= curr_month_end_date:
        temporary_storage = {}
        for transaction in transactions_related_to_cash:
            if transaction.transaction_date == current_date:
                key = (transaction.payee, accounts_map[transaction.account_id])
                if key not in temporary_storage:
                    temporary_storage[key] = 0
                temporary_storage[key] += (transaction.debit_amount - transaction.credit_amount)

        if temporary_storage and temporary_storage[key] > 10000:
            datewise_transactions[current_date] = temporary_storage
        current_date += relativedelta(days=1)
    
    deep_insight_one_data = []
    for dt in datewise_transactions:
        for key in datewise_transactions[dt]:
            cash_expense = {
                'account_name': key[1],
                'payee': key[0],
                'date': dt,
                'amount': locale.format("%.2f",  datewise_transactions[dt][key], grouping=True)
            }
        deep_insight_one_data.append(cash_expense)
    
    return deep_insight_one_data


def get_deep_insight_two(client_id, current_period):
    if current_period is None:
        current_period = date(2022, 6, 30)
    elif not isinstance(current_period, date):
        current_period = datetime.strptime(current_period, '%Y-%m-%d').date()
    
    accounts_related_to_loans = ZohoAccount.objects.filter(
        client_id=client_id,
        account_for_coding__in = insights_config_data['accounts_related_to_borrowings']
    ).values_list('account_id', 'account_name')

    accounts_map = dict(accounts_related_to_loans)

    transactions_related_to_loans = ZohoTransaction.objects.filter(
        account_id__in = accounts_map
    )
    
    loan_map = {}
    for transaction in transactions_related_to_loans:
        if transaction.account_id not in loan_map:
            loan_map[transaction.account_id] = 0
        loan_map[transaction.account_id] += (transaction.credit_amount - transaction.debit_amount)
    
    deep_insight_two_data = []
    for key in loan_map:
        deep_insight_two_data.append({
            'account_name': accounts_map[key],
            'amount': locale.format("%.2f", loan_map[key], grouping=True)
        })
    return deep_insight_two_data


def get_deep_insight_three(client_id, current_period):
    if current_period is None:
        current_period = date(2022, 6, 30)
    elif not isinstance(current_period, date):
        current_period = datetime.strptime(current_period, '%Y-%m-%d').date()

    month, year = current_period.month, current_period.year
    start_of_current_fy = date(year, 4, 1) if  month >= 4 else date(year-1, 4, 1)

    accounts_related_to_revenue = ZohoAccount.objects.filter(
        client_id=client_id,
        account_for_coding = strvar.direct_income
    ).values_list('account_id')

    transactions_related_to_revenue = ZohoTransaction.objects.filter(
        account_id__in = (tup[0] for tup in accounts_related_to_revenue), 
        transaction_date__gte = start_of_current_fy,
        transaction_date__lte = current_period
    )

    total_revenue = 0
    for transaction in transactions_related_to_revenue:
        total_revenue += transaction.credit_amount

    deep_insight_three_data = 'Total sales for this financial year ' + locale.currency(total_revenue, grouping=True)

    return deep_insight_three_data


def get_deep_insight_four(client_id, current_period):
    if current_period is None:
        current_period = date(2022, 6, 30)
    elif not isinstance(current_period, date):
        current_period = datetime.strptime(current_period, '%Y-%m-%d').date()

    current_month_start = current_period.replace(day=1)
    previous_month_start = (current_month_start + relativedelta(days=-1)).replace(day=1)

    accounts_related_to_expenses = ZohoAccount.objects.filter(
        client_id=client_id,
        account_type__in = insights_config_data['expense_related_types']
    ).values_list('account_id', 'account_for_coding')

    accounts_map = dict(accounts_related_to_expenses)
    
    transactions_related_to_expense = ZohoTransaction.objects.filter(
        account_id__in = accounts_map, 
        transaction_date__gte = previous_month_start,
        transaction_date__lte = current_period
    )

    transactions_map = {}
    for transaction in transactions_related_to_expense:
        if transaction.account_id in accounts_map:
            account_header = ' '.join(accounts_map[transaction.account_id].split('_')).title()
            if account_header not in transactions_map:
                transactions_map[account_header] = []
            transactions_map[account_header].append(transaction)

    deep_insight_four_data = []
    for account_header in transactions_map:

        temporary_storage = {
            account_header_str: account_header,
            current_str: 0,
            previous_str: 0,
            per_change_str: 0,
        }

        for transaction in transactions_map[account_header]:
            trans_date = transaction.transaction_date
            debit_minus_credit = transaction.debit_amount - transaction.credit_amount
            if trans_date >= current_month_start:
                temporary_storage[current_str] += debit_minus_credit
            elif transaction.transaction_date >= previous_month_start and trans_date < current_month_start:
                temporary_storage[previous_str] += debit_minus_credit

        if temporary_storage[previous_str] == 0:
            temporary_storage[per_change_str] = 100 if temporary_storage[current_str] != 0 else 0
        else:
            temporary_storage[per_change_str] = round((
                temporary_storage[current_str]/temporary_storage[previous_str] - 1) * 100)

        if temporary_storage[current_str] > 10000 and temporary_storage[per_change_str] >= 25:
            temporary_storage[current_str] = locale.format("%.2f", temporary_storage[current_str], grouping=True)
            temporary_storage[previous_str] = locale.format("%.2f", temporary_storage[previous_str], grouping=True)
            deep_insight_four_data.append(temporary_storage)


    return deep_insight_four_data


def get_deep_insight_five(client_id, current_period):
    if current_period is None:
        current_period = date(2022, 6, 30)
    elif not isinstance(current_period, date):
        current_period = datetime.strptime(current_period, '%Y-%m-%d').date()

    accounts_related_to_assets = ZohoAccount.objects.filter(
        client_id=client_id,
        account_type__in = insights_config_data['asset_related_accounts']
    ).values_list('account_id', 'account_name')
    assets_accounts_map = dict(accounts_related_to_assets)

    accounts_related_to_liabilities = ZohoAccount.objects.filter(
        client_id=client_id,
        account_type__in = insights_config_data['liabilities_related_accounts']
    ).values_list('account_id', 'account_name')
    liabilities_accounts_map = dict(accounts_related_to_liabilities)

    transactions_related_to_assets = ZohoTransaction.objects.filter(
        account_id__in = assets_accounts_map, transaction_date__lte = current_period
    )

    transactions_related_to_liabilities = ZohoTransaction.objects.filter(
        account_id__in = liabilities_accounts_map, transaction_date__lte = current_period
    )

    asset_wise_transactions = {}
    for transaction in transactions_related_to_assets:
        account_name = assets_accounts_map[transaction.account_id]
        if account_name not in asset_wise_transactions:
            asset_wise_transactions[account_name] = 0
        asset_wise_transactions[account_name] += (transaction.debit_amount - transaction.credit_amount)
    
    liability_wise_transactions = {}
    for transaction in transactions_related_to_liabilities:
        account_name = liabilities_accounts_map[transaction.account_id]
        if account_name not in liability_wise_transactions:
            liability_wise_transactions[account_name] = 0
        liability_wise_transactions[account_name] += (transaction.credit_amount - transaction.debit_amount)


    deep_insight_five_data = []

    for key in asset_wise_transactions:
        amount = asset_wise_transactions[key]
        if amount < 0:
            deep_insight_five_data.append({
                'account_name': key,
                'amount': locale.format("%.2f", amount, grouping=True)
            })
    
    for key in liability_wise_transactions:
        amount = liability_wise_transactions[key]
        if amount < 0:
            deep_insight_five_data.append({
                'account_name': key,
                'amount': locale.format("%.2f", amount, grouping=True)
            })

    return deep_insight_five_data


def get_deep_insight_six(client_id, current_period):
    if current_period is None:
        current_period = date(2022, 6, 30)
    elif not isinstance(current_period, date):
        current_period = datetime.strptime(current_period, '%Y-%m-%d').date()

    accounts_for_payable_receivable = ZohoAccount.objects.filter(
        client_id=client_id,
        account_name__in = ('Accounts Payable', 'Accounts Receivable')
    ).values_list('account_name', 'account_id')

    accounts_map = dict(accounts_for_payable_receivable)
    
    transactions_related_accounts_for_payable_receivable = ZohoTransaction.objects.filter(
        account_id__in = accounts_map.values(), transaction_date__lte = current_period
    )

    temporary_storage_acc_rec = {}
    temporary_storage_acc_pay = {}

    for transaction in transactions_related_accounts_for_payable_receivable:
        if transaction.account_id == accounts_map['Accounts Receivable']:
            key = transaction.payee
            if key not in temporary_storage_acc_rec:
                temporary_storage_acc_rec[key] = 0
            temporary_storage_acc_rec[key] += (transaction.debit_amount - transaction.credit_amount)
        else:
            key = transaction.payee
            if key not in temporary_storage_acc_pay:
                temporary_storage_acc_pay[key] = 0
            temporary_storage_acc_pay[key] += (transaction.credit_amount - transaction.debit_amount)

    deep_insight_six_data = []
    for key in temporary_storage_acc_rec:
        if temporary_storage_acc_rec[key] < 0:
            deep_insight_six_data.append({
                'account_name': 'Acounts Receivable',
                'payee': key,
                'amount': locale.format("%.2f", temporary_storage_acc_rec[key], grouping=True)
            })
    
    for key in temporary_storage_acc_pay:
        if temporary_storage_acc_pay[key] < 0:
            deep_insight_six_data.append({
                'account_name': 'Acounts Payable',
                'payee': key,
                'amount': locale.format("%.2f", temporary_storage_acc_pay[key], grouping=True)
            })
    
    return deep_insight_six_data


def get_deep_insight_seven(client_id, current_period):
    if current_period is None:
        current_period = date(2022, 6, 30)
    elif not isinstance(current_period, date):
        current_period = datetime.strptime(current_period, '%Y-%m-%d').date()

    month, year = current_period.month, current_period.year
    start_of_current_fy = date(year, 4, 1) if  month >= 4 else date(year-1, 4, 1)

    accounts_related_to_rent_expenses = ZohoAccount.objects.filter(
        client_id=client_id,
        account_for_coding = strvar.rent_expenses
    ).values_list('account_id')

    transactions_related_to_rent_expenses = ZohoTransaction.objects.filter(
        account_id__in = (tup[0] for tup in accounts_related_to_rent_expenses), 
        transaction_date__gte = start_of_current_fy,
        transaction_date__lte = current_period
    )

    temporary_storage = {}
    for transaction in transactions_related_to_rent_expenses:
        key = transaction.payee
        if key not in temporary_storage:
            temporary_storage[key] = 0
        temporary_storage[key] += (transaction.debit_amount - transaction.credit_amount)
    
    deep_insight_seven_data = []
    for key in temporary_storage:
        if temporary_storage[key] > 240000:
            deep_insight_seven_data.append({
                'payee': key if key != '' else 'Unknown',
                'amount': locale.currency(temporary_storage[key], grouping=True)
            })

    return deep_insight_seven_data

def get_deep_insight_eight(client_id, current_period):
    if current_period is None:
        current_period = date(2022, 6, 30)
    elif not isinstance(current_period, date):
        current_period = datetime.strptime(current_period, '%Y-%m-%d').date()

    month, year = current_period.month, current_period.year
    start_of_current_fy = date(year, 4, 1) if  month >= 4 else date(year-1, 4, 1)

    accounts_related_to_commission = ZohoAccount.objects.filter(
        client_id=client_id,
        account_for_coding = strvar.brokerage_and_commission_charges
    ).values_list('account_id')

    transactions_related_to_commission = ZohoTransaction.objects.filter(
        account_id__in = (tup[0] for tup in accounts_related_to_commission), 
        transaction_date__gte = start_of_current_fy,
        transaction_date__lte = current_period
    )

    temporary_storage = {}
    for transaction in transactions_related_to_commission:
        key = transaction.payee
        if key not in temporary_storage:
            temporary_storage[key] = 0
        temporary_storage[key] += (transaction.debit_amount - transaction.credit_amount)
    
    deep_insight_eight_data = []
    for key in temporary_storage:
        if temporary_storage[key] > 15000:
            deep_insight_eight_data.append({
                'payee': key if key != '' else 'Unknown',
                'amount': locale.currency(temporary_storage[key], grouping=True)
            })

    return deep_insight_eight_data

def get_deep_insight_nine(client_id, current_period):
    if current_period is None:
        current_period = date(2022, 6, 30)
    elif not isinstance(current_period, date):
        current_period = datetime.strptime(current_period, '%Y-%m-%d').date()

    month, year = current_period.month, current_period.year
    start_of_current_fy = date(year, 4, 1) if  month >= 4 else date(year-1, 4, 1)

    accounts_related_to_professional_fees = ZohoAccount.objects.filter(
        client_id=client_id,
        account_for_coding = strvar.legal_and_professional_fees
    ).values_list('account_id')

    transactions_related_to_professional_fees = ZohoTransaction.objects.filter(
        account_id__in = (tup[0] for tup in accounts_related_to_professional_fees), 
        transaction_date__gte = start_of_current_fy,
        transaction_date__lte = current_period
    )

    temporary_storage = {}
    for transaction in transactions_related_to_professional_fees:
        key = transaction.payee
        if key not in temporary_storage:
            temporary_storage[key] = 0
        temporary_storage[key] += (transaction.debit_amount - transaction.credit_amount)
    
    deep_insight_nine_data = []
    for key in temporary_storage:
        if temporary_storage[key] > 30000:
            deep_insight_nine_data.append({
                'payee': key if key != '' else 'Unknown',
                'amount': locale.currency(temporary_storage[key], grouping=True)
            })

    return deep_insight_nine_data

def get_deep_insight_ten(client_id, current_period):
    if current_period is None:
        current_period = date(2022, 6, 30)
    elif not isinstance(current_period, date):
        current_period = datetime.strptime(current_period, '%Y-%m-%d').date()

    accounts_related_to_expenses = ZohoAccount.objects.filter(
        client_id=client_id,
        account_type__in = insights_config_data['expense_related_types']
    ).values_list('account_id', 'account_for_coding')

    accounts_map = dict(accounts_related_to_expenses)

    prev_four_months = [current_period]
    current_date = current_period
    for i in range(3):
        first_date_of_previous_month = (current_date.replace(
            day=1) + relativedelta(days=-1)).replace(day=1)
        prev_four_months.append(first_date_of_previous_month)
        current_date = first_date_of_previous_month
    prev_four_months.sort()
    
    transactions_related_to_expense = ZohoTransaction.objects.filter(
        account_id__in = accounts_map, 
        transaction_date__gte = prev_four_months[0],
        transaction_date__lte = current_period
    )

    month_wise_payee = {
        "1": set(), "2": set(), "3": set(),current_str: set()
    }

    for transaction in transactions_related_to_expense:
        trans_date = transaction.transaction_date
        if trans_date >= prev_four_months[0] and trans_date < prev_four_months[1]:
            month_wise_payee["1"].add(transaction.payee)
        elif trans_date >= prev_four_months[1] and trans_date < prev_four_months[2]:
            month_wise_payee["2"].add(transaction.payee)
        elif trans_date >= prev_four_months[2] and trans_date < prev_four_months[3]:
            month_wise_payee["3"].add(transaction.payee)
        else:
            month_wise_payee[current_str].add(transaction.payee)

    absent_payees = set()
    for transaction in transactions_related_to_expense:
        payee = transaction.payee
        if (payee in month_wise_payee['1']) and (payee in month_wise_payee['2']) and (payee in month_wise_payee['3']):
            if payee not in month_wise_payee[current_str]:
                absent_payees.add(payee)

    deep_insight_ten_data = []
    for payee in absent_payees:
        payee = payee if payee != '' else 'Unknown'
        deep_insight_ten_data.append(
            f'{payee} has no transactions for current month'
        )

    return deep_insight_ten_data

def get_deep_insight_eleven(client_id, current_period):
    if current_period is None:
        current_period = date(2022, 6, 30)
    elif not isinstance(current_period, date):
        current_period = datetime.strptime(current_period, '%Y-%m-%d').date()

    current_month_start = current_period.replace(day=1)

    accounts_related_to_uncategorized = ZohoAccount.objects.filter(
        client_id=client_id,
        account_name = 'Uncategorized'
    ).get()
    
    transactions_related_to_uncategorized = ZohoTransaction.objects.filter(
        account_id = accounts_related_to_uncategorized.account_id, transaction_date__gte = current_month_start
    )
    
    total_transactions, total_amount = 0, 0
    for transaction in transactions_related_to_uncategorized:
        total_transactions += 1
        total_amount += (transaction.debit_amount - transaction.credit_amount)
    
    deep_insight_eleven_data = f'There are total {total_transactions} Uncategorized transactions worth {total_amount}'

    return deep_insight_eleven_data

def get_deep_insight_twelve(client_id, current_period):
    if current_period is None:
        current_period = date(2022, 6, 30)
    elif not isinstance(current_period, date):
        current_period = datetime.strptime(current_period, '%Y-%m-%d').date()

    current_month_start = current_period.replace(day=1)

    accounts_related_to_bank = ZohoAccount.objects.filter(
        client_id=client_id,
        account_for_coding = insights_config_data['account_for_bank_balance']
    ).values_list('account_id', 'account_name')

    accounts_map = dict(accounts_related_to_bank)

    transactions_related_to_bank = ZohoTransaction.objects.filter(
        account_id__in = accounts_map, transaction_date__gte = current_month_start
    )

    temporary_storage = {}
    double_transactions = {}
    for transaction in transactions_related_to_bank:
        credit_minus_debit = transaction.credit_amount - transaction.debit_amount
        trans_date = transaction.transaction_date
        key = transaction.payee
        if key not in temporary_storage:
            temporary_storage[key] = (credit_minus_debit, trans_date)
        else:
            if temporary_storage[key] == (credit_minus_debit, trans_date):
                double_transactions[transaction.payee] = (accounts_map[transaction.account_id], trans_date, credit_minus_debit)

    deep_insight_twelve_data = []
    for duplicate in double_transactions:
        val = double_transactions[duplicate]
        deep_insight_twelve_data.append({
            "account_name": val[0],
            "payee": duplicate,
            "date": val[1],
            "amount": val[2]
        })

    return deep_insight_twelve_data