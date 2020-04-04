import datetime
import json

class TDAmeritradeAPIWrapper:
    def __init__(self, api_key, session, account_id=None):
        self.api_key = api_key
        self.session = session
        self.account_id = account_id

    def __account_id(self):
        if self.account_id is None:
            raise ValueError('client initialized without account ID')
        return self.account_id


    def __format_datetime(self, dt):
        '''Formats datetime objects appropriately, depending on whether they are 
        naive or timezone-aware'''
        tz_offset = dt.strftime('%z')
        tz_offset = tz_offset if tz_offset else '+0000'

        return dt.strftime('%Y-%m-%5T%H:%M:%S') + tz_offset


    def __get_request(self, path, params):
        dest = 'https://api.tdameritrade.com' + path
        resp = self.session.get(dest, params=params)
        return resp


    def __post_request(self, path, data):
        dest = 'https://api.tdameritrade.com' + path
        return self.session.post(dest, json=data)


    def __put_request(self, path, data):
        dest = 'https://api.tdameritrade.com' + path
        return self.session.put(dest, json=data)


    def __delete_request(self, path):
        dest = 'https://api.tdameritrade.com' + path
        return self.session.delete(dest)

    
    ############################################################################
    # Orders


    def cancel_order(self, order_id, account_id):
        'Cancel a specific order for a specific account.'
        path = '/v1/accounts/{}/orders/{}'.format(account_id, order_id)
        return self.__delete_request(path)


    def get_order(self, order_id, account_id):
        'Get a specific order for a specific account.'
        path = '/v1/accounts/{}/orders/{}'.format(account_id, order_id)
        return self.__get_request(path)


    def __make_order_query(self,
            max_results=None,
            from_entered_datetime=None,
            to_entered_datetime=None,
            status=None,
            statuses=None):
        if from_entered_datetime is None:
            from_entered_datetime = datetime.datetime.min
        if to_entered_datetime is None:
            to_entered_datetime = datetime.datetime.utcnow()

        params = {
            'fromEnteredTime': self.__format_datetime(from_entered_datetime),
            'toEnteredTime': self.__format_datetime(to_entered_datetime),
        }

        if max_results:
            params['maxResults'] = max_results

        if status is not None and statuses is not None:
            raise ValueError('at most one of status or statuses may be set')
        if status:
            params['status'] = status
        if statuses:
            params['status'] = ','.join(statuses)

        return params


    def get_orders_by_path(self,
            account_id,
            max_results=None,
            from_entered_datetime=None, 
            to_entered_datetime=None,
            status=None,
            statuses=None):
        'Orders for a specific account.'
        path = '/v1/accounts/{}/orders'.format(account_id)
        return self.__get_request(path, self.__make_order_query(
            max_results, from_entered_datetime, to_entered_datetime, status, 
            statuses))


    def get_orders_by_query(self,
            max_results=None,
            from_entered_datetime=None, 
            to_entered_datetime=None,
            status=None,
            statuses=None):
        'Orders for a specific account.'
        path = '/v1/orders'
        return self.__get_request(path, self.__make_order_query(
            max_results, from_entered_datetime, to_entered_datetime, status, 
            statuses))


    def place_order(self, account_id, order_spec):
        'Place an order for a specific account.'
        path = '/v1/accounts/{}/orders'.format(account_id)
        return self.__post_request(path, order_spec)


    def replace_order(self, account_id, order_id, order_spec):
        '''Replace an existing order for an account. The existing order will be 
        replaced by the new order. Once replaced, the old order will be canceled 
        and a new order will be created.'''
        path = '/v1/accounts/{}/orders/{}'.format(account_id, order_id)
        return self.__post_request(path, order_spec)


    ############################################################################
    # Saved Orders


    def create_saved_order(self, account_id, order_spec):
        'Save an order for a specific account.'
        path = '/v1/accounts/{}/savedorders'.format(account_id)
        return self.__post_request(path, order_spec)


    def delete_saved_order(self, account_id, order_id):
        'Delete a specific saved order for a specific account.'
        path = '/v1/accounts/{}/savedorders/{}'.format(account_id, order_id)
        return self.__delete_request(path)


    def get_saved_order(self, account_id, order_id):
        'Specific saved order by its ID, for a specific account.'
        path = '/v1/accounts/{}/savedorders/{}'.format(account_id, order_id)
        return self.__get_request(path, {})


    def get_saved_orders_by_path(self, account_id):
        'Saved orders for a specific account.'
        path = '/v1/accounts/{}/savedorders'.format(account_id)
        return self.__get_request(path, {})


    def replace_saved_order(self, account_id, order_id, order_spec):
        '''Replace an existing saved order for an account. The existing saved 
        order will be replaced by the new order.'''
        path = '/v1/accounts/{}/savedorders/{}'.format(account_id, order_id)
        return self.__put_request(path, order_spec)


    ############################################################################
    # Accounts


    def get_account(self, account_id, fields=None):
        'Account balances, positions, and orders for a specific account.'
        params = {}
        if fields:
            params['fields'] = ','.join(fields)

        path = '/v1/accounts/{}'.format(account_id)
        return self.__get_request(path, params)


    def get_accounts(self, fields=None):
        'Account balances, positions, and orders for a specific account.'
        params = {}
        if fields:
            params['fields'] = ','.join(fields)

        path = '/v1/accounts'
        return self.__get_request(path, params)
