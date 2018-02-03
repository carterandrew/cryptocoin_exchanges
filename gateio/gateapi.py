from hashlib import sha512
import hmac
import httplib
import json
import os
import urllib

from cryptocoin_exchanges.exchange import Exchange


class GateIO(Exchange):

  _API_URL = 'data.gate.io'
  _CREDENTIALS_PATH = os.path.join(
      os.path.expanduser('~'), 'credentials', 'gateio.json')
  _NAME = 'Gate.io'

  def __init__(self):
    super(GateIO, self).__init__()
    credentials = self._loadCredentials()
    self._API_KEY = credentials['apikey']
    self._API_SECRET = credentials['secret']

  def getDepositAddress(self, coin):
    result = self.depositAddress(coin)
    if not result['addr'].startswith('New address is being generated'):
      return result['addr']

  def _getPairs(self):
    return self._httpGet('/api2/1/pairs')

  def _marketinfo(self):
    return self._httpGet('/api2/1/marketinfo')

  def _marketlist(self):
    return self._httpGet('/api2/1/marketlist')

  def _tickers(self):
    return self._httpGet('/api2/1/tickers')

  def _ticker(self, pair):
    return self._httpGet('/api2/1/ticker', pair)
  
  def _orderBooks(self):
    return self._httpGet('/api2/1/orderBooks')
  
  def _orderBook(self, pair):
    return self._httpGet('/api2/1/orderBook', pair)
  
  def _tradeHistory(self, pair, tradeId=None):
    params = '%s/%s' % (pair, tradeId) if tradeId else pair
    return self._httpGet('/api2/1/tradeHistory', params)
  
  def _balances(self):
    return self._httpPost('/api2/1/private/balances', {})
  
  def _depositAddress(self, currency):
    params = {'currency': currency}
    return self._httpPost('/api2/1/private/depositAddress', params)
  
  def _depositsWithdrawals(self, start_ts, end_ts):
    params = {'start': start_ts, 'end': end_ts}
    return self._httpPost('/api2/1/private/depositsWithdrawals', params)
  
  def _buy(self, pair, rate, amount):
    params = {'currencyPair': pair, 'rate': rate, 'amount': amount}
    return self._httpPost('/api2/1/private/buy', params)
  
  def _sell(self, pair, rate, amount):
    params = {'currencyPair': pair, 'rate': rate, 'amount': amount}
    return self._httpPost('/api2/1/private/sell', params)
  
  def _cancelOrder(self, order_number, pair):
    params = {'orderNumber': order_number, 'currencyPair': pair}
    return self._httpPost('/api2/1/private/cancelOrder', params)
  
  def _cancelAllOrders(self, order_type, pair):
    params = {'type': order_type, 'currencyPair': pair}
    return self._httpPost('/api2/1/private/cancelAllOrders', params)
  
  def _getOrder(self, order_number, pair):
    params = {'orderNumber': order_number, 'currencyPair': currency_pair}
    return self._httpPost('/api2/1/private/getOrder', params)
  
  def _openOrders(self):
    return self._httpPost('/api2/1/private/openOrders', {})
  
  def _myTradeHistory(self, pair, order_number=0):
    params = {'currencyPair': pair}
    if order_number:
      params['orderNumber'] = order_number
    return self._httpPost('/api2/1/private/tradeHistory', params)
  
  def _withdraw(self, currency, amount, address):
    params = {'currency': currency, 'amount': amount, 'address': address}
    return self._httpPost('/api2/1/private/withdraw', params)
    
  def _httpGet(self, resource, params=''):
    conn = httplib.HTTPSConnection(self._API_URL, timeout=10)
    conn.request('GET', resource + '/' + params)
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    return json.loads(data)

  def _httpPost(self, resource, params):
    headers = {
        'Content-type': 'application/x-www-form-urlencoded',
        'KEY': self._API_KEY,
        'SIGN': getSign(params, self._API_SECRET)
    }
    conn = httplib.HTTPSConnection(self._API_URL, timeout=10)
    conn.request('POST', resource, urllib.urlencode(params), headers)
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    conn.close()
    return json.loads(data)


def _getSign(params, secretKey):
  to_sign = urllib.urlencode(params).encode('utf8')
  return hmac.new(secretKey.encode('utf8'), to_sign, sha512).hexdigest()



