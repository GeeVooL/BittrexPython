import requests
import datetime
import hmac
import hashlib

# ===============================================
# BITTREX API CONFIG
# ===============================================

# Bittrex API version string
API_VERSION = 'v1.1'

# Bittrex base URL string
BITTREX_BASEURL = 'https://bittrex.com/api/' + API_VERSION

# Bittrex public API base URL string
PUBLIC_BASEURL = BITTREX_BASEURL + '/public'

# Bittrex account API base URL string
ACCOUNT_BASEURL = BITTREX_BASEURL + '/account'

# Bittrex market API base URL string
MARKET_BASEURL = BITTREX_BASEURL + '/market'

# ===============================================

class Bittrex(object):
    """Handling REST API requests to Bittrex"""
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def make_auth_request(self, uri, params=None):
        """Make authorised request to Bittrex API
                
        Parameters:
        uri = full path to REST API,
        params (optional) = request parameters

        Return:
        requests response object
        """

        nonce = datetime.datetime.now().timestamp()
        base_params = {'apikey': self.api_key, 'nonce': nonce}
        api_sign = hmac.new(self.api_secret.encode(), uri.encode(), hashlib.sha512).hexdigest()
        header_data = {'apisign': api_sign}
        
        if params is not None:
            base_params.update(params)
        
        r = requests.get(uri, headers=header_data, params=base_params)
        r.raise_for_status()
        return r

    def make_request(self, uri, params=None):
        """Make unauthorised request to Bittrex API
        
        Parameters:
        uri = full path to REST API,
        params (optional) = request parameters

        Return:
        requests response object
        """

        r = requests.get(uri, params=params)
        r.raise_for_status()
        return r

    # PUBLIC REQUESTS
    def get_markets(self):
        """Used to get the open and available trading markets at Bittrex along with other meta data.
        
        Return:
        json structure
        """

        uri = PUBLIC_BASEURL + '/getmarkets'
        data = self.make_request(uri)
        return data.json()

    def get_currencies(self):
        """Used to get all supported currencies at Bittrex along with other meta data.
        
        Return:
        json structure
        """

        uri = PUBLIC_BASEURL + '/getcurrencies'
        data = self.make_request(uri)
        return data.json()
    
    def get_ticker(self, market):
        """Used to get the current tick values for a market.
        
        Parameters:
        market = market name string, ex. BTC-ETH
        
        Return:
        json structure
        """

        uri = PUBLIC_BASEURL + '/getticker'
        data = self.make_request(uri, params={'market': market})
        return data.json()
    
    def get_market_summaries(self):
        """Used to get the last 24 hour summary of all active exchanges.
        
        Return:
        json structure
        """

        uri = PUBLIC_BASEURL + '/getmarketsummaries'
        data = self.make_request(uri)
        return data.json()

    def get_market_summary(self, market):
        """Used to get the last 24 hour summary of all active exchanges.
        
        Parameters:
        market = market name string, ex. BTC-ETH
        
        Return:
        json structure
        """

        uri = PUBLIC_BASEURL + '/getmarketsummary'
        data = self.make_request(uri, params={'market': market})
        return data.json()

    def get_order_book(self, market, orderbook_type):
        """Used to get retrieve the orderbook for a given market.
        
        Parameters:
        market = market name string, ex. BTC-ETH,
        orderbook_type = "required buy", "sell" or "both" as orderbook type
        
        Return:
        json structure
        """

        uri = PUBLIC_BASEURL + '/getorderbook'
        data = self.make_request(uri, params={'market': market, 'type': orderbook_type})
        return data.json()
    
    def get_market_history(self, market):
        """Used to retrieve the latest trades that have occured for a specific market.
        
        Parameters:
        market = market name string, ex. BTC-ETH
        
        Return:
        json structure
        """

        uri = PUBLIC_BASEURL + '/getmarkethistory'
        data = self.make_request(uri, params={'market': market})
        return data.json()

    # ACCOUNT REQUESTS
    def get_balances(self):
        """Used to retrieve all balances from your account.
        
        Return:
        json structure
        """

        uri = ACCOUNT_BASEURL + '/getbalances'
        data = self.make_auth_request(uri)
        return data.json()

    def get_balance(self, currency):
        """Used to retrieve the balance from your account for a specific currency.
        
        Parameters:
        currency = currency name string, ex. "BTC"
        
        Return:
        json structure
        """

        uri = ACCOUNT_BASEURL + '/getbalance'
        data = self.make_auth_request(uri, params={'currency': currency})
        return data.json()

    def get_deposit_address(self, currency):
        """Used to retrieve or generate an address for a specific currency. If one does not exist, the call will fail and return ADDRESS_GENERATING until one is available.
        
        Parameters:
        currency = currency name string, ex. "BTC"
        
        Return:
        json structure
        """

        uri = ACCOUNT_BASEURL + '/getdepositaddress'
        data = self.make_auth_request(uri, params={'currency': currency})
        return data.json()

    def withdraw(self, currency, quantity, address, payment_id=None):
        """Used to withdraw funds from your account. note: please account for txfee.
        
        Parameters:
        currency = currency name string, ex. "BTC",
        quantity = quantity of coins to withdraw,
        address = address of destination wallet,
        payment_id (optional) = used for CryptoNotes/BitShareX/Nxt optional field (memo/paymentid)
        
        Return:
        json structure
        """

        uri = ACCOUNT_BASEURL + '/withdraw'
        parameters = {'currency': currency, 'quantity': quantity, 'address': address}
        if payment_id is not None:
            parameters['paymentid'] = payment_id
        data = self.make_auth_request(uri, params=parameters)
        return data.json()

    def get_order(self, uuid):
        """Used to retrieve a single order by uuid.
        
        Parameters:
        uuid = uuid string of a single order
        
        Return:
        json structure
        """

        uri = ACCOUNT_BASEURL + '/getorder'
        data = self.make_auth_request(uri, params={'uuid': uuid})
        return data.json()

    def get_order_history(self, market=None):
        """Used to retrieve your order history.
        
        Parameters:
        market (optional) = market name string, ex. BTC-ETH
        
        Return:
        json structure
        """

        uri = ACCOUNT_BASEURL + '/getorderhistory'
        if market is not None:
            data = self.make_auth_request(uri, params={'market': market})
        else:
            data = self.make_auth_request(uri)
        return data.json()
    
    def get_withdrawal_history(self, currency=None):
        """Used to retrieve your withdrawal history.
        
        Parameters:
        currency (optional) = currency name string, ex. "BTC"
        
        Return:
        json structure
        """

        uri = ACCOUNT_BASEURL + '/getwithdrawalhistory'
        if currency is not None:
            data = self.make_auth_request(uri, params={'currency': currency})
        else:
            data = self.make_auth_request(uri)
        return data.json()
    
    def get_deposit_history(self, currency=None):
        """Used to retrieve your deposit history.
        
        Parameters:
        currency (optional) = currency name string, ex. "BTC"
        
        Return:
        json structure
        """

        uri = ACCOUNT_BASEURL + '/getdeposithistory'
        if currency is not None:
            data = self.make_auth_request(uri, params={'currency': currency})
        else:
            data = self.make_auth_request(uri)
        return data.json()

    # MARKET REQUESTS
    def buy_limit(self, market, quantity, rate):
        """Used to place a buy order in a specific market. Use buylimit to place limit orders. Make sure you have the proper permissions set on your API keys for this call to work
        
        Parameters:
        market = market name string, ex. BTC-ETH,
        quantity = quantity of coins to withdraw,
        rate = the rate at which to place the order.
        
        Return:
        json structure
        """

        uri = ACCOUNT_BASEURL + '/buylimit'
        parameters = {'market': market,
                      'quantity': quantity,
                      'rate': rate}

        data = self.make_auth_request(uri, params=parameters)
        return data.json()
    
    def sell_limit(self, market, quantity, rate):
        """Used to place an sell order in a specific market. Use selllimit to place limit orders. Make sure you have the proper permissions set on your API keys for this call to work.
        
        Parameters:
        market = market name string, ex. BTC-ETH,
        quantity = quantity of coins to withdraw,
        rate = the rate at which to place the order.
        
        Return:
        json structure
        """

        uri = ACCOUNT_BASEURL + '/buylimit'
        parameters = {'market': market,
                      'quantity': quantity,
                      'rate': rate}

        data = self.make_auth_request(uri, params=parameters)
        return data.json()

    def cancel(self, uuid):
        """Used to cancel a buy or sell order.
        
        Parameters:
        uuid = uuid of buy or sell order
        
        Return:
        json structure
        """

        uri = ACCOUNT_BASEURL + '/cancel'
        data = self.make_auth_request(uri, params={'uuid': uuid})
        return data.json()

    def get_open_orders(self, market=None):
        """Get all orders that you currently have opened. A specific market can be requested.
        
        Parameters:
        market (optional) = market name string, ex. BTC-ETH
        
        Return:
        json structure
        """

        uri = ACCOUNT_BASEURL + '/getopenorders'
        if market is not None:
            data = self.make_auth_request(uri, params={'currency': market})
        else:
            data = self.make_auth_request(uri)
        return data.json()
