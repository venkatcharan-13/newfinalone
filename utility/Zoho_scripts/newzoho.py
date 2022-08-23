import requests
import json


REDIRECT_URI = "http://www.zoho.in/books"
URL_FOR_GENERATING_REFRESH_TOKEN = "https://accounts.zoho.{}/oauth/v2/token?refresh_token={}&client_id={}&client_secret={}&redirect_uri={}&grant_type=refresh_token"
URL_FOR_ACCOUNTS = "https://books.zoho.{}/api/v3/chartofaccounts?organization_id={}&showbalance=true"
URL_FOR_TRANSACTIONS = "https://books.zoho.{}/api/v3/chartofaccounts/transactions?organization_id={}&page={}&per_page=200&account_id={}"


def generate_access_token(domain, refresh_token, zoho_client_id, zoho_client_secret):
    response_for_token = requests.post(URL_FOR_GENERATING_REFRESH_TOKEN.format(domain, refresh_token, zoho_client_id, zoho_client_secret, REDIRECT_URI))
    response_data = response_for_token.content
    access_token = json.loads(response_data)['access_token']
    return access_token

def request_for_accounts(domain, organization_id, auth_token):
    response_for_accounts = requests.get(URL_FOR_ACCOUNTS.format(domain, organization_id), headers={
        'Authorization': f'Zoho-oauthtoken {auth_token}'
    })
    accounts_data = response_for_accounts.content
    accounts_data = json.loads(accounts_data)['chartofaccounts']
    return accounts_data

def add_fetched_accounts_to_db(accounts_data, client_id, dbobj):
    for account in accounts_data:
        account['account_for_coding'] = ''
        account['client_id'] = client_id
        dbobj.add_record('accounts_zohoaccount', 'accounts', input_data=account)
    print('Accounts added')

def request_for_transactions(domain, accounts_data, organization_id, auth_token):
    account_ids_dict = {}
    for account in accounts_data:
        account_ids_dict[account['account_id']] = 0

    transactions_dict = {}
    cnt = 1
    for account_id in account_ids_dict:
        transaction_data, has_more_page, page = [], True, 1
        while has_more_page:
            response_for_transaction = requests.get(URL_FOR_TRANSACTIONS.format(domain, organization_id, page, account_id), headers={
                'Authorization': f'Zoho-oauthtoken {auth_token}'
            })
            transaction_response = response_for_transaction.content
            transactions = json.loads(transaction_response)['transactions']
            if transactions:
                transaction_data.extend(transactions)

            has_more_page = json.loads(transaction_response)['page_context']['has_more_page']
            page += 1
        transactions_dict[account_id] = transaction_data
        print(response_for_transaction.status_code, cnt, account_id)
        cnt += 1
    return transactions_dict


def add_fetched_transactions_to_db(transactions_dict, dbobj):
    for account_id in transactions_dict:
        if transactions_dict[account_id] == []:
            continue
        for transaction in transactions_dict[account_id]:
            if transaction['debit_amount'] == "":
                transaction['debit_amount'] = 0.0
            if transaction['credit_amount'] == "":
                transaction['credit_amount'] = 0.0

            dbobj.add_record('accounts_zohotransaction', 'transactions', input_data=transaction)
