import hashlib
import hmac
import json
import os
import requests
import time
import urllib

from cryptocoin_exchanges.exchange import Exchange


class YoBit(Exchange):
  
  _API_URL = 'https://yobit.net'
  _CREDENTIALS_PATH = os.path.join(
      os.path.expanduser('~'), 'credentials', 'yobit.json')
  _NAME = 'YoBit'

  def __init__(self):
    super(YoBit, self).__init__()
    credentials = self._loadCredentials()
    self._API_KEY = credentials['apikey']
    self._API_SECRET = credentials['secret']

  def getDepositAddress(self, coin):
    try:
      result = self._httpPost({
          'method': 'GetDepositAddress', 'coinName': coin, 'need_new': 0})
      if result['success'] and result['return']['address']:
        return result['return']['address']
    except ValueError as e:
      print 'Failed to retrieve %s data for %s' % (self._NAME, coin)

  def _getNonce(self):
    return int(time.time() * 1000000) - 1000000000000000

  def _httpGet(self, method, params):
    url = self._API_URL + '/api/3' + method
    if 'currency' in params:
      url += '/%s' % params['currency']
      del params['currency']
    req = requests.get(url + '?' urllib.urlencode(params))
    return json.loads(req.text)

  def _httpPost(self, params):
    url = self._API_URL + '/tapi'
    params['nonce'] = str(self._getNonce())
    signature = hmac.new(
        self._API_SECRET.encode('utf8'),
        urllib.urlencode(params).encode('utf-8'),
        hashlib.sha512).hexdigest()
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Key': self._API_KEY,
        'Sign': signature
    }
    req = requests.post(url, data=params, headers=headers)
    return json.loads(req.text)

  def _getInfo(self):
    return self._httpGet('/info', {})

  def _getTicker(self, currency):
    return self._httpGet('/ticker', {'currency': currency})

  def _getDepth(self, currency):
    return self._httpGet('/depth', {'currency': currency})

  def _getTrades(self, currency, limit=150):
    return self._httpGet(
        '/trades', {'currency': currency, 'limit': str(limit)})

  def _getFunds(self):
    # Really, their method should be called getFunds. Oh well.
    return self._httpPost({'method': 'getInfo'})

  def _trade(self, pair, ttype, rate, amount):
    return self._httpPost({
        'method': 'Trade',
        'pair': pair,
        'type': ttype,
        'rate': rate,
        'amount': amount,})

  def _getActiveOrders(self, pair):
    return self._httpPost({'method': 'ActiveOrders', 'pair': pair})

  def _getOrderInfo(self, order_id):
    return self._httpPost({'method': 'OrderInfo', 'order_id': order_id})

  def _cancelOrder(self, order_id):
    return self._httpPost({'method': 'CancelOrder', 'order_id': order_id})

  def _getTradeHistory(
      self, pair, from_n=0, count=1000, from_id=0, end_id='',
      order='DESC', since=0, end=''):
    return self._httpPost({
        'method': 'TradeHistory', 'from': from_n, 'count': count,
        'from_id': from_id, 'end_id': end_id, 'order': order,
        'since': since, 'end': end, 'pair': pair,})

  def _withdrawCoinsToAddress(self, coinname, amount, address):
    return self._httpPost({
        'method': 'WithdrawCoinsToAddress', 'coinName': coinname,
        'amount': amount, 'address': address,})
