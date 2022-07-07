import copy
from accounts.models import ZohoAccount, ZohoTransaction
from utility import accounts_util, jsonobj
from dateutil.relativedelta import relativedelta
from datetime import date
import locale

locale.setlocale(locale.LC_ALL, 'en_IN.utf8')

pnl_pbt = {
    'current': 0,
    'previous': 0,
    'per_change': 0
}
pnl_dep_exp = {
    'current': 0,
    'previous': 0,
    'per_change': 0
}

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


def get_pnl(period):

    # Fetching accounts and transactions from database
    pnl_accounts_data, transactions_data = accounts_util.fetch_data_from_db(
        'pnl',
        period,
        ['income', 'expense', 'other_expense', 'cost_of_goods_sold']
    )

    accounts_map, transactions_map = {}, {}

    # Generating accounts_map to map account IDs with their account_type and account_for_coding
    for account in pnl_accounts_data:
        if account.account_for_coding == 'Interest Expenses':
            accounts_map[account.account_id] = (
                'interest_expenses', account.account_for_coding)
            continue

        if account.account_for_coding == 'Depreciation expenses':
            accounts_map[account.account_id] = (
                'depreciation_expenses', account.account_for_coding)
            continue

        if account.account_type in ('other_expense', 'expense'):
            accounts_map[account.account_id] = (
                'expense', account.account_for_coding, account.parent_account_name)
        else:
            accounts_map[account.account_id] = (
                account.account_type, account.account_for_coding)

    # Generating transaction_map to map account headers with the corresponding list of transactions
    for transaction in transactions_data:
        if transaction.account_id in accounts_map:
            account_header = accounts_map[transaction.account_id]
            if account_header not in transactions_map:
                transactions_map[account_header] = []
            transactions_map[account_header].append(transaction)

    # Defining structure for API response
    pnl_data = copy.deepcopy(jsonobj.json_structure['pnl_data'])

    # Filling up API response with relevant data
    for account_header in transactions_map:

        temporary_storage = {
            "account_header": account_header[1],
            "current": 0,
            "previous": 0,
            "per_change": 0,
            "three_month_avg": 0
        }

        # Calculating total amount for current, previous period and average of last 3 months for each account header
        for transaction in transactions_map[account_header]:
            credit_minus_debit = transaction.credit_amount - transaction.debit_amount
            if transaction.transaction_date.month == period.month:
                temporary_storage["current"] += credit_minus_debit
            elif transaction.transaction_date.month == period.month-1:
                temporary_storage["previous"] += credit_minus_debit
            temporary_storage["three_month_avg"] += credit_minus_debit

        temporary_storage['three_month_avg'] /= 3

        # Calculating percentage change
        if temporary_storage['previous'] == 0:
            temporary_storage['per_change'] = 0
        else:
            temporary_storage['per_change'] = (
                temporary_storage['current']/temporary_storage['previous'] - 1) * 100

        # Finally updating the data in response
        if len(account_header) == 2:
            pnl_data[account_header[0]].append(temporary_storage)

        else:
            if account_header[2] not in pnl_data[account_header[0]]:
                pnl_data[account_header[0]][account_header[2]] = []
            pnl_data[account_header[0]][account_header[2]].append(
                temporary_storage)

    # Calculating total income and costs of goods sold
    income_total, cogs_total = {
        'current': 0,
        'previous': 0,
        'per_change': 0,
        'three_month_avg': 0
    }, {
        'current': 0,
        'previous': 0,
        'per_change': 0,
        'three_month_avg': 0
    }

    for acc in pnl_data['income']:
        income_total['current'] += acc['current']
        income_total['previous'] += acc['previous']
        income_total['three_month_avg'] += acc['three_month_avg']
    income_total['per_change'] = 0 if income_total['previous'] == 0 else (
        income_total['current'] / income_total['previous'] - 1) * 100

    for k in ('current', 'previous', 'per_change', 'three_month_avg'):
        pnl_data['total_income'][k] = income_total[k]

    for acc in pnl_data['cost_of_goods_sold']:
        cogs_total['current'] += acc['current']
        cogs_total['previous'] += acc['previous']
        cogs_total['three_month_avg'] += acc['three_month_avg']
    cogs_total['per_change'] = 0 if cogs_total['previous'] == 0 else round((
        cogs_total['current'] / cogs_total['previous'] - 1) * 100)

    # Changing sign for expenses
    for cat in pnl_data['expense']:
        for acc in pnl_data['expense'][cat]:
            acc['current'] = -acc['current']
            acc['previous'] = -acc['previous']
            acc['three_month_avg'] = -acc['three_month_avg']

    # Calculating total expense
    expense_total = {
        'current': 0,
        'previous': 0,
        'per_change': 0,
        'three_month_avg': 0
    }

    for cat in pnl_data['expense']:
        for acc in pnl_data['expense'][cat]:
            expense_total['current'] += acc['current']
            expense_total['previous'] += acc['previous']
            expense_total['three_month_avg'] += acc['three_month_avg']
    expense_total['per_change'] = 0 if expense_total['previous'] == 0 else (
        expense_total['current'] / expense_total['previous'] - 1) * 100

    # Calculating gross profit and EBITDA
    for k in income_total:
        pnl_data['gross_profit'][k] = income_total[k] - cogs_total[k]
        pnl_data['ebitda'][k] = pnl_data['gross_profit'][k] - \
            expense_total[k]

    # Calculating PBIT
    if pnl_data['depreciation_expenses']:
        pnl_data['depreciation_expenses'] = pnl_data['depreciation_expenses'][0]
        for k in income_total:
            pnl_data['pbit'][k] = pnl_data['ebitda'][k] - \
                pnl_data['depreciation_expenses'][k]
    else:
        pnl_data['depreciation_expenses'] = {
            'current': 0,
            'previous': 0,
            'per_change': 0,
            'three_month_avg': 0
        }
        pnl_data['pbit'] = {
            'current': pnl_data['ebitda']['current'],
            'previous': pnl_data['ebitda']['previous'],
            'per_change': pnl_data['ebitda']['per_change'],
            'three_month_avg': pnl_data['ebitda']['three_month_avg']
        }

    # Calculating PBT
    if pnl_data['interest_expenses']:
        pnl_data['interest_expenses'] = pnl_data['interest_expenses'][0]
        for k in income_total:
            pnl_data['pbt'][k] = pnl_data['pbit'][k] - \
                pnl_data['interest_expenses'][k]
    else:
        pnl_data['interest_expenses'] = {
            'current': 0,
            'previous': 0,
            'per_change': 0,
            'three_month_avg': 0
        }
        pnl_data['pbt'] = {
            'current': pnl_data['pbit']['current'],
            'previous': pnl_data['pbit']['previous'],
            'per_change': pnl_data['pbit']['per_change'],
            'three_month_avg': pnl_data['pbit']['three_month_avg']
        }
    pnl_data['pbt'] = copy.deepcopy(pnl_data['pbit'])

    for k in ('gross_profit', 'ebitda', 'depreciation_expenses', 'pbit', 'interest_expenses', 'pbt'):
        pnl_data[k]['curr_per'] = round(
            pnl_data[k]['current']/income_total['current'] * 100)
        pnl_data[k]['prev_per'] = round(
            pnl_data[k]['previous']/income_total['previous'] * 100)

    global pnl_pbt, pnl_dep_exp
    pnl_pbt = copy.deepcopy(pnl_data['pbt'])
    pnl_dep_exp = copy.deepcopy(pnl_data['depreciation_expenses'])

    return pnl_data


