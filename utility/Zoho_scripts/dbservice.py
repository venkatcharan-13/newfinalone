import psycopg2


class dbservice:
    def __init__(self):
        self.connector = None
        self.dbcursor = None
        self.connect_db()

    def connect_db(self):
        '''Connects to Postgresql Database'''
        self.connector = psycopg2.connect(
            database='Jordensky', user='postgres', password='postgres', host='127.0.0.1', port='5432')
        self.dbcursor = self.connector.cursor()

    def add_record(self, table_name, record_type, input_data):
        if 'documents' in input_data:
            del input_data['documents']

        keys = list(input_data.keys())

        table_data, table_values = '(', ' VALUES ('
        for i, x in enumerate(keys):
            if i != len(keys)-1:
                table_values += f'%({x})s, '
                table_data += f'{x}, '
            else:
                table_values += f'%({x})s)'
                table_data += f'{x})'

        if record_type == 'accounts':
            add_query = (f'INSERT INTO {table_name} ' + table_data + table_values +
                         f'ON CONFLICT(account_id) DO UPDATE SET current_balance = EXCLUDED.current_balance')
        else:
            add_query = (f'INSERT INTO {table_name} ' + table_data + table_values +
                         f'ON CONFLICT DO NOTHING')

        # Execute Query
        try:
            self.dbcursor.execute(add_query, input_data)
        except Exception as e:
            print(e)

        self.connector.commit()

    def get_zoho_creds(self, client_id):

        select_query = (
            f'SELECT zoho_organization_id, zoho_client_id, zoho_client_secret, zoho_refresh_token, zoho_domain from authentication_client where client_id={client_id}')
        try:
            self.dbcursor.execute(select_query)
            value_tup = self.dbcursor.fetchone()
        except Exception as e:
            print(e)
            
        key_tup = ('zoho_organization_id', 'zoho_client_id',
                   'zoho_client_secret', 'zoho_refresh_token', 'zoho_domain')
        result_dic = dict(zip(key_tup, value_tup))

        return result_dic
