import requests
import datetime
import hmac
import hashlib

from config import *

class Bittrex(object):
    '''Handling REST API requests to Bittrex'''
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def make_auth_request(self, uri, params=None):
        # TODO: Change public requests to use make_request(...)
        nonce = datetime.datetime.now().timestamp()
        uri += '?apikey=%s&nonce=%s' % (self.api_key, nonce)
        api_sign = hmac.new(self.api_secret.encode(), uri.encode(), hashlib.sha512).hexdigest()
        header_data = {'apisign': api_sign}
        if params is not None:
            r = requests.get(uri, headers=header_data, params=params)
        else:    
            r = requests.get(uri, headers=header_data)
        r.raise_for_status()
        return r

    def make_request(self, uri, params=None):
        # TODO: Make public request without auth data
        pass

    @property
    def public(self):
        class Public(object): # self -> p_self
            def get_markets(p_self):
                '''Used to get the open and available trading markets at Bittrex along with other meta data.'''

                uri = PUBLIC_BASEURL + '/getmarkets'
                data = self.make_request(uri)
                return data.json()

            def get_currencies(p_self):
                '''Used to get all supported currencies at Bittrex along with other meta data.'''

                uri = PUBLIC_BASEURL + '/getcurrencies'
                data = self.make_request(uri)
                return data.json()
            
            def get_ticker(p_self, market):
                '''Used to get the current tick values for a market.
                Parameters:
                market = market name string, ex. "BTC-ETH"'''

                uri = PUBLIC_BASEURL + '/getticker'
                data = self.make_request(uri, params={'market': market})
                return data.json()
            
            def get_market_summaries(p_self):
                '''Used to get the last 24 hour summary of all active exchanges.'''

                uri = PUBLIC_BASEURL + '/getmarketsummaries'
                data = self.make_request(uri)
                return data.json()

            def get_market_summary(p_self, market):
                '''Used to get the last 24 hour summary of all active exchanges.
                Parameters:
                market = market name string, ex. "BTC-ETH"'''

                uri = PUBLIC_BASEURL + '/getmarketsummary'
                data = self.make_request(uri, params={'market': market})
                return data.json()

            def get_order_book(p_self, market, orderbook_type):
                '''Used to get retrieve the orderbook for a given market.
                Parameters:
                market = market name string, ex. "BTC-ETH",
                orderbook_type = "required buy", "sell" or "both" as orderbook type'''

                uri = PUBLIC_BASEURL + '/getorderbook'
                data = self.make_request(uri, params={'market': market, 'type': orderbook_type})
                return data.json()
            
            def get_market_history(p_self, market):
                '''Used to retrieve the latest trades that have occured for a specific market.
                Parameters:
                market = market name string, ex. "BTC-ETH"'''

                uri = PUBLIC_BASEURL + '/getmarkethistory'
                data = self.make_request(uri, params={'market': market})
                return data.json()

        return Public()
    
    @property
    def account(self):
        class Account(object): # self -> a_self
            def get_balances(a_self):
                '''Used to retrieve all balances from your account.'''

                uri = ACCOUNT_BASEURL + '/getbalances'
                data = self.make_request(uri)
                return data.json()

            def get_balance(a_self, currency):
                '''Used to retrieve the balance from your account for a specific currency.
                Parameters:
                currency = currency name string, ex. "BTC"'''

                uri = ACCOUNT_BASEURL + '/getbalance'
                data = self.make_request(uri, params={'currency': currency})
                return data.json()

            def get_deposit_address(a_self, currency):
                '''Used to retrieve or generate an address for a specific currency.
                If one does not exist, the call will fail and return ADDRESS_GENERATING until one is available.
                Parameters:
                currency = currency name string, ex. "BTC"'''

                uri = ACCOUNT_BASEURL + '/getdepositaddress'
                data = self.make_request(uri, params={'currency': currency})
                return data.json()

            def withdraw(a_self, currency, quantity, address, payment_id=None):
                '''Used to withdraw funds from your account. note: please account for txfee.
                Parameters:
                currency = currency name string, ex. "BTC",
                quantity = quantity of coins to withdraw,
                address = address of destination wallet,
                payment_id (optional) = used for CryptoNotes/BitShareX/Nxt optional field (memo/paymentid)'''

                uri = ACCOUNT_BASEURL + '/withdraw'
                parameters = {'currency': currency, 'quantity': quantity, 'address': address}
                if payment_id is not None:
                    parameters['paymentid'] = payment_id
                data = self.make_request(uri, params=parameters)
                return data.json()

            def get_order(a_self, uuid):
                '''Used to retrieve a single order by uuid.
                Parameters:
                uuid = uuid string of a single order'''

                uri = ACCOUNT_BASEURL + '/getorder'
                data = self.make_request(uri, params={'uuid': uuid})
                return data.json()

            def get_order_history(a_self, market=None):
                '''Used to retrieve your order history.
                Parameters:
                market (optional) = market name string, ex. "BTC-ETH"'''

                uri = ACCOUNT_BASEURL + '/getorderhistory'
                if market is not None:
                    data = self.make_request(uri, params={'market': market})
                else:
                    data = self.make_request(uri)
                return data.json()
            
            def get_withdrawal_history(a_self, currency=None):
                '''Used to retrieve your withdrawal history.
                Parameters:
                currency (optional) = currency name string, ex. "BTC"'''

                uri = ACCOUNT_BASEURL + '/getwithdrawalhistory'
                if currency is not None:
                    data = self.make_request(uri, params={'currency': currency})
                else:
                    data = self.make_request(uri)
                return data.json()
            
            def get_deposit_history(a_self, currency=None):
                '''Used to retrieve your deposit history.
                Parameters:
                currency (optional) = currency name string, ex. "BTC"'''

                uri = ACCOUNT_BASEURL + '/getdeposithistory'
                if currency is not None:
                    data = self.make_request(uri, params={'currency': currency})
                else:
                    data = self.make_request(uri)
                return data.json()

        return Account()
    
    @property
    def market(self):
        # TODO: Finish impelementation
        class Market(object): # self -> m_self
            def buy_limit(m_self, market, quantity, rate):
                pass
            
            def sell_limit(m_self, market, quantity, rate):
                pass

            def cancel(m_self, uuid):
                pass

            def get_open_orders()
        return Market()