def get_balsheet(period):
    # Fetching accounts and transactions from database
    bal_accounts_data, transactions_data = accounts_util.fetch_data_from_db(
        'balsheet',
        period,
        (
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
    )

    accounts_map, transactions_map = {}, {}

    for account in bal_accounts_data:
        accounts_map[account.account_id] = (
            account.account_type, account.account_for_coding
        )
    # Finding transactions related to each account header
    for transaction in transactions_data:
        if transaction.account_id in accounts_map:
            account_header = accounts_map[transaction.account_id]
            if account_header not in transactions_map:
                transactions_map[account_header] = []
            transactions_map[account_header].append(transaction)

    # Defining structure of API response for balance sheet data
    bal_sheet_data = copy.deepcopy(
        jsonobj.json_structure['bal_sheet_data'])

    # Filling up response with appropriate values
    for account_header in transactions_map:
        temporary_storage = {
            "account_header": account_header[1],
            "current": 0,
            "previous": 0,
            "pre_prev": 0,
            "per_change": 0,
            "three_month_avg": 0
        }

        for transaction in transactions_map[account_header]:
            credit_minus_debit = transaction.credit_amount - transaction.debit_amount
            temporary_storage["current"] += credit_minus_debit
            if transaction.transaction_date <= (period.replace(day=1)) + relativedelta(days=-1):
                temporary_storage['previous'] += credit_minus_debit
            if transaction.transaction_date <= (period + relativedelta(months=-2)):
                temporary_storage['pre_prev'] += credit_minus_debit

        temporary_storage["three_month_avg"] += (
            temporary_storage['current'] + temporary_storage['previous'] + temporary_storage['pre_prev'])/3

        if temporary_storage['previous'] == 0:
            temporary_storage['per_change'] = 0
        else:
            temporary_storage['per_change'] = (
                temporary_storage['current']/temporary_storage['previous'] - 1) * 100

        bal_sheet_data[account_header[0]].append(temporary_storage)

    for k in ('accounts_receivable', 'fixed_asset', 'other_asset', 'other_current_asset', 'stock', 'cash', 'bank'):
        for acc in bal_sheet_data[k]:
            acc['current'] = -acc['current']
            acc['previous'] = -acc['previous']

    for k in ('accounts_receivable', 'fixed_asset', 'other_asset', 'other_current_asset', 'stock', 'cash', 'bank'):
        for acc in bal_sheet_data[k]:
            bal_sheet_data['total_assets'] += acc['current']

    for k in ('accounts_payable', 'long_term_liability', 'other_current_liability', 'other_liability'):
        for acc in bal_sheet_data[k]:
            bal_sheet_data['total_liabilities'] += acc['current']

    for acc in bal_sheet_data['equity']:
        bal_sheet_data['total_equity'] = acc['current']

    return bal_sheet_data


def get_cashflow(period):
    # Fetching data related to cashflow accounts
    cashflow_accounts_data, transactions_data = accounts_util.fetch_data_from_db(
        'cashflow',
        period,
        cashflow_accounts
    )

    # Defining structure for API response
    cashflow_data = copy.deepcopy(jsonobj.json_structure['cashflow_data'])

    accounts_map, transactions_map = {}, {}
    cashflow_data_uncategorized = {}  # To store data related to all cashflow accounts
    assets_related_types = ('fixed_asset', 'accounts_receivable',
                            'other_asset', 'bank', 'cash', 'other_current_asset', 'stock')

    for account in cashflow_accounts:
        cashflow_data_uncategorized[account] = {
            'current': 0,
            'previous': 0,
            'pre_prev': 0
        }

    for account in cashflow_accounts_data:
        accounts_map[account.account_id] = (
            account.account_for_coding, account.account_type)

    for transaction in transactions_data:
        if transaction.account_id in accounts_map:
            acccount_header = accounts_map[transaction.account_id]
            if acccount_header not in transactions_map:
                transactions_map[acccount_header] = []
            transactions_map[acccount_header].append(transaction)

    for account_head in transactions_map:
        temporary_storage = {
            'current': 0,
            'previous': 0,
            'pre_prev': 0,
        }

        for transaction in transactions_map[account_head]:
            credit_minus_debit = transaction.credit_amount - transaction.debit_amount
            temporary_storage["current"] += credit_minus_debit
            if transaction.transaction_date <= (period.replace(day=1)) + relativedelta(days=-1):
                temporary_storage['previous'] += credit_minus_debit
            if transaction.transaction_date <= period + relativedelta(months=-2):
                temporary_storage['pre_prev'] += credit_minus_debit

        if account_head[1] in assets_related_types:
            temporary_storage['current'] = - \
                round(float(temporary_storage['current']))
            temporary_storage['previous'] = - \
                round(float(temporary_storage['previous']))
            temporary_storage['pre_prev'] = - \
                round(float(temporary_storage['pre_prev']))
        else:
            temporary_storage['current'] = round(
                float(temporary_storage['current']))
            temporary_storage['previous'] = round(
                float(temporary_storage['previous']))
            temporary_storage['pre_prev'] = round(
                float(temporary_storage['pre_prev']))

        cashflow_data_uncategorized[account_head[0]] = temporary_storage

    cashflow_from_operating_activities = 'cashflow_from_operating_activities'
    cashflow_from_investing_activities = 'cashflow_from_investing_activities'
    cashflow_from_financing_activities = 'cashflow_from_financing_activities'
    
    # Filling up response data with uncategorized and combined data
    temporary_storage = cashflow_data_uncategorized['Bank Balance']
    temporary_storage2 = cashflow_data_uncategorized['Cash Balance']
    cashflow_data['beginning_cash_balance'] = {
        'current': temporary_storage['previous'] + temporary_storage2['previous'],
        'previous': temporary_storage['pre_prev'] + temporary_storage2['pre_prev'],
        'per_change': 0 if (temporary_storage['pre_prev'] + temporary_storage2['pre_prev']) == 0 else round(((temporary_storage['previous'] + temporary_storage2['previous']) / (temporary_storage['pre_prev'] + temporary_storage2['pre_prev'])-1) * 100)
    }

    for act, val in {'Net Income': pnl_pbt, 'Plus: Depreciation & Amortization': pnl_dep_exp}.items():
        cashflow_data[cashflow_from_operating_activities].append({
            'activity': act,
            'current': round(val['current']),
            'previous': round(val['previous']),
            'per_change': round(val['per_change'])
        })

    temporary_storage = cashflow_data_uncategorized['Accounts Receivable']
    cashflow_data[cashflow_from_operating_activities].append({
        'activity': 'Increase / decrease in sundry debtors',
        'current': temporary_storage['previous'] - temporary_storage['current'],
        'previous': temporary_storage['pre_prev'] - temporary_storage['previous'],
        'per_change': 0 if (temporary_storage['pre_prev'] - temporary_storage['previous']) == 0 else round(((temporary_storage['previous'] - temporary_storage['current'])/(temporary_storage['pre_prev'] - temporary_storage['previous'])-1) * 100)
    })

    temporary_storage = cashflow_data_uncategorized['Other Current Assets']
    temporary_storage2 = cashflow_data_uncategorized['Other Non Current Assets']
    cashflow_data[cashflow_from_operating_activities].append({
        'activity': 'Increase / Decrease in Other Assets',
        'current': temporary_storage['previous'] + temporary_storage2['previous'] - (temporary_storage['current'] + temporary_storage2['current']),
        'previous': temporary_storage['pre_prev'] + temporary_storage2['pre_prev'] - (temporary_storage['previous'] + temporary_storage2['previous']),
        'per_change': 0 if temporary_storage['pre_prev'] + temporary_storage2['pre_prev'] - (temporary_storage['previous'] + temporary_storage2['previous']) == 0 else round(((temporary_storage['previous'] + temporary_storage2['previous'] - (temporary_storage['current'] + temporary_storage2['current']))/(temporary_storage['pre_prev'] + temporary_storage2['pre_prev'] - (temporary_storage['previous'] + temporary_storage2['previous']))-1)*100)
    })

    temporary_storage = cashflow_data_uncategorized['Trade Payables']
    cashflow_data[cashflow_from_operating_activities].append({
        'activity': 'Increase / Decrease in sundry creditors',
        'current': temporary_storage['current'] - temporary_storage['previous'],
        'previous': temporary_storage['previous'] - temporary_storage['pre_prev'],
        'per_change': 0 if temporary_storage['previous'] - temporary_storage['pre_prev'] == 0 else round(((temporary_storage['current'] - temporary_storage['previous'])/(temporary_storage['previous'] - temporary_storage['pre_prev']) - 1) * 100)
    })

    temporary_storage = cashflow_data_uncategorized['Other long term Liabilities & Provisions']
    temporary_storage2 = cashflow_data_uncategorized['Other Liabilities']
    temporary_storage3 = cashflow_data_uncategorized['Other Current Liabilities & Provisions']
    a = temporary_storage['current'] + temporary_storage2['current'] + temporary_storage3['current'] - \
        (temporary_storage['previous'] +
         temporary_storage2['previous'] + temporary_storage3['previous'])
    b = temporary_storage['previous'] + temporary_storage2['previous'] + temporary_storage3['previous'] - \
        (temporary_storage['pre_prev'] +
         temporary_storage2['pre_prev'] + temporary_storage3['pre_prev'])
    cashflow_data[cashflow_from_operating_activities].append({
        'activity': 'Increase / Decrease in Other Liability',
        'current': a,
        'previous': b,
        'per_change': 0 if b == 0 else round((a/b-1)*100)
    })

    for key in cashflow_data[cashflow_from_operating_activities]:
        cashflow_data['net_cash_a']['current'] += key['current']
        cashflow_data['net_cash_a']['previous'] += key['previous']
    cashflow_data['net_cash_a']['per_change'] = 0 if cashflow_data['net_cash_a']['previous'] == 0 else round(
        (cashflow_data['net_cash_a']['current']/cashflow_data['net_cash_a']['previous']-1)*100)

    temporary_storage = cashflow_data_uncategorized['Tangible Assets']
    cashflow_data[cashflow_from_investing_activities].append({
        'activity': 'Investments in Property & Equipment',
        'current': temporary_storage['previous'] - temporary_storage['current'],
        'previous': temporary_storage['pre_prev'] - temporary_storage['previous'],
        'per_change': 0 if (temporary_storage['pre_prev'] - temporary_storage['previous']) == 0 else round(((temporary_storage['previous'] - temporary_storage['current'])/(temporary_storage['pre_prev'] - temporary_storage['previous'])-1)*100)
    })

    cashflow_data[cashflow_from_investing_activities].append({
        'activity': 'Purchase / Sale of investments',
        'current': 0,
        'previous': 0,
        'per_change': 0
    })

    for key in cashflow_data[cashflow_from_investing_activities]:
        cashflow_data['net_cash_b']['current'] += key['current']
        cashflow_data['net_cash_b']['previous'] += key['previous']
    cashflow_data['net_cash_b']['per_change'] = 0 if cashflow_data['net_cash_b']['previous'] == 0 else round(
        (cashflow_data['net_cash_b']['current']/cashflow_data['net_cash_b']['previous']-1)*100)

    temporary_storage = cashflow_data_uncategorized['Short-term borrowings']
    temporary_storage2 = cashflow_data_uncategorized['Long Term Borrowing']
    temporary_storage3 = cashflow_data_uncategorized['Short Term Loans & Advances']
    temporary_storage4 = cashflow_data_uncategorized['Long Term Loans & Advances']
    a = temporary_storage['current'] + temporary_storage2['current'] - temporary_storage['previous'] - temporary_storage2['previous'] + \
        temporary_storage3['previous'] + temporary_storage4['previous'] - \
        temporary_storage3['current'] - temporary_storage4['current']
    b = temporary_storage['previous'] + temporary_storage2['previous'] - temporary_storage['pre_prev'] - temporary_storage2['pre_prev'] + \
        temporary_storage3['pre_prev'] + temporary_storage4['pre_prev'] - \
        temporary_storage3['previous'] - temporary_storage4['previous']
    cashflow_data[cashflow_from_financing_activities].append({
        'activity': 'Issuance (repayment) of debt',
        'current': a,
        'previous': b,
        'per_change': 0 if b == 0 else round((a/b-1)*100)
    })

    temporary_storage = cashflow_data_uncategorized['Share Capital']
    cashflow_data[cashflow_from_financing_activities].append({
        'activity': 'Issuance (repayment) of equity',
        'current': temporary_storage['current'] - temporary_storage['previous'],
        'previous': temporary_storage['previous'] - temporary_storage['pre_prev'],
        'per_change': 0 if temporary_storage['previous'] - temporary_storage['pre_prev'] == 0 else round(((temporary_storage['current'] - temporary_storage['previous'])/(temporary_storage['previous'] - temporary_storage['pre_prev'])-1)*100)
    })

    for key in cashflow_data[cashflow_from_financing_activities]:
        cashflow_data['net_cash_c']['current'] += key['current']
        cashflow_data['net_cash_c']['previous'] += key['previous']
    cashflow_data['net_cash_c']['per_change'] = 0 if cashflow_data['net_cash_c']['previous'] == 0 else round(
        (cashflow_data['net_cash_c']['current']/cashflow_data['net_cash_c']['previous']-1)*100)

    for k in ('current', 'previous'):
        cashflow_data['net_change_abc'][k] = (
            cashflow_data['net_cash_a'][k] + cashflow_data['net_cash_b'][k] + cashflow_data['net_cash_c'][k])
    cashflow_data['net_change_abc']['per_change'] = 0 if cashflow_data['net_change_abc']['previous'] == 0 else round(
        (cashflow_data['net_change_abc']['current']/cashflow_data['net_change_abc']['previous']-1)*100)

    cashflow_data['ending_cash_balance'] = {
        'current': cashflow_data['beginning_cash_balance']['current'] + cashflow_data['net_change_abc']['current'],
        'previous': cashflow_data['beginning_cash_balance']['previous'] + cashflow_data['net_change_abc']['previous']
    }
    cashflow_data['ending_cash_balance']['per_change'] = 0 if cashflow_data['ending_cash_balance']['previous'] == 0 else round(
        ((cashflow_data['ending_cash_balance']['current'])/(cashflow_data['ending_cash_balance']['previous'])-1)*100)

    return cashflow_data


def get_earnings(period):
    earnings_accounts_data = ZohoAccount.objects.filter(
        account_type__in=('income', 'expense',
                          'other_expense', 'cost_of_goods_sold')
    ).values_list('account_id', 'account_type')

    transactions_related_to_earnings = ZohoTransaction.objects.filter(
        account_id__in=(tup[0] for tup in earnings_accounts_data)
    )

    accounts_map = {}
    for account in earnings_accounts_data:
        accounts_map[account[0]] = account[1]

    current_year_period = date(2022, 4, 1)
    previous_period = period.replace(day=1)+relativedelta(days=-1)

    cy_income, cy_cogs, cy_expenses = {'current': 0, 'previous': 0}, {
        'current': 0, 'previous': 0}, {'current': 0, 'previous': 0}
    ret_income, ret_cogs, ret_expenses = {'current': 0, 'previous': 0}, {
        'current': 0, 'previous': 0}, {'current': 0, 'previous': 0}
    for transaction in transactions_related_to_earnings:
        credit_minus_debit = transaction.credit_amount - transaction.debit_amount
        debit_minus_credit = transaction.debit_amount - transaction.credit_amount
        if transaction.transaction_date >= current_year_period:
            if accounts_map[transaction.account_id] == 'income':
                cy_income['current'] += credit_minus_debit
            if accounts_map[transaction.account_id] == 'cost_of_goods_sold':
                cy_cogs['current'] += debit_minus_credit
            if accounts_map[transaction.account_id] in ('expense', 'other_expense'):
                cy_expenses['current'] += debit_minus_credit
        if transaction.transaction_date >= current_year_period and transaction.transaction_date <= previous_period:
            if accounts_map[transaction.account_id] == 'income':
                cy_income['previous'] += credit_minus_debit
            if accounts_map[transaction.account_id] == 'cost_of_goods_sold':
                cy_cogs['previous'] += debit_minus_credit
            if accounts_map[transaction.account_id] in ('expense', 'other_expense'):
                cy_expenses['previous'] += debit_minus_credit
        if transaction.transaction_date < current_year_period:
            if accounts_map[transaction.account_id] == 'income':
                ret_income['current'] += credit_minus_debit
            if accounts_map[transaction.account_id] == 'cost_of_goods_sold':
                ret_cogs['current'] += debit_minus_credit
            if accounts_map[transaction.account_id] in ('expense', 'other_expense'):
                ret_expenses['current'] += debit_minus_credit

    current_year_earnings = {
        'current': cy_income['current']-cy_cogs['current']-cy_expenses['current'],
        'previous': cy_income['previous']-cy_cogs['previous']-cy_expenses['previous'],
    }
    retained_earnings = {
        'current': ret_income['current']-ret_cogs['current']-ret_expenses['current'],
        'previous': ret_income['current']-ret_cogs['current']-ret_expenses['current'],
    }

    return current_year_earnings, retained_earnings
