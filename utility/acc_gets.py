import copy
from accounts.models import ZohoAccount, ZohoTransaction, Ratio
from accounts.models import account_for_coding_choice
from utility import accounts_util, jsonobj
from utility import accounts_str as strvar
from dateutil.relativedelta import relativedelta
from datetime import date, datetime
import locale
import json

locale.setlocale(locale.LC_ALL, 'en_IN.utf8')
account_header_str, account_for_coding_str, activity_str, data_str = "account_header", "account_for_coding", "activity", "data"
ratio_head, ratio_info, ideal_ratio, ratio_format = "ratio_head", "ratio_info", "ideal_ratio", "ratio_format"
action_str = "action_to_be_taken"
current_str = strvar.current
previous_str = strvar.previous
pre_prev_str = strvar.pre_previous
per_change_str = strvar.per_change
three_month_avg_str = strvar.three_month_avg


config_file = open("config/accounts_config.json")
config_data = json.load(config_file)
pnl_config_data = config_data['income_statement']
bs_config_data = config_data['balance_sheet']
cashflow_config_data = config_data['cashflow']
ratio_config_data = config_data['ratios']


def get_pnl(period, logged_client_id):

    # Fetching accounts and transactions from database
    pnl_accounts_data, transactions_data = accounts_util.fetch_data_from_db(
        'pnl',
        logged_client_id,
        period,
        pnl_config_data['related_accounts']
    )

    accounts_map, transactions_map = {}, {}

    # Generating accounts_map to map account IDs with their account_type and account_for_coding
    for account in pnl_accounts_data:
        acc_for_coding, acc_for_coding_display = account.account_for_coding, account.get_account_for_coding_display()
        acc_type = account.account_type

        if acc_for_coding == strvar.interest_expenses:
            accounts_map[account.account_id] = (
                acc_for_coding, acc_for_coding_display
            )
            continue

        if acc_for_coding == strvar.tax_expenses:
            accounts_map[account.account_id] = (
                acc_for_coding, acc_for_coding_display
            )
            continue

        if acc_type in (strvar.expense, strvar.other_expense):
            if acc_for_coding == strvar.depreciation_expenses:
                accounts_map[account.account_id] = (
                acc_type, acc_for_coding_display, acc_for_coding_display, acc_for_coding)
                continue
            accounts_map[account.account_id] = (
                strvar.expense, acc_for_coding_display, account.parent_account_name, account.account_for_coding)
        else:
            accounts_map[account.account_id] = (
                acc_type, acc_for_coding_display, acc_for_coding)

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
        if account_header[-1] in (strvar.direct_income, strvar.indirect_income):
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
    for acc in pnl_data[strvar.income][data_str]:
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

    for acc in pnl_data[strvar.income][data_str]:
        pnl_data[strvar.income][current_str] += acc[current_str]
        pnl_data[strvar.income][previous_str] += acc[previous_str]
        pnl_data[strvar.income][three_month_avg_str] += acc[three_month_avg_str]
    pnl_data[strvar.income][per_change_str] = 0 if pnl_data[strvar.income][previous_str] == 0 else round((
        pnl_data[strvar.income][current_str]/pnl_data[strvar.income][previous_str] - 1
    ) * 100)

    income_total[current_str] = pnl_data[strvar.income][current_str]
    income_total[previous_str] = pnl_data[strvar.income][previous_str]
    income_total[three_month_avg_str] = pnl_data[strvar.income][three_month_avg_str]
    income_total[per_change_str] = pnl_data[strvar.income][per_change_str]

    for k in (current_str, previous_str, per_change_str, three_month_avg_str):
        pnl_data['total_income'][k] = income_total[k]

    if pnl_data[strvar.cost_of_goods_sold]:
        pnl_data[strvar.cost_of_goods_sold] = pnl_data[strvar.cost_of_goods_sold][0]
        cogs_data = pnl_data[strvar.cost_of_goods_sold]
        cogs_total[current_str] = cogs_data[current_str]
        cogs_total[previous_str] = cogs_data[previous_str]
        cogs_total[three_month_avg_str] = cogs_data[three_month_avg_str]
        cogs_total[per_change_str] = 0 if cogs_total[previous_str] == 0 else round((
            cogs_total[current_str] / cogs_total[previous_str] - 1) * 100)
    else:
        pnl_data[strvar.cost_of_goods_sold] = {
            current_str: 0,
            previous_str: 0,
            per_change_str: 0,
            three_month_avg_str: 0
        }

    # Calculating total expense for each category
    for category in pnl_data[strvar.expense]:
        cat_dic = pnl_data[strvar.expense][category]
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

    for category in pnl_data[strvar.expense]:
        for acc in pnl_data[strvar.expense][category][data_str]:
            expense_total[current_str] += acc[current_str]
            expense_total[previous_str] += acc[previous_str]
            expense_total[three_month_avg_str] += acc[three_month_avg_str]
    expense_total[per_change_str] = 0 if expense_total[previous_str] == 0 else round((
        expense_total[current_str] / expense_total[previous_str] - 1) * 100)

    for k in (current_str, previous_str, per_change_str, three_month_avg_str):
        pnl_data['total_expense'][k] = expense_total[k]

    # Calculating gross profit and EBIT
    for k in (current_str, previous_str, three_month_avg_str):
        pnl_data['gross_profit'][k] = income_total[k] - cogs_total[k]
        pnl_data['ebit'][k] = pnl_data['gross_profit'][k] - expense_total[k]
    pnl_data['gross_profit'][per_change_str] = 0 if pnl_data['gross_profit'][previous_str] == 0 else round(
        (pnl_data['gross_profit'][current_str]/pnl_data['gross_profit'][previous_str]-1)*100)
    pnl_data['ebit'][per_change_str] = 0 if pnl_data['ebit'][previous_str] == 0 else round(
        (pnl_data['ebit'][current_str]/pnl_data['ebit'][previous_str]-1)*100)


    # Calculating PBT
    if pnl_data[strvar.interest_expenses]:
        pnl_data[strvar.interest_expenses] = pnl_data[strvar.interest_expenses][0]
    else:
        pnl_data[strvar.interest_expenses] = {
            current_str: 0,
            previous_str: 0,
            per_change_str: 0,
            three_month_avg_str: 0
        }
    
    if pnl_data[strvar.tax_expenses]:
        pnl_data[strvar.tax_expenses] = pnl_data[strvar.tax_expenses][0]
    else:
        pnl_data[strvar.tax_expenses] = {
            current_str: 0,
            previous_str: 0,
            per_change_str: 0,
            three_month_avg_str: 0
        }

    pnl_data['net_profit'] = {
        current_str: pnl_data['ebit'][current_str] - pnl_data[strvar.interest_expenses][current_str] - pnl_data[strvar.tax_expenses][current_str],
        previous_str: pnl_data['ebit'][previous_str] - pnl_data[strvar.interest_expenses][previous_str] - pnl_data[strvar.tax_expenses][previous_str],
        three_month_avg_str: pnl_data['ebit'][three_month_avg_str] -
        pnl_data[strvar.interest_expenses][three_month_avg_str] - pnl_data[strvar.tax_expenses][three_month_avg_str]
    }
    pnl_data['net_profit'][per_change_str] = 0 if pnl_data['net_profit'][previous_str] == 0 else round(
        (pnl_data['net_profit'][current_str]/pnl_data['net_profit'][previous_str]-1)*100
    )

    for k in ('gross_profit', 'ebit', strvar.tax_expenses, strvar.interest_expenses, 'net_profit', 'total_expense'):
        pnl_data[k]['curr_per'] = 0 if income_total[current_str] == 0 else round(pnl_data[k][current_str] / \
            income_total[current_str] * 100)
        pnl_data[k]['prev_per'] = 0 if income_total[previous_str] == 0 else round(pnl_data[k][previous_str] / \
            income_total[previous_str] * 100)

    pnl_pbt = copy.deepcopy(pnl_data['net_profit'])
    
    if 'Depreciation Expenses' in pnl_data[strvar.expense]:
        pnl_dep_exp = copy.deepcopy(pnl_data[strvar.expense]['Depreciation Expenses'])
    else:
        pnl_dep_exp = {
            current_str: 0,
            previous_str: 0,
            per_change_str: 0
        }

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
        bs_config_data['related_accounts']
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

        if account_header[0] in (strvar.accounts_payable, strvar.accounts_receivable, strvar.cash, strvar.bank):
            bal_sheet_data[account_header[0]].append(temporary_storage)
        else:
            bal_sheet_data[account_header[0]]['data'].append(temporary_storage)

    total_assets, total_liabilities, total_equity = "total_assets", "total_liabilities", "total_equity"
    current_total, previous_total = "current_total", "previous_total"
    overall_change = "overall_change"

    bal_sheet_data[total_assets] = {current_str: 0, previous_str: 0}
    for k in (strvar.fixed_asset, strvar.other_asset, strvar.other_current_asset, strvar.stock):
        for acc in bal_sheet_data[k]['data']:
            acc[current_str] = -acc[current_str]
            acc[previous_str] = -acc[previous_str]
            bal_sheet_data[k][current_total] += acc[current_str]
            bal_sheet_data[k][previous_total] += acc[previous_str]
            bal_sheet_data[total_assets][current_str] += acc[current_str]
            bal_sheet_data[total_assets][previous_str] += acc[previous_str]
        bal_sheet_data[k][overall_change] = 0 if bal_sheet_data[k][previous_total] == 0 else round(
            (bal_sheet_data[k][current_total]/bal_sheet_data[k][previous_total]-1)*100
        )
    bal_sheet_data[total_assets][per_change_str] = 0 if bal_sheet_data[total_assets][previous_str] == 0 else round(
        (bal_sheet_data[total_assets][current_str]/bal_sheet_data[total_assets][previous_str]-1)*100)

    for k in (strvar.accounts_receivable, strvar.cash, strvar.bank):
        for acc in bal_sheet_data[k]:
            acc[current_str] = -acc[current_str]
            acc[previous_str] = -acc[previous_str]
            bal_sheet_data[total_assets][current_str] += acc[current_str]
            bal_sheet_data[total_assets][previous_str] += acc[previous_str]
    bal_sheet_data[total_assets][per_change_str] = 0 if bal_sheet_data[total_assets][previous_str] == 0 else round(
        (bal_sheet_data[total_assets][current_str]/bal_sheet_data[total_assets][previous_str]-1)*100)

    bal_sheet_data[total_liabilities] = {current_str: 0, previous_str: 0}
    for k in (strvar.long_term_liability, strvar.other_current_liability, strvar.other_liability):
        for acc in bal_sheet_data[k]['data']:
            bal_sheet_data[k][current_total] += acc[current_str]
            bal_sheet_data[k][previous_total] += acc[previous_str]
            bal_sheet_data[total_liabilities][current_str] += acc[current_str]
            bal_sheet_data[total_liabilities][previous_str] += acc[previous_str]
        bal_sheet_data[k][overall_change] = 0 if bal_sheet_data[k][previous_total] == 0 else round(
            (bal_sheet_data[k][current_total]/bal_sheet_data[k][previous_total]-1)*100
        )
    bal_sheet_data[total_liabilities][per_change_str] = 0 if bal_sheet_data[total_liabilities][previous_str] == 0 else round(
        (bal_sheet_data[total_liabilities][current_str]/bal_sheet_data[total_liabilities][previous_str]-1)*100)
    
    for acc in bal_sheet_data[strvar.accounts_payable]:
            bal_sheet_data[total_liabilities][current_str] += acc[current_str]
            bal_sheet_data[total_liabilities][previous_str] += acc[previous_str]
    bal_sheet_data[total_liabilities][per_change_str] = 0 if bal_sheet_data[total_liabilities][previous_str] == 0 else round(
        (bal_sheet_data[total_liabilities][current_str]/bal_sheet_data[total_liabilities][previous_str]-1)*100)

    bal_sheet_data[total_equity] = {current_str: 0, previous_str: 0}
    for acc in bal_sheet_data[strvar.equity]['data']:
        bal_sheet_data[total_equity][current_str] += acc[current_str]
        bal_sheet_data[total_equity][previous_str] += acc[previous_str]
    bal_sheet_data[total_equity][per_change_str] = 0 if bal_sheet_data[total_equity][previous_str] == 0 else round(
        (bal_sheet_data[total_equity][current_str]/bal_sheet_data[total_equity][previous_str]-1)*100)

    return bal_sheet_data


