import copy
from accounts.models import ZohoAccount, ZohoTransaction, Ratio
from utility import accounts_util, jsonobj
from dateutil.relativedelta import relativedelta
from datetime import date, datetime
import locale
import json

locale.setlocale(locale.LC_ALL, 'en_IN.utf8')
account_header_str, account_for_coding_str, activity_str, data_str = "account_header", "account_for_coding", "activity", "data"
current_str, previous_str, pre_prev_str, per_change_str, three_month_avg_str = "current", "previous", "pre_prev", "per_change", "three_month_avg"


cashflow_accounts = (
    'bank_balance',
    'cash_balance',
    'accounts_receivable',
    'other_current_assets',
    'other_non_current_assets',
    'trade_payables',
    'other_long_term_liabilities_and_provisions',
    'other_liabilities',
    'other_current_liabilities_and_provisions',
    'tangible_assets',
    'short_term_loans_and_advances',
    'long_term_loans_and_advances',
    'short_term_borrowings',
    'long_term_borrowings',
    'share_capital'
)


config_file = open("config/accounts_config.json")
config_data = json.load(config_file)


def get_pnl(period, logged_client_id):

    # Fetching accounts and transactions from database
    pnl_accounts_data, transactions_data = accounts_util.fetch_data_from_db(
        'pnl',
        logged_client_id,
        period,
        ['income', 'expense', 'other_expense', 'cost_of_goods_sold']
    )

    accounts_map, transactions_map = {}, {}

    # Generating accounts_map to map account IDs with their account_type and account_for_coding
    for account in pnl_accounts_data:
        if account.get_account_for_coding_display() == 'Interest Expenses':
            accounts_map[account.account_id] = (
                'interest_expenses', account.get_account_for_coding_display())
            continue

        if account.get_account_for_coding_display() == 'Depreciation expenses':
            accounts_map[account.account_id] = (
                'depreciation_expenses', account.get_account_for_coding_display())
            continue

        if account.account_type in ('other_expense', 'expense'):
            accounts_map[account.account_id] = (
                'expense', account.get_account_for_coding_display(), account.parent_account_name, account.account_for_coding)
        else:
            accounts_map[account.account_id] = (
                account.account_type, account.get_account_for_coding_display(), account.account_for_coding)

    # Generating transaction_map to map account headers with the corresponding list of transactions
    for transaction in transactions_data:
        if transaction.account_id in accounts_map:
            account_header = accounts_map[transaction.account_id]
            if account_header not in transactions_map:
                transactions_map[account_header] = []
            transactions_map[account_header].append(transaction)

    # Defining structure for API response
    pnl_data = copy.deepcopy(jsonobj.json_structure['pnl_data'])

    # current month and previous month
    curr_month, curr_year = period.month, period.year
    prev_month, prev_year = (
        12, curr_year-1) if period.month == 1 else (period.month - 1, curr_year)

    # Filling up API response with relevant data
    for account_header in transactions_map:

        temporary_storage = {
            account_header_str: account_header[1],
            account_for_coding_str: account_header[-1],
            current_str: 0,
            previous_str: 0,
            per_change_str: 0,
            three_month_avg_str: 0
        }

        # Calculating total amount for current, previous period and average of last 3 months for each account header
        for transaction in transactions_map[account_header]:
            trans_date = transaction.transaction_date
            debit_minus_credit = transaction.debit_amount - transaction.credit_amount
            if (trans_date.month, trans_date.year) == (curr_month, curr_year):
                temporary_storage[current_str] += debit_minus_credit
            elif (trans_date.month, trans_date.year) == (prev_month, prev_year):
                temporary_storage[previous_str] += debit_minus_credit
            temporary_storage[three_month_avg_str] += debit_minus_credit

        temporary_storage[three_month_avg_str] /= 3

        # Calculating percentage change
        if temporary_storage[previous_str] == 0:
            temporary_storage[per_change_str] = 0
        else:
            temporary_storage[per_change_str] = round((
                temporary_storage[current_str]/temporary_storage[previous_str] - 1) * 100)

        # Checking if there are no values for current and previous month
        if (abs(round(temporary_storage[current_str])), abs(round(temporary_storage[previous_str]))) == (0, 0):
            continue

        # Finally updating the data in response
        if account_header[1] in ('Direct Income', 'Indirect Income'):
            pnl_data[account_header[0]][data_str].append(temporary_storage)

        elif len(account_header) > 3:
            if account_header[2] not in pnl_data[account_header[0]]:
                pnl_data[account_header[0]][account_header[2]] = {
                    current_str: 0,
                    previous_str: 0,
                    per_change_str: 0,
                    three_month_avg_str: 0,
                    data_str: []
                }
            pnl_data[account_header[0]][account_header[2]][data_str].append(
                temporary_storage)

        else:
            pnl_data[account_header[0]].append(temporary_storage)

    # Changing sign for income
    for acc in pnl_data['income'][data_str]:
        acc[current_str] = -acc[current_str]
        acc[previous_str] = -acc[previous_str]
        acc[three_month_avg_str] = -acc[three_month_avg_str]

    # Calculating total income and costs of goods sold
    income_total, cogs_total = {
        current_str: 0,
        previous_str: 0,
        per_change_str: 0,
        three_month_avg_str: 0
    }, {
        current_str: 0,
        previous_str: 0,
        per_change_str: 0,
        three_month_avg_str: 0
    }

    for acc in pnl_data['income'][data_str]:
        pnl_data['income'][current_str] += acc[current_str]
        pnl_data['income'][previous_str] += acc[previous_str]
        pnl_data['income'][three_month_avg_str] += acc[three_month_avg_str]
    pnl_data['income'][per_change_str] = 0 if pnl_data['income'][previous_str] == 0 else round((
        pnl_data['income'][current_str]/pnl_data['income'][previous_str] - 1
    ) * 100)

    income_total[current_str] = pnl_data['income'][current_str]
    income_total[previous_str] = pnl_data['income'][previous_str]
    income_total[three_month_avg_str] = pnl_data['income'][three_month_avg_str]
    income_total[per_change_str] = pnl_data['income'][per_change_str]

    for k in (current_str, previous_str, per_change_str, three_month_avg_str):
        pnl_data['total_income'][k] = income_total[k]

    if pnl_data['cost_of_goods_sold']:
        pnl_data['cost_of_goods_sold'] = pnl_data['cost_of_goods_sold'][0]
        cogs_data = pnl_data['cost_of_goods_sold']
        cogs_total[current_str] = cogs_data[current_str]
        cogs_total[previous_str] = cogs_data[previous_str]
        cogs_total[three_month_avg_str] = cogs_data[three_month_avg_str]
        cogs_total[per_change_str] = 0 if cogs_total[previous_str] == 0 else round((
            cogs_total[current_str] / cogs_total[previous_str] - 1) * 100)
    else:
        pnl_data['cost_of_goods_sold'] = {
            current_str: 0,
            previous_str: 0,
            per_change_str: 0,
            three_month_avg_str: 0
        }

    # Calculating total expense for each category
    for category in pnl_data['expense']:
        cat_dic = pnl_data['expense'][category]
        for acc in cat_dic[data_str]:
            cat_dic[current_str] += acc[current_str]
            cat_dic[previous_str] += acc[previous_str]
            cat_dic[three_month_avg_str] += acc[three_month_avg_str]
        cat_dic[per_change_str] = 0 if cat_dic[previous_str] == 0 else round((
            cat_dic[current_str]/cat_dic[previous_str] - 1
        ) * 100)
        cat_dic['curr_per'] = 0 if income_total[current_str] == 0 else round(cat_dic[current_str] /
                                                                             income_total[current_str] * 100)
        cat_dic['prev_per'] = 0 if income_total[previous_str] == 0 else round(cat_dic[previous_str] /
                                                                              income_total[previous_str] * 100)

    # Calculating total expense
    expense_total = {
        current_str: 0,
        previous_str: 0,
        per_change_str: 0,
        three_month_avg_str: 0
    }

    for category in pnl_data['expense']:
        for acc in pnl_data['expense'][category][data_str]:
            expense_total[current_str] += acc[current_str]
            expense_total[previous_str] += acc[previous_str]
            expense_total[three_month_avg_str] += acc[three_month_avg_str]
    expense_total[per_change_str] = 0 if expense_total[previous_str] == 0 else round((
        expense_total[current_str] / expense_total[previous_str] - 1) * 100)

    for k in (current_str, previous_str, per_change_str, three_month_avg_str):
        pnl_data['total_expense'][k] = expense_total[k]

    # Calculating gross profit and EBITDA
    for k in (current_str, previous_str, three_month_avg_str):
        pnl_data['gross_profit'][k] = income_total[k] - cogs_total[k]
        pnl_data['ebitda'][k] = pnl_data['gross_profit'][k] - expense_total[k]
    pnl_data['gross_profit'][per_change_str] = 0 if pnl_data['gross_profit'][previous_str] == 0 else round(
        (pnl_data['gross_profit'][current_str]/pnl_data['gross_profit'][previous_str]-1)*100)
    pnl_data['ebitda'][per_change_str] = 0 if pnl_data['ebitda'][previous_str] == 0 else round(
        (pnl_data['ebitda'][current_str]/pnl_data['ebitda'][previous_str]-1)*100)

    # Calculating PBIT
    if pnl_data['depreciation_expenses']:
        pnl_data['depreciation_expenses'] = pnl_data['depreciation_expenses'][0]
    else:
        pnl_data['depreciation_expenses'] = {
            current_str: 0,
            previous_str: 0,
            per_change_str: 0,
            three_month_avg_str: 0
        }
    pnl_data['pbit'] = {
        current_str: pnl_data['ebitda'][current_str] - pnl_data['depreciation_expenses'][current_str],
        previous_str: pnl_data['ebitda'][previous_str] - pnl_data['depreciation_expenses'][previous_str],
        three_month_avg_str: pnl_data['ebitda'][three_month_avg_str] -
        pnl_data['depreciation_expenses'][three_month_avg_str]
    }
    pnl_data['pbit'][per_change_str] = 0 if pnl_data['pbit'][previous_str] == 0 else round(
        (pnl_data['pbit'][current_str]/pnl_data['pbit'][previous_str]-1)*100)

    # Calculating PBT
    if pnl_data['interest_expenses']:
        pnl_data['interest_expenses'] = pnl_data['interest_expenses'][0]
    else:
        pnl_data['interest_expenses'] = {
            current_str: 0,
            previous_str: 0,
            per_change_str: 0,
            three_month_avg_str: 0
        }
    pnl_data['pbt'] = {
        current_str: pnl_data['pbit'][current_str] - pnl_data['interest_expenses'][current_str],
        previous_str: pnl_data['pbit'][previous_str] - pnl_data['interest_expenses'][previous_str],
        three_month_avg_str: pnl_data['pbit'][three_month_avg_str] -
        pnl_data['interest_expenses'][three_month_avg_str]
    }
    pnl_data['pbt'][per_change_str] = 0 if pnl_data['pbt'][previous_str] == 0 else round(
        (pnl_data['pbt'][current_str]/pnl_data['pbt'][previous_str]-1)*100
    )

    for k in ('gross_profit', 'ebitda', 'depreciation_expenses', 'pbit', 'interest_expenses', 'pbt', 'total_expense'):
        pnl_data[k]['curr_per'] = 0 if income_total[current_str] == 0 else round(pnl_data[k][current_str] / \
            income_total[current_str] * 100)
        pnl_data[k]['prev_per'] = 0 if income_total[previous_str] == 0 else round(pnl_data[k][previous_str] / \
            income_total[previous_str] * 100)

    pnl_pbt = copy.deepcopy(pnl_data['pbt'])
    pnl_dep_exp = copy.deepcopy(pnl_data['depreciation_expenses'])

    return pnl_data, pnl_pbt, pnl_dep_exp


