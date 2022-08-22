import requests
import json
from utility.Zoho_scripts.dbservice import dbservice

db = dbservice()
creds = db.get_zoho_creds(2)
# to be stored with client
ORGANIZATION_ID = 60014631936
CLIENT_ID = 7 # to be captured from chosen client
ZOHO_CLIENT_ID = '1000.4MRW467CKK6O6JU5QMQQSDC4VVVJFL'
ZOHO_CLIENT_SECRET = '4ca8f47df3add19f6e78f70078964362413ca3fe9e'
REDIRECT_URI = "http://www.zoho.in/books"
REFRESH_TOKEN = '1000.6177255049d5494d6abf532f96ef676a.d59dd2cfc10ebbad54cd1a94dfa0484d'

# URLs defined for generating access token and fetching data
URL_FOR_GENERATING_REFRESH_TOKEN = "https://accounts.zoho.in/oauth/v2/token?refresh_token={}&client_id={}&client_secret={}&redirect_uri={}&grant_type=refresh_token"
URL_FOR_ACCOUNTS = "https://books.zoho.in/api/v3/chartofaccounts?organization_id={}&showbalance=true"
URL_FOR_TRANSACTIONS = "https://books.zoho.in/api/v3/chartofaccounts/transactions?organization_id={}&page={}&per_page=200&account_id={}"


def generate_access_token():
    response_for_token = requests.post(URL_FOR_GENERATING_REFRESH_TOKEN.format(REFRESH_TOKEN, ZOHO_CLIENT_ID, ZOHO_CLIENT_SECRET, REDIRECT_URI))
    response_data = response_for_token.content
    access_token = json.loads(response_data)['access_token']
    return access_token

def request_for_accounts(auth_token):
    response_for_accounts = requests.get(URL_FOR_ACCOUNTS.format(ORGANIZATION_ID), headers={
        'Authorization': f'Zoho-oauthtoken {auth_token}'
    })
    accounts_data = response_for_accounts.content
    accounts_data = json.loads(accounts_data)['chartofaccounts']
    return accounts_data

def request_for_transactions(accounts_data, auth_token):
    account_ids_dict = {}
    for account in accounts_data:
        account_ids_dict[account['account_id']] = account['parent_account_id']

    transactions_dict = {}
    cnt = 1
    for account_id in account_ids_dict:
        transaction_data, has_more_page, page = [], True, 1
        while has_more_page:
            response_for_transaction = requests.get(URL_FOR_TRANSACTIONS.format(ORGANIZATION_ID, page, account_id), headers={
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


def add_fetched_accounts_to_db(accounts_data):
    for account in accounts_data:
        account['account_for_coding'] = ''
        account['client_id'] = CLIENT_ID
        db.add_record('accounts_zohoaccount', input_data=account)
    print('Accounts added')


def add_fetched_transactions_to_db(transactions_dict):
    for account_id in transactions_dict:
        if transactions_dict[account_id] == []:
            continue
        for transaction in transactions_dict[account_id]:
            if transaction['debit_amount'] == "":
                transaction['debit_amount'] = 0.0
            if transaction['credit_amount'] == "":
                transaction['credit_amount'] = 0.0

            db.add_record('accounts_zohotransaction', input_data=transaction)

AUTH_TOKEN = generate_access_token()

# accounts_data = request_for_accounts(AUTH_TOKEN)
## Comment below part while fetching transactions
# add_fetched_accounts_to_db(accounts_data)

## Comment this part when fetching accounts
# transactions_dict = request_for_transactions(accounts_data, AUTH_TOKEN)
# add_fetched_transactions_to_db(transactions_dict)