def get_earnings(period, logged_client_id):
    if period is None:
        period = date(2022, 6, 30)
    elif not isinstance(period, date):
        period = datetime.strptime(period, '%Y-%m-%d').date()

    earnings_accounts_data = ZohoAccount.objects.filter(
        client_id=logged_client_id,
        account_type__in=(strvar.income, strvar.expense,
                          'other_expense', strvar.cost_of_goods_sold)
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
            if accounts_map[transaction.account_id] == strvar.income:
                cy_income[current_str] += credit_minus_debit
            if accounts_map[transaction.account_id] == strvar.cost_of_goods_sold:
                cy_cogs[current_str] += debit_minus_credit
            if accounts_map[transaction.account_id] in (strvar.expense, 'other_expense'):
                cy_expenses[current_str] += debit_minus_credit
        if trans_date >= current_year_period and trans_date <= prev_period:
            if accounts_map[transaction.account_id] == strvar.income:
                cy_income[previous_str] += credit_minus_debit
            if accounts_map[transaction.account_id] == strvar.cost_of_goods_sold:
                cy_cogs[previous_str] += debit_minus_credit
            if accounts_map[transaction.account_id] in (strvar.expense, 'other_expense'):
                cy_expenses[previous_str] += debit_minus_credit
        if trans_date < current_year_period:
            if accounts_map[transaction.account_id] == strvar.income:
                ret_income[current_str] += credit_minus_debit
            if accounts_map[transaction.account_id] == strvar.cost_of_goods_sold:
                ret_cogs[current_str] += debit_minus_credit
            if accounts_map[transaction.account_id] in (strvar.expense, 'other_expense'):
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

    # Fetching data related to cashflow accounts
    cashflow_accounts_data, transactions_data = accounts_util.fetch_data_from_db(
        'cashflow',
        logged_client_id,
        period,
        cashflow_config_data['related_accounts']
    )

    # Defining structure for API response
    cashflow_data = copy.deepcopy(jsonobj.json_structure['cashflow_data'])

    accounts_map, transactions_map = {}, {}
    cashflow_data_uncategorized = {}  # To store data related to all cashflow accounts
    assets_related_types = (
        strvar.fixed_asset, strvar.accounts_receivable, strvar.other_asset, strvar.bank,
        strvar.cash, strvar.other_current_asset, strvar.stock
    )

    for account in cashflow_config_data['related_accounts']:
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
    temporary_storage = cashflow_data_uncategorized[strvar.bank_balance]
    temporary_storage2 = cashflow_data_uncategorized[strvar.cash_balance]
    cashflow_data['beginning_cash_balance'] = {
        current_str: temporary_storage[previous_str] + temporary_storage2[previous_str],
        previous_str: temporary_storage[pre_prev_str] + temporary_storage2[pre_prev_str],
        per_change_str: 0 if (temporary_storage[pre_prev_str] + temporary_storage2[pre_prev_str]) == 0 else round(
            ((temporary_storage[previous_str] + temporary_storage2[previous_str]) / (temporary_storage[pre_prev_str] + temporary_storage2[pre_prev_str])-1) * 100)
    }

    operating_activities_config_data = cashflow_config_data['cashflow_from_operating_activities']

    pnl_pbt, pnl_dep_exp = get_pnl(period, logged_client_id)[1:]

    for act, val in {operating_activities_config_data['net_income']['head']: pnl_pbt, 
            operating_activities_config_data['depreciation_and_amortization']['head']: pnl_dep_exp}.items():
        cashflow_data[cashflow_from_operating_activities].append({
            activity_str: act,
            current_str: val[current_str],
            previous_str: val[previous_str],
            per_change_str: round(val[per_change_str])
        })

    temporary_storage = cashflow_data_uncategorized[strvar.accounts_receivable]
    cashflow_data[cashflow_from_operating_activities].append({
        activity_str: operating_activities_config_data['increase_decrease_sundry_debtors']['head'],
        current_str: temporary_storage[previous_str] - temporary_storage[current_str],
        previous_str: temporary_storage[pre_prev_str] - temporary_storage[previous_str],
        per_change_str: 0 if (temporary_storage[pre_prev_str] - temporary_storage[previous_str]) == 0 else round(
            ((temporary_storage[previous_str] - temporary_storage[current_str])/(temporary_storage[pre_prev_str] - temporary_storage[previous_str])-1) * 100)
    })

    temporary_storage = cashflow_data_uncategorized[strvar.other_current_assets]
    cashflow_data[cashflow_from_operating_activities].append({
        activity_str: operating_activities_config_data['increase_decrease_other_assets']['head'],
        current_str: temporary_storage[previous_str] - temporary_storage[current_str],
        previous_str: temporary_storage[pre_prev_str] - temporary_storage[previous_str],
        per_change_str: 0 if temporary_storage[pre_prev_str] - temporary_storage[previous_str] == 0 else round(
            ((temporary_storage[previous_str] - temporary_storage[current_str])/(temporary_storage[pre_prev_str] - temporary_storage[previous_str])-1)*100)
    })

    temporary_storage = cashflow_data_uncategorized[strvar.trade_payables]
    cashflow_data[cashflow_from_operating_activities].append({
        activity_str: operating_activities_config_data['increase_decrease_sundry_creditors']['head'],
        current_str: temporary_storage[current_str] - temporary_storage[previous_str],
        previous_str: temporary_storage[previous_str] - temporary_storage[pre_prev_str],
        per_change_str: 0 if temporary_storage[previous_str] - temporary_storage[pre_prev_str] == 0 else round(
            ((temporary_storage[current_str] - temporary_storage[previous_str])/(temporary_storage[previous_str] - temporary_storage[pre_prev_str]) - 1) * 100)
    })

    temporary_storage = cashflow_data_uncategorized[strvar.other_long_term_liabilities_and_provisions]
    temporary_storage2 = cashflow_data_uncategorized[strvar.other_liabilities]
    temporary_storage3 = cashflow_data_uncategorized[strvar.other_current_liabilities_and_provisions]
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

    temporary_storage = cashflow_data_uncategorized[strvar.tangible_assets]
    cashflow_data[cashflow_from_investing_activities].append({
        activity_str: investing_activities_config_data['investments_property_equipment']['head'],
        current_str: temporary_storage[previous_str] - temporary_storage[current_str],
        previous_str: temporary_storage[pre_prev_str] - temporary_storage[previous_str],
        per_change_str: 0 if (temporary_storage[pre_prev_str] - temporary_storage[previous_str]) == 0 else round(
            ((temporary_storage[previous_str] - temporary_storage[current_str])/(temporary_storage[pre_prev_str] - temporary_storage[previous_str])-1)*100)
    })

    temporary_storage = cashflow_data_uncategorized[strvar.other_non_current_assets]
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

    temporary_storage = cashflow_data_uncategorized[strvar.short_term_borrowings]
    temporary_storage2 = cashflow_data_uncategorized[strvar.long_term_borrowings]
    temporary_storage3 = cashflow_data_uncategorized[strvar.short_term_loans_and_advances]
    temporary_storage4 = cashflow_data_uncategorized[strvar.long_term_loans_and_advances]
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

    temporary_storage = cashflow_data_uncategorized[strvar.share_capital]
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

    pnl_data = get_pnl(period, logged_client_id)[0]
    balsheet_data = get_balsheet(period, logged_client_id)
    cashflow_data = get_cashflow(period, logged_client_id)

    ratios_data = {}

    gross_profit = pnl_data['gross_profit']
    ratios_data['gross_profit'] = {
        current_str: locale.format("%.2f", gross_profit[current_str], grouping=True),
        previous_str: locale.format("%.2f", gross_profit[previous_str], grouping=True),
        three_month_avg_str: locale.format(
            "%.2f", gross_profit[three_month_avg_str], grouping=True)
    }

    net_profit = pnl_data['net_profit']
    ratios_data['net_profit'] = {
        current_str: locale.format("%.2f", net_profit[current_str], grouping=True),
        previous_str: locale.format("%.2f", net_profit[previous_str], grouping=True),
        three_month_avg_str: locale.format(
            "%.2f", net_profit[three_month_avg_str], grouping=True)
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
        current_str: 0 if income[current_str] == 0 else round(gross_profit[current_str]/income[current_str]*100),
        previous_str: 0 if income[previous_str] == 0 else round(gross_profit[previous_str]/income[previous_str]*100),
        three_month_avg_str: 0 if income[three_month_avg_str] == 0 else round(
            gross_profit[three_month_avg_str]/income[three_month_avg_str]*100)
    }
    ratios_data['profit_ratios'].append(temporary_storage)

    temporary_storage = {
        ratio_head: ratio_config_data['net_profit_margin']['head'],
        ratio_info: ratio_config_data['net_profit_margin']['info'],
        ideal_ratio: ratio_config_data['net_profit_margin']['ideal'],
        action_str: action['net_profit_margin'] if 'net_profit_margin' in action else '',
        ratio_format: "%",
        current_str: 0 if income[current_str] == 0 else round(net_profit[current_str]/income[current_str]*100),
        previous_str: 0 if income[previous_str] == 0 else round(net_profit[previous_str]/income[previous_str]*100),
        three_month_avg_str: 0 if income[three_month_avg_str] == 0 else round(
            net_profit[three_month_avg_str]/income[three_month_avg_str]*100)
    }
    ratios_data['profit_ratios'].append(temporary_storage)

    if balsheet_data[strvar.equity]:
        for acc in balsheet_data[strvar.equity]['data']:
            if acc[account_header_str] == "Share Capital":
                equity = acc
                break
    else:
        equity = {
            account_header_str: "Share Capital",
            current_str: 0,
            previous_str: 0,
            pre_prev_str: 0,
            per_change_str: 0,
            three_month_avg_str: 0
        }

    temporary_storage = {
        ratio_head: ratio_config_data['return_on_equity']['head'],
        ratio_info: ratio_config_data['return_on_equity']['info'],
        ideal_ratio: ratio_config_data['return_on_equity']['ideal'],
        action_str: action['return_on_equity'] if 'return_on_equity' in action else '',
        ratio_format: "%",
        current_str: 0 if equity[current_str] == 0 else round(net_profit[current_str]/equity[current_str]*100),
        previous_str: 0 if equity[previous_str] == 0 else round(net_profit[previous_str]/equity[previous_str]*100),
        three_month_avg_str: 0 if equity[three_month_avg_str] == 0 else round(
            net_profit[three_month_avg_str]/equity[three_month_avg_str]*100)
    }
    ratios_data['profit_ratios'].append(temporary_storage)

    cf_operations = cashflow_data['net_cash_a']
    temporary_storage = {
        ratio_head: ratio_config_data['cashflow_to_sales_ratio']['head'],
        ratio_info: ratio_config_data['cashflow_to_sales_ratio']['info'],
        ideal_ratio: ratio_config_data['cashflow_to_sales_ratio']['ideal'],
        action_str: action['cashflow_to_sales_ratio'] if 'cashflow_to_sales_ratio' in action else '',
        ratio_format: "%",
        current_str: 0 if income[current_str] == 0 else round(cf_operations[current_str]/income[current_str]*100),
        previous_str: 0 if income[previous_str] == 0 else round(cf_operations[previous_str]/income[previous_str]*100),
        three_month_avg_str: 0
    }
    ratios_data['profit_ratios'].append(temporary_storage)

    ratios_data['liquidity_ratio'] = []

    if balsheet_data[strvar.accounts_receivable]:
        accrec = balsheet_data[strvar.accounts_receivable][0]
    else:
        accrec = {
            account_header_str: "Accounts Receivable",
            current_str: 0,
            previous_str: 0,
            pre_prev_str: 0,
            per_change_str: 0,
            three_month_avg_str: 0
        }

    if balsheet_data[strvar.cash]:
        cash = balsheet_data[strvar.cash][0]
    else:
        cash = {
            account_header_str: "Cash Balance",
            current_str: 0,
            previous_str: 0,
            pre_prev_str: 0,
            per_change_str: 0,
            three_month_avg_str: 0
        }

    if balsheet_data[strvar.bank]:
        bank = balsheet_data[strvar.bank][0]
    else:
        bank = {
            account_header_str: "Bank Balance",
            current_str: 0,
            previous_str: 0,
            pre_prev_str: 0,
            per_change_str: 0,
            three_month_avg_str: 0
        }

    ocurra = {current_str: 0, previous_str: 0, three_month_avg_str: 0}
    if balsheet_data[strvar.other_current_asset]:
        for account in balsheet_data[strvar.other_current_asset]['data']:
            ocurra[current_str] += account[current_str]
            ocurra[previous_str] += account[previous_str]
            ocurra[three_month_avg_str] += account[three_month_avg_str]

    if balsheet_data[strvar.accounts_payable]:
        accpay = balsheet_data[strvar.accounts_payable][0]
    else:
        accpay = {
            account_header_str: "Trade Payables",
            current_str: 0,
            previous_str: 0,
            pre_prev_str: 0,
            per_change_str: 0,
            three_month_avg_str: 0
        }

    ocurrl = {current_str: 0, previous_str: 0, three_month_avg_str: 0}
    for account in balsheet_data[strvar.other_current_liability]['data']:
        ocurrl[current_str] += account[current_str]
        ocurrl[previous_str] += account[previous_str]
        ocurrl[three_month_avg_str] += account[three_month_avg_str]

    temporary_storage = {
        ratio_head: ratio_config_data['working_capital_current_ratio']['head'],
        ratio_info: ratio_config_data['working_capital_current_ratio']['info'],
        ideal_ratio: ratio_config_data['working_capital_current_ratio']['ideal'],
        action_str: action['working_capital_current_ratio'] if 'working_capital_current_ratio' in action else '',
        ratio_format: "x",
        current_str: 0 if (accpay[current_str]+ocurrl[current_str]) == 0 else (accrec[current_str]+cash[current_str]+bank[current_str]+ocurra[current_str])/(accpay[current_str]+ocurrl[current_str]),
        previous_str: 0 if (accpay[previous_str]+ocurrl[previous_str]) == 0 else (accrec[previous_str]+cash[previous_str]+bank[previous_str]+ocurra[previous_str])/(accpay[previous_str]+ocurrl[previous_str]),
        three_month_avg_str: 0 if (accpay[three_month_avg_str]+ocurrl[three_month_avg_str]) == 0 else (accrec[three_month_avg_str] +
                                                                                           cash[three_month_avg_str]+bank[three_month_avg_str]+ocurra[three_month_avg_str])/(accpay[three_month_avg_str]+ocurrl[three_month_avg_str])
    }
    ratios_data['liquidity_ratio'].append(temporary_storage)

    for account in balsheet_data[strvar.other_current_liability]['data']:
        if account[account_header_str] == 'Short-term borrowings':
            st_borrow = copy.deepcopy(account)
            break
    else:
        st_borrow = {current_str: 0, previous_str: 0, three_month_avg_str: 0}
    for account in balsheet_data[strvar.long_term_liability]['data']:
        if account[account_header_str] == 'Long Term Borrowing':
            lt_borrow = copy.deepcopy(account)
            break
    else:
        lt_borrow = {current_str: 0, previous_str: 0, three_month_avg_str: 0}

    temporary_storage = {
        ratio_head: ratio_config_data['cashflow_to_debt_ratio']['head'],
        ratio_info: ratio_config_data['cashflow_to_debt_ratio']['info'],
        ideal_ratio: ratio_config_data['cashflow_to_debt_ratio']['ideal'],
        action_str: action['cashflow_to_debt_ratio'] if 'cashflow_to_debt_ratio' in action else '',
        ratio_format: "x",
        current_str: 0 if (st_borrow[current_str] + lt_borrow[current_str]) == 0 else cf_operations[current_str]/(st_borrow[current_str] + lt_borrow[current_str]),
        previous_str: 0 if (st_borrow[current_str] + lt_borrow[current_str]) == 0 else cf_operations[previous_str]/(st_borrow[previous_str] + lt_borrow[previous_str]),
        three_month_avg_str: 0
    }

    ratios_data['liquidity_ratio'].append(temporary_storage)

    ratios_data['op_eff_ratios'] = []

    if pnl_data[strvar.cost_of_goods_sold]:
        cogs = pnl_data[strvar.cost_of_goods_sold]
    else:
        cogs = {
            current_str: 0, previous_str: 0, pre_prev_str: 0, three_month_avg_str: 0
        }

    inventory = {current_str: 0, previous_str: 0, pre_prev_str: 0, three_month_avg_str: 0}
    if balsheet_data[strvar.stock]['data']:
        for acc in balsheet_data[strvar.stock]['data']:
            inventory[current_str] += acc[current_str]

        inventory = balsheet_data[strvar.stock]['data']
    else:
        inventory = {
            current_str: 0, previous_str: 0, pre_prev_str: 0, three_month_avg_str: 0
        }

    temporary_storage = {
        ratio_head: ratio_config_data['inventory_turnover']['head'],
        ratio_info: ratio_config_data['inventory_turnover']['info'],
        ideal_ratio: ratio_config_data['inventory_turnover']['ideal'],
        action_str: action['inventory_turnover'] if 'inventory_turnover' in action else '',
        ratio_format: "x",
        current_str: 0 if (inventory[current_str] + inventory[previous_str]) == 0 else cogs[current_str]/(inventory[current_str] + inventory[previous_str]) * 2,
        previous_str: 0 if (inventory[previous_str] + inventory[pre_prev_str]) == 0 else cogs[previous_str]/(inventory[previous_str] + inventory[pre_prev_str]) * 2,
        three_month_avg_str: 0 if (
            inventory[three_month_avg_str]) == 0 else cogs[three_month_avg_str]/(inventory[three_month_avg_str])
    }
    ratios_data['op_eff_ratios'].append(temporary_storage)

    temporary_storage = {
        ratio_head: ratio_config_data['accounts_receivable_turnover']['head'],
        ratio_info: ratio_config_data['accounts_receivable_turnover']['info'],
        ideal_ratio: ratio_config_data['accounts_receivable_turnover']['ideal'],
        action_str: action['accounts_receivable_turnover'] if 'accounts_receivable_turnover' in action else '',
        ratio_format: "x",
        current_str: 0 if (accrec[current_str] + accrec[previous_str]) == 0 else income[current_str]/((accrec[current_str] + accrec[previous_str])/2),
        previous_str: 0 if (accrec[previous_str] + accrec[pre_prev_str]) == 0 else income[previous_str]/((accrec[previous_str] + accrec[pre_prev_str])/2),
        three_month_avg_str: 0 if (accrec[three_month_avg_str]) == 0 else income[three_month_avg_str]/(accrec[three_month_avg_str]),
    }
    ratios_data['op_eff_ratios'].append(temporary_storage)

    temporary_storage = {
        ratio_head: ratio_config_data['days_payable_outstanding']['head'],
        ratio_info: ratio_config_data['days_payable_outstanding']['info'],
        ideal_ratio: ratio_config_data['days_payable_outstanding']['ideal'],
        action_str: action['days_payable_outstanding'] if 'days_payable_outstanding' in action else '',
        ratio_format: " days",
        current_str: 0 if cogs[current_str] == 0 else round((accpay[current_str] + accpay[previous_str])/(2*cogs[current_str])*365),
        previous_str: 0 if cogs[previous_str] == 0 else round((accpay[previous_str] + accpay[pre_prev_str])/(2*cogs[previous_str])*365),
        three_month_avg_str: 0 if cogs[three_month_avg_str] == 0 else round((accpay[three_month_avg_str])/(cogs[three_month_avg_str])*365),
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
        current_str: 0 if share_cap[current_str] == 0 else (st_borrow[current_str] + lt_borrow[current_str])/share_cap[current_str],
        previous_str: 0 if share_cap[previous_str] == 0 else (st_borrow[previous_str] + lt_borrow[previous_str])/share_cap[previous_str],
        three_month_avg_str: 0 if share_cap[three_month_avg_str] == 0 else (
            st_borrow[three_month_avg_str] + lt_borrow[three_month_avg_str])/share_cap[three_month_avg_str]
    }
    ratios_data['solvency_ratios'].append(temporary_storage)

    mbr = {
        ratio_head: ratio_config_data['monthly_burn_rate']['head'],
        ratio_info: ratio_config_data['monthly_burn_rate']['info'],
        ideal_ratio: ratio_config_data['monthly_burn_rate']['ideal'],
        action_str: action['monthly_burn_rate'] if 'monthly_burn_rate' in action else '',
        ratio_format: "",
        current_str: cash[current_str] + bank[current_str] - cash[previous_str] - bank[previous_str],
        previous_str: cash[previous_str] + bank[previous_str] - cash[pre_prev_str] - bank[pre_prev_str],
        three_month_avg_str: cash[three_month_avg_str] + bank[three_month_avg_str]
    }
    ratios_data['solvency_ratios'].append(mbr)

    temporary_storage = {
        ratio_head: ratio_config_data['runway']['head'],
        ratio_info: ratio_config_data['runway']['info'],
        ideal_ratio: ratio_config_data['runway']['ideal'],
        action_str: action['runway'] if 'runway' in action else '',
        ratio_format: " months",
        current_str: 0 if mbr[current_str] == 0 else round((cash[current_str] + bank[current_str])/mbr[current_str]),
        previous_str: 0 if mbr[previous_str] == 0 else round((cash[previous_str] + bank[previous_str])/mbr[previous_str]),
        three_month_avg_str: 0 if mbr[three_month_avg_str] == 0 else round((cash[three_month_avg_str] + bank[three_month_avg_str])/mbr[three_month_avg_str]),
    }
    ratios_data['solvency_ratios'].append(temporary_storage)

    for obj in ratios_data:
        if type(ratios_data[obj]) == list:
            for ratio in ratios_data[obj]:
                ratio[current_str] = round(ratio[current_str], 2)
                ratio[previous_str] = round(ratio[previous_str], 2)
                ratio[three_month_avg_str] = round(ratio[three_month_avg_str], 2)

    mbr[current_str] = locale.format("%d", mbr[current_str], grouping=True)
    mbr[previous_str] = locale.format("%d", mbr[previous_str], grouping=True)
    mbr[three_month_avg_str] = locale.format(
        "%d", mbr[three_month_avg_str], grouping=True)

    return ratios_data