def get_balsheet(period, logged_client_id):
    if period is None:
        period = date(2022, 6, 30)
    elif not isinstance(period, date):
        period = datetime.strptime(period, '%Y-%m-%d').date()

    # Fetching accounts and transactions from database
    bal_accounts_data, transactions_data = accounts_util.fetch_data_from_db(
        'balsheet',
        logged_client_id,
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
            account.account_type, account.get_account_for_coding_display()
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

    prev_period = period.replace(day=1) + relativedelta(days=-1)
    pre_prev_period = prev_period.replace(day=1) + relativedelta(days=-1)

    # Filling up response with appropriate values
    for account_header in transactions_map:
        temporary_storage = {
            account_header_str: account_header[1],
            current_str: 0,
            previous_str: 0,
            pre_prev_str: 0,
            per_change_str: 0,
            three_month_avg_str: 0
        }

        for transaction in transactions_map[account_header]:
            credit_minus_debit = transaction.credit_amount - transaction.debit_amount
            temporary_storage[current_str] += credit_minus_debit
            if transaction.transaction_date <= prev_period:
                temporary_storage[previous_str] += credit_minus_debit
            if transaction.transaction_date <= pre_prev_period:
                temporary_storage[pre_prev_str] += credit_minus_debit

        temporary_storage[three_month_avg_str] += (
            temporary_storage[current_str] + temporary_storage[previous_str] + temporary_storage[pre_prev_str])/3

        if temporary_storage[previous_str] == 0:
            temporary_storage[per_change_str] = 0
        else:
            temporary_storage[per_change_str] = round((
                temporary_storage[current_str]/temporary_storage[previous_str] - 1) * 100)

        bal_sheet_data[account_header[0]].append(temporary_storage)

    bal_sheet_data['total_assets'] = {current_str: 0, previous_str: 0}
    for k in ('accounts_receivable', 'fixed_asset', 'other_asset', 'other_current_asset', 'stock', 'cash', 'bank'):
        for acc in bal_sheet_data[k]:
            acc[current_str] = -acc[current_str]
            acc[previous_str] = -acc[previous_str]
            bal_sheet_data['total_assets'][current_str] += acc[current_str]
            bal_sheet_data['total_assets'][previous_str] += acc[previous_str]
    bal_sheet_data['total_assets'][per_change_str] = round(
        (bal_sheet_data['total_assets'][current_str]/bal_sheet_data['total_assets'][previous_str]-1)*100)

    bal_sheet_data['total_liabilities'] = {current_str: 0, previous_str: 0}
    for k in ('accounts_payable', 'long_term_liability', 'other_current_liability', 'other_liability'):
        for acc in bal_sheet_data[k]:
            bal_sheet_data['total_liabilities'][current_str] += acc[current_str]
            bal_sheet_data['total_liabilities'][previous_str] += acc[previous_str]
    bal_sheet_data['total_liabilities'][per_change_str] = round(
        (bal_sheet_data['total_liabilities'][current_str]/bal_sheet_data['total_liabilities'][previous_str]-1)*100)

    bal_sheet_data['total_equity'] = {current_str: 0, previous_str: 0}
    for acc in bal_sheet_data['equity']:
        bal_sheet_data['total_equity'][current_str] = acc[current_str]
        bal_sheet_data['total_equity'][previous_str] = acc[previous_str]
    bal_sheet_data['total_equity'][per_change_str] = round(
        (bal_sheet_data['total_equity'][current_str]/bal_sheet_data['total_equity'][previous_str]-1)*100)

    return bal_sheet_data


def get_earnings(period, logged_client_id):
    if period is None:
        period = date(2022, 6, 30)
    elif not isinstance(period, date):
        period = datetime.strptime(period, '%Y-%m-%d').date()

    earnings_accounts_data = ZohoAccount.objects.filter(
        client_id=logged_client_id,
        account_type__in=('income', 'expense',
                          'other_expense', 'cost_of_goods_sold')
    ).values_list('account_id', 'account_type')

    transactions_related_to_earnings = ZohoTransaction.objects.filter(
        account_id__in=(tup[0] for tup in earnings_accounts_data)
    )

    accounts_map = {}
    for account in earnings_accounts_data:
        accounts_map[account[0]] = account[1]

    if period.month < 4:
        current_year_period = date(period.year-1, 4, 1)
    else:
        current_year_period = date(period.year, 4, 1)
    prev_period = period.replace(day=1) + relativedelta(days=-1)
    # pre_prev_period = prev_period.replace(day=1) + relativedelta(days=-1)

    cy_income, cy_cogs, cy_expenses = {current_str: 0, previous_str: 0}, {
        current_str: 0, previous_str: 0}, {current_str: 0, previous_str: 0}
    ret_income, ret_cogs, ret_expenses = {current_str: 0, previous_str: 0}, {
        current_str: 0, previous_str: 0}, {current_str: 0, previous_str: 0}
    for transaction in transactions_related_to_earnings:
        credit_minus_debit = transaction.credit_amount - transaction.debit_amount
        debit_minus_credit = transaction.debit_amount - transaction.credit_amount
        trans_date = transaction.transaction_date
        if trans_date >= current_year_period and trans_date <= period:
            if accounts_map[transaction.account_id] == 'income':
                cy_income[current_str] += credit_minus_debit
            if accounts_map[transaction.account_id] == 'cost_of_goods_sold':
                cy_cogs[current_str] += debit_minus_credit
            if accounts_map[transaction.account_id] in ('expense', 'other_expense'):
                cy_expenses[current_str] += debit_minus_credit
        if trans_date >= current_year_period and trans_date <= prev_period:
            if accounts_map[transaction.account_id] == 'income':
                cy_income[previous_str] += credit_minus_debit
            if accounts_map[transaction.account_id] == 'cost_of_goods_sold':
                cy_cogs[previous_str] += debit_minus_credit
            if accounts_map[transaction.account_id] in ('expense', 'other_expense'):
                cy_expenses[previous_str] += debit_minus_credit
        if trans_date < current_year_period:
            if accounts_map[transaction.account_id] == 'income':
                ret_income[current_str] += credit_minus_debit
            if accounts_map[transaction.account_id] == 'cost_of_goods_sold':
                ret_cogs[current_str] += debit_minus_credit
            if accounts_map[transaction.account_id] in ('expense', 'other_expense'):
                ret_expenses[current_str] += debit_minus_credit

    current_year_earnings = {
        current_str: cy_income[current_str]-cy_cogs[current_str]-cy_expenses[current_str],
        previous_str: cy_income[previous_str]-cy_cogs[previous_str]-cy_expenses[previous_str],
    }
    retained_earnings = {
        current_str: ret_income[current_str]-ret_cogs[current_str]-ret_expenses[current_str],
        previous_str: ret_income[current_str]-ret_cogs[current_str]-ret_expenses[current_str],
    }

    return current_year_earnings, retained_earnings


def get_cashflow(period, logged_client_id):

    cashflow_config_data = config_data['cashflow']

    # Fetching data related to cashflow accounts
    cashflow_accounts_data, transactions_data = accounts_util.fetch_data_from_db(
        'cashflow',
        logged_client_id,
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
            current_str: 0,
            previous_str: 0,
            pre_prev_str: 0
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

    prev_period = period.replace(day=1) + relativedelta(days=-1)
    pre_prev_period = prev_period.replace(day=1) + relativedelta(days=-1)

    for account_head in transactions_map:
        temporary_storage = {
            current_str: 0,
            previous_str: 0,
            pre_prev_str: 0,
        }

        for transaction in transactions_map[account_head]:
            credit_minus_debit = transaction.credit_amount - transaction.debit_amount
            temporary_storage[current_str] += credit_minus_debit
            if transaction.transaction_date <= prev_period:
                temporary_storage[previous_str] += credit_minus_debit
            if transaction.transaction_date <= pre_prev_period:
                temporary_storage[pre_prev_str] += credit_minus_debit

        if account_head[1] in assets_related_types:
            temporary_storage[current_str] = - temporary_storage[current_str]
            temporary_storage[previous_str] = - temporary_storage[previous_str]
            temporary_storage[pre_prev_str] = - temporary_storage[pre_prev_str]
        else:
            temporary_storage[current_str] = temporary_storage[current_str]
            temporary_storage[previous_str] = temporary_storage[previous_str]
            temporary_storage[pre_prev_str] = temporary_storage[pre_prev_str]

        cashflow_data_uncategorized[account_head[0]] = temporary_storage

    cashflow_from_operating_activities = 'cashflow_from_operating_activities'
    cashflow_from_investing_activities = 'cashflow_from_investing_activities'
    cashflow_from_financing_activities = 'cashflow_from_financing_activities'

    # Filling up response data with uncategorized and combined data
    temporary_storage = cashflow_data_uncategorized['bank_balance']
    temporary_storage2 = cashflow_data_uncategorized['cash_balance']
    cashflow_data['beginning_cash_balance'] = {
        current_str: temporary_storage[previous_str] + temporary_storage2[previous_str],
        previous_str: temporary_storage[pre_prev_str] + temporary_storage2[pre_prev_str],
        per_change_str: 0 if (temporary_storage[pre_prev_str] + temporary_storage2[pre_prev_str]) == 0 else round(
            ((temporary_storage[previous_str] + temporary_storage2[previous_str]) / (temporary_storage[pre_prev_str] + temporary_storage2[pre_prev_str])-1) * 100)
    }

    operating_activities_config_data = cashflow_config_data['cashflow_from_operating_activities']

    pnl_pbt, pnl_dep_exp = get_pnl(period, logged_client_id)[1:]

    for act, val in {'Net Income': pnl_pbt, 'Plus: Depreciation & Amortization': pnl_dep_exp}.items():
        cashflow_data[cashflow_from_operating_activities].append({
            activity_str: act,
            current_str: val[current_str],
            previous_str: val[previous_str],
            per_change_str: round(val[per_change_str])
        })

    temporary_storage = cashflow_data_uncategorized['accounts_receivable']
    cashflow_data[cashflow_from_operating_activities].append({
        activity_str: operating_activities_config_data['increase_decrease_sundry_debtors']['head'],
        current_str: temporary_storage[previous_str] - temporary_storage[current_str],
        previous_str: temporary_storage[pre_prev_str] - temporary_storage[previous_str],
        per_change_str: 0 if (temporary_storage[pre_prev_str] - temporary_storage[previous_str]) == 0 else round(
            ((temporary_storage[previous_str] - temporary_storage[current_str])/(temporary_storage[pre_prev_str] - temporary_storage[previous_str])-1) * 100)
    })

    temporary_storage = cashflow_data_uncategorized['other_current_assets']
    cashflow_data[cashflow_from_operating_activities].append({
        activity_str: operating_activities_config_data['increase_decrease_other_assets']['head'],
        current_str: temporary_storage[previous_str] - temporary_storage[current_str],
        previous_str: temporary_storage[pre_prev_str] - temporary_storage[previous_str],
        per_change_str: 0 if temporary_storage[pre_prev_str] - temporary_storage[previous_str] == 0 else round(
            ((temporary_storage[previous_str] - temporary_storage[current_str])/(temporary_storage[pre_prev_str] - temporary_storage[previous_str])-1)*100)
    })

    temporary_storage = cashflow_data_uncategorized['trade_payables']
    cashflow_data[cashflow_from_operating_activities].append({
        activity_str: operating_activities_config_data['increase_decrease_sundry_creditors']['head'],
        current_str: temporary_storage[current_str] - temporary_storage[previous_str],
        previous_str: temporary_storage[previous_str] - temporary_storage[pre_prev_str],
        per_change_str: 0 if temporary_storage[previous_str] - temporary_storage[pre_prev_str] == 0 else round(
            ((temporary_storage[current_str] - temporary_storage[previous_str])/(temporary_storage[previous_str] - temporary_storage[pre_prev_str]) - 1) * 100)
    })

    temporary_storage = cashflow_data_uncategorized['other_long_term_liabilities_and_provisions']
    temporary_storage2 = cashflow_data_uncategorized['other_liabilities']
    temporary_storage3 = cashflow_data_uncategorized['other_current_liabilities_and_provisions']
    a = temporary_storage[current_str] + temporary_storage2[current_str] + temporary_storage3[current_str] - \
        (temporary_storage[previous_str] +
         temporary_storage2[previous_str] + temporary_storage3[previous_str])
    b = temporary_storage[previous_str] + temporary_storage2[previous_str] + temporary_storage3[previous_str] - \
        (temporary_storage[pre_prev_str] +
         temporary_storage2[pre_prev_str] + temporary_storage3[pre_prev_str])
    cashflow_data[cashflow_from_operating_activities].append({
        activity_str: operating_activities_config_data['increase_decrease_other_liability']['head'],
        current_str: a,
        previous_str: b,
        per_change_str: 0 if b == 0 else round((a/b-1)*100)
    })

    for key in cashflow_data[cashflow_from_operating_activities]:
        cashflow_data['net_cash_a'][current_str] += key[current_str]
        cashflow_data['net_cash_a'][previous_str] += key[previous_str]
    cashflow_data['net_cash_a'][per_change_str] = 0 if cashflow_data['net_cash_a'][previous_str] == 0 else round(
        (cashflow_data['net_cash_a'][current_str]/cashflow_data['net_cash_a'][previous_str]-1)*100)

    investing_activities_config_data = cashflow_config_data['cashflow_from_investing_activities']

    temporary_storage = cashflow_data_uncategorized['tangible_assets']
    cashflow_data[cashflow_from_investing_activities].append({
        activity_str: investing_activities_config_data['investments_property_equipment']['head'],
        current_str: temporary_storage[previous_str] - temporary_storage[current_str],
        previous_str: temporary_storage[pre_prev_str] - temporary_storage[previous_str],
        per_change_str: 0 if (temporary_storage[pre_prev_str] - temporary_storage[previous_str]) == 0 else round(
            ((temporary_storage[previous_str] - temporary_storage[current_str])/(temporary_storage[pre_prev_str] - temporary_storage[previous_str])-1)*100)
    })

    temporary_storage = cashflow_data_uncategorized['other_non_current_assets']
    cashflow_data[cashflow_from_investing_activities].append({
        activity_str: investing_activities_config_data['purchase_sale_investments']['head'],
        current_str: temporary_storage[previous_str] - temporary_storage[current_str],
        previous_str: temporary_storage[pre_prev_str] - temporary_storage[previous_str],
        per_change_str: 0 if (temporary_storage[pre_prev_str] - temporary_storage[previous_str]) == 0 else round(
            ((temporary_storage[previous_str] - temporary_storage[current_str])/(temporary_storage[pre_prev_str] - temporary_storage[previous_str])-1)*100)
    })

    for key in cashflow_data[cashflow_from_investing_activities]:
        cashflow_data['net_cash_b'][current_str] += key[current_str]
        cashflow_data['net_cash_b'][previous_str] += key[previous_str]
    cashflow_data['net_cash_b'][per_change_str] = 0 if cashflow_data['net_cash_b'][previous_str] == 0 else round(
        (cashflow_data['net_cash_b'][current_str]/cashflow_data['net_cash_b'][previous_str]-1)*100)

    financing_activities_config_data = cashflow_config_data['cashflow_from_financing_activities']

    temporary_storage = cashflow_data_uncategorized['short_term_borrowings']
    temporary_storage2 = cashflow_data_uncategorized['long_term_borrowings']
    temporary_storage3 = cashflow_data_uncategorized['short_term_loans_and_advances']
    temporary_storage4 = cashflow_data_uncategorized['long_term_loans_and_advances']
    a = temporary_storage[current_str] + temporary_storage2[current_str] - temporary_storage[previous_str] - temporary_storage2[previous_str] + \
        temporary_storage3[previous_str] + temporary_storage4[previous_str] - \
        temporary_storage3[current_str] - temporary_storage4[current_str]
    b = temporary_storage[previous_str] + temporary_storage2[previous_str] - temporary_storage[pre_prev_str] - temporary_storage2[pre_prev_str] + \
        temporary_storage3[pre_prev_str] + temporary_storage4[pre_prev_str] - \
        temporary_storage3[previous_str] - temporary_storage4[previous_str]
    cashflow_data[cashflow_from_financing_activities].append({
        activity_str: financing_activities_config_data['issuance_of_debt']['head'],
        current_str: a,
        previous_str: b,
        per_change_str: 0 if b == 0 else round((a/b-1)*100)
    })

    temporary_storage = cashflow_data_uncategorized['share_capital']
    cashflow_data[cashflow_from_financing_activities].append({
        activity_str: financing_activities_config_data['issuance_of_equity']['head'],
        current_str: temporary_storage[current_str] - temporary_storage[previous_str],
        previous_str: temporary_storage[previous_str] - temporary_storage[pre_prev_str],
        per_change_str: 0 if temporary_storage[previous_str] - temporary_storage[pre_prev_str] == 0 else round(
            ((temporary_storage[current_str] - temporary_storage[previous_str])/(temporary_storage[previous_str] - temporary_storage[pre_prev_str])-1)*100)
    })

    for key in cashflow_data[cashflow_from_financing_activities]:
        cashflow_data['net_cash_c'][current_str] += key[current_str]
        cashflow_data['net_cash_c'][previous_str] += key[previous_str]
    cashflow_data['net_cash_c'][per_change_str] = 0 if cashflow_data['net_cash_c'][previous_str] == 0 else round(
        (cashflow_data['net_cash_c'][current_str]/cashflow_data['net_cash_c'][previous_str]-1)*100)

    for k in (current_str, previous_str):
        cashflow_data['net_change_abc'][k] = (
            cashflow_data['net_cash_a'][k] + cashflow_data['net_cash_b'][k] + cashflow_data['net_cash_c'][k])
    cashflow_data['net_change_abc'][per_change_str] = 0 if cashflow_data['net_change_abc'][previous_str] == 0 else round(
        (cashflow_data['net_change_abc'][current_str]/cashflow_data['net_change_abc'][previous_str]-1)*100)

    cashflow_data['ending_cash_balance'] = {
        current_str: cashflow_data['beginning_cash_balance'][current_str] + cashflow_data['net_change_abc'][current_str],
        previous_str: cashflow_data['beginning_cash_balance'][previous_str] +
        cashflow_data['net_change_abc'][previous_str]
    }
    cashflow_data['ending_cash_balance'][per_change_str] = 0 if cashflow_data['ending_cash_balance'][previous_str] == 0 else round(
        ((cashflow_data['ending_cash_balance'][current_str])/(cashflow_data['ending_cash_balance'][previous_str])-1)*100)

    return cashflow_data


def get_ratio_actions(period, client_id):
    ratio_actions = Ratio.objects.filter(
        client_id=client_id,
        period=period
    ).values_list('ratio_type', 'action_need_to_be_taken')

    ratios_dic = dict(ratio_actions)

    return ratios_dic


def get_ratios(period, logged_client_id):

    ratio_config_data = config_data['ratios_info']

    pnl_data = get_pnl(period, logged_client_id)[0]
    balsheet_data = get_balsheet(period, logged_client_id)
    cashflow_data = get_cashflow(period, logged_client_id)

    ratios_data = {}
    ratio_head, ratio_info, ideal_ratio, ratio_format = "ratio_head", "ratio_info", "ideal_ratio", "ratio_format"
    current, previous, three_month_avg = "current", "previous", "three_month_avg"
    action_str = "action_to_be_taken"

    gross_profit = pnl_data['gross_profit']
    ratios_data['gross_profit'] = {
        current: locale.format("%.2f", gross_profit[current], grouping=True),
        previous: locale.format("%.2f", gross_profit[previous], grouping=True),
        three_month_avg: locale.format(
            "%.2f", gross_profit[three_month_avg], grouping=True)
    }

    pbt = pnl_data['pbt']
    ratios_data['pbt'] = {
        current: locale.format("%.2f", pbt[current], grouping=True),
        previous: locale.format("%.2f", pbt[previous], grouping=True),
        three_month_avg:  locale.format(
            "%.2f", pbt[three_month_avg], grouping=True)
    }

    ratios_data['profit_ratios'] = []
    income = pnl_data['total_income']

    action = get_ratio_actions(period, logged_client_id)

    temporary_storage = {
        ratio_head: ratio_config_data['gross_profit_margin']['head'],
        ratio_info: ratio_config_data['gross_profit_margin']['info'],
        ideal_ratio: ratio_config_data['gross_profit_margin']['ideal'],
        action_str: action['gross_profit_margin'] if 'gross_profit_margin' in action else '',
        ratio_format: "%",
        current: 0 if income[current] == 0 else round(gross_profit[current]/income[current]*100),
        previous: 0 if income[previous] == 0 else round(gross_profit[previous]/income[previous]*100),
        three_month_avg: 0 if income[three_month_avg] == 0 else round(
            gross_profit[three_month_avg]/income[three_month_avg]*100)
    }
    ratios_data['profit_ratios'].append(temporary_storage)

    temporary_storage = {
        ratio_head: ratio_config_data['net_profit_margin']['head'],
        ratio_info: ratio_config_data['net_profit_margin']['info'],
        ideal_ratio: ratio_config_data['net_profit_margin']['ideal'],
        action_str: action['net_profit_margin'] if 'net_profit_margin' in action else '',
        ratio_format: "%",
        current: 0 if income[current] == 0 else round(pbt[current]/income[current]*100),
        previous: 0 if income[previous] == 0 else round(pbt[previous]/income[previous]*100),
        three_month_avg: 0 if income[three_month_avg] == 0 else round(
            pbt[three_month_avg]/income[three_month_avg]*100)
    }
    ratios_data['profit_ratios'].append(temporary_storage)

    if balsheet_data['equity']:
        equity = balsheet_data['equity'][0]
    else:
        equity = {
            "account_header": "Share Capital",
            "current": 0,
            "previous": 0,
            "pre_prev": 0,
            "per_change": 0,
            "three_month_avg": 0
        }

    temporary_storage = {
        ratio_head: ratio_config_data['return_on_equity']['head'],
        ratio_info: ratio_config_data['return_on_equity']['info'],
        ideal_ratio: ratio_config_data['return_on_equity']['ideal'],
        action_str: action['return_on_equity'] if 'return_on_equity' in action else '',
        ratio_format: "%",
        current: 0 if equity[current] == 0 else round(pbt[current]/equity[current]*100),
        previous: 0 if equity[previous] == 0 else round(pbt[previous]/equity[previous]*100),
        three_month_avg: 0 if equity[three_month_avg] == 0 else round(
            pbt[three_month_avg]/equity[three_month_avg]*100)
    }
    ratios_data['profit_ratios'].append(temporary_storage)

    cf_operations = cashflow_data['net_cash_a']
    temporary_storage = {
        ratio_head: ratio_config_data['cashflow_to_sales_ratio']['head'],
        ratio_info: ratio_config_data['cashflow_to_sales_ratio']['info'],
        ideal_ratio: ratio_config_data['cashflow_to_sales_ratio']['ideal'],
        action_str: action['cashflow_to_sales_ratio'] if 'cashflow_to_sales_ratio' in action else '',
        ratio_format: "%",
        current: 0 if income[current] == 0 else round(cf_operations[current]/income[current]*100),
        previous: 0 if income[previous] == 0 else round(cf_operations[previous]/income[previous]*100),
        three_month_avg: 0
    }
    ratios_data['profit_ratios'].append(temporary_storage)

    ratios_data['liquidity_ratio'] = []

    if balsheet_data['accounts_receivable']:
        accrec = balsheet_data['accounts_receivable'][0]
    else:
        accrec = {
            "account_header": "Accounts Receivable",
            "current": 0,
            "previous": 0,
            "pre_prev": 0,
            "per_change": 0,
            "three_month_avg": 0
        }

    if balsheet_data['cash']:
        cash = balsheet_data['cash'][0]
    else:
        cash = {
            "account_header": "Cash Balance",
            "current": 0,
            "previous": 0,
            "pre_prev": 0,
            "per_change": 0,
            "three_month_avg": 0
        }

    if balsheet_data['bank']:
        bank = balsheet_data['bank'][0]
    else:
        bank = {
            "account_header": "Bank Balance",
            "current": 0,
            "previous": 0,
            "pre_prev": 0,
            "per_change": 0,
            "three_month_avg": 0
        }

    if balsheet_data['other_current_asset']:
        ocurra = balsheet_data['other_current_asset'][0]
    else:
        ocurra = {
            "account_header": "Other Current Assets",
            "current": 0,
            "previous": 0,
            "pre_prev": 0,
            "per_change": 0,
            "three_month_avg": 0
        }

    if balsheet_data['accounts_payable']:
        accpay = balsheet_data['accounts_payable'][0]
    else:
        accpay = {
            "account_header": "Trade Payables",
            "current": 0,
            "previous": 0,
            "pre_prev": 0,
            "per_change": 0,
            "three_month_avg": 0
        }

    ocurrl = {current: 0, previous: 0, three_month_avg: 0}
    for account in balsheet_data['other_current_liability']:
        ocurrl[current] += account[current]
        ocurrl[previous] += account[previous]
        ocurrl[three_month_avg] += account[three_month_avg]

    temporary_storage = {
        ratio_head: ratio_config_data['working_capital_current_ratio']['head'],
        ratio_info: ratio_config_data['working_capital_current_ratio']['info'],
        ideal_ratio: ratio_config_data['working_capital_current_ratio']['ideal'],
        action_str: action['working_capital_current_ratio'] if 'working_capital_current_ratio' in action else '',
        ratio_format: "x",
        current: 0 if (accpay[current]+ocurrl[current]) == 0 else (accrec[current]+cash[current]+bank[current]+ocurra[current])/(accpay[current]+ocurrl[current]),
        previous: 0 if (accpay[previous]+ocurrl[previous]) == 0 else (accrec[previous]+cash[previous]+bank[previous]+ocurra[previous])/(accpay[previous]+ocurrl[previous]),
        three_month_avg: 0 if (accpay[three_month_avg]+ocurrl[three_month_avg]) == 0 else (accrec[three_month_avg] +
                                                                                           cash[three_month_avg]+bank[three_month_avg]+ocurra[three_month_avg])/(accpay[three_month_avg]+ocurrl[three_month_avg])
    }
    ratios_data['liquidity_ratio'].append(temporary_storage)

    for account in balsheet_data['other_current_liability']:
        if account['account_header'] == 'Short-term borrowings':
            st_borrow = copy.deepcopy(account)
            break
    else:
        st_borrow = {current: 0, previous: 0, three_month_avg: 0}
    for account in balsheet_data['long_term_liability']:
        if account['account_header'] == 'Long Term Borrowing':
            lt_borrow = copy.deepcopy(account)
            break
    else:
        lt_borrow = {current: 0, previous: 0, three_month_avg: 0}

    temporary_storage = {
        ratio_head: ratio_config_data['cashflow_to_debt_ratio']['head'],
        ratio_info: ratio_config_data['cashflow_to_debt_ratio']['info'],
        ideal_ratio: ratio_config_data['cashflow_to_debt_ratio']['ideal'],
        action_str: action['cashflow_to_debt_ratio'] if 'cashflow_to_debt_ratio' in action else '',
        ratio_format: "x",
        current: 0 if (st_borrow[current] + lt_borrow[current]) == 0 else cf_operations[current]/(st_borrow[current] + lt_borrow[current]),
        previous: 0 if (st_borrow[current] + lt_borrow[current]) == 0 else cf_operations[previous]/(st_borrow[previous] + lt_borrow[previous]),
        three_month_avg: 0
    }

    ratios_data['liquidity_ratio'].append(temporary_storage)

    ratios_data['op_eff_ratios'] = []

    if pnl_data['cost_of_goods_sold']:
        cogs = pnl_data['cost_of_goods_sold']
    else:
        cogs = {
            current: 0, previous: 0, 'pre_prev': 0, three_month_avg: 0
        }

    if balsheet_data['stock']:
        inventory = balsheet_data['stock']
    else:
        inventory = {
            current: 0, previous: 0, 'pre_prev': 0, three_month_avg: 0
        }

    temporary_storage = {
        ratio_head: ratio_config_data['inventory_turnover']['head'],
        ratio_info: ratio_config_data['inventory_turnover']['info'],
        ideal_ratio: ratio_config_data['inventory_turnover']['ideal'],
        action_str: action['inventory_turnover'] if 'inventory_turnover' in action else '',
        ratio_format: "x",
        current: 0 if (inventory[current] + inventory[previous]) == 0 else cogs[current]/(inventory[current] + inventory[previous]) * 2,
        previous: 0 if (inventory[previous] + inventory['pre_prev']) == 0 else cogs[previous]/(inventory[previous] + inventory['pre_prev']) * 2,
        three_month_avg: 0 if (
            inventory[three_month_avg]) == 0 else cogs[three_month_avg]/(inventory[three_month_avg])
    }
    ratios_data['op_eff_ratios'].append(temporary_storage)

    temporary_storage = {
        ratio_head: ratio_config_data['accounts_receivable_turnover']['head'],
        ratio_info: ratio_config_data['accounts_receivable_turnover']['info'],
        ideal_ratio: ratio_config_data['accounts_receivable_turnover']['ideal'],
        action_str: action['accounts_receivable_turnover'] if 'accounts_receivable_turnover' in action else '',
        ratio_format: "x",
        current: 0 if (accrec[current] + accrec[previous]) == 0 else income[current]/((accrec[current] + accrec[previous])/2),
        previous: 0 if (accrec[previous] + accrec['pre_prev']) == 0 else income[previous]/((accrec[previous] + accrec['pre_prev'])/2),
        three_month_avg: 0 if (accrec[three_month_avg]) == 0 else income[three_month_avg]/(accrec[three_month_avg]),
    }
    ratios_data['op_eff_ratios'].append(temporary_storage)

    temporary_storage = {
        ratio_head: ratio_config_data['days_payable_outstanding']['head'],
        ratio_info: ratio_config_data['days_payable_outstanding']['info'],
        ideal_ratio: ratio_config_data['days_payable_outstanding']['ideal'],
        action_str: action['days_payable_outstanding'] if 'days_payable_outstanding' in action else '',
        ratio_format: " days",
        current: 0 if cogs[current] == 0 else round((accpay[current] + accpay[previous])/(2*cogs[current])*365),
        previous: 0 if cogs[previous] == 0 else round((accpay[previous] + accpay['pre_prev'])/(2*cogs[previous])*365),
        three_month_avg: 0 if cogs[three_month_avg] == 0 else round((accpay[three_month_avg])/(cogs[three_month_avg])*365),
    }
    ratios_data['op_eff_ratios'].append(temporary_storage)

    ratios_data['solvency_ratios'] = []

    share_cap = equity
    temporary_storage = {
        ratio_head: ratio_config_data['debt_to_equity_ratio']['head'],
        ratio_info: ratio_config_data['debt_to_equity_ratio']['info'],
        ideal_ratio: ratio_config_data['debt_to_equity_ratio']['ideal'],
        action_str: action['debt_to_equity_ratio'] if 'debt_to_equity_ratio' in action else '',
        ratio_format: "x",
        current: 0 if share_cap[current] == 0 else (st_borrow[current] + lt_borrow[current])/share_cap[current],
        previous: 0 if share_cap[previous] == 0 else (st_borrow[previous] + lt_borrow[previous])/share_cap[previous],
        three_month_avg: 0 if share_cap[three_month_avg] == 0 else (
            st_borrow[three_month_avg] + lt_borrow[three_month_avg])/share_cap[three_month_avg]
    }
    ratios_data['solvency_ratios'].append(temporary_storage)

    mbr = {
        ratio_head: ratio_config_data['monthly_burn_rate']['head'],
        ratio_info: ratio_config_data['monthly_burn_rate']['info'],
        ideal_ratio: ratio_config_data['monthly_burn_rate']['ideal'],
        action_str: action['monthly_burn_rate'] if 'monthly_burn_rate' in action else '',
        ratio_format: "",
        current: cash[current] + bank[current] - cash[previous] - bank[previous],
        previous: cash[previous] + bank[previous] - cash['pre_prev'] - bank['pre_prev'],
        three_month_avg: cash[three_month_avg] + bank[three_month_avg]
    }
    ratios_data['solvency_ratios'].append(mbr)

    temporary_storage = {
        ratio_head: ratio_config_data['runway']['head'],
        ratio_info: ratio_config_data['runway']['info'],
        ideal_ratio: ratio_config_data['runway']['ideal'],
        action_str: action['runway'] if 'runway' in action else '',
        ratio_format: " months",
        current: 0 if mbr[current] == 0 else round((cash[current] + bank[current])/mbr[current]),
        previous: 0 if mbr[previous] == 0 else round((cash[previous] + bank[previous])/mbr[previous]),
        three_month_avg: 0 if mbr[three_month_avg] == 0 else round((cash[three_month_avg] + bank[three_month_avg])/mbr[three_month_avg]),
    }
    ratios_data['solvency_ratios'].append(temporary_storage)

    for obj in ratios_data:
        if type(ratios_data[obj]) == list:
            for ratio in ratios_data[obj]:
                ratio[current] = round(ratio[current], 2)
                ratio[previous] = round(ratio[previous], 2)
                ratio[three_month_avg] = round(ratio[three_month_avg], 2)

    mbr[current] = locale.format("%d", mbr[current], grouping=True)
    mbr[previous] = locale.format("%d", mbr[previous], grouping=True)
    mbr[three_month_avg] = locale.format(
        "%d", mbr[three_month_avg], grouping=True)

    return ratios_data
