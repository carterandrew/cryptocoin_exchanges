from decimal import *
import getpass
import json
import requests
import time
import uuid

from cryptocoin_exchanges.exchange import Exchange


class HitBTC(Exchange):

  _API_URL = 'https://api.hitbtc.com/api/2/'
  _CREDENTIALS_PATH = os.path.join(
      os.path.expanduser('~'), 'credentials', 'hitbtc.json')
  _NAME = 'HitBTC'

  def __init__(self):
    super(HitBTC, self).__init__()
    credentials = self._loadCredentials()
    self._API_KEY = credentials['apikey']
    self._API_SECRET = credentials['secret']
    self._session = requests.session()
    self._session.auth = (self._API_KEY, self._API_SECRET)

  def getDepositAddress(self, coin):
    result = self._getAddress(coin)
    if 'address' in result:
      return result['address']

  def _getSymbol(self, symbol_code):
    return self._sessionGet('public/symbol/%s' % symbol_code)

  def _getOrderbook(self, symbol_code):
    return self._sessionGet('public/orderbook/%s' % symbol_code)

  def _getAddress(self, currency_code):
    return self._sessionGet('account/crypto/address/%s' % currency_code)

  def _getAccountBalance(self):
    return self._sessionGet('account/balance')

  def _getTradingBalance(self):
    return self._sessionGet('trading/balance')

  def _transfer(self, currency_code, amount, to_exchange):
    params = {
        'currency': currency_code, 'amount': amount,
        'type': 'bankToExchange' if to_exchange else 'exchangeToBank',
    }
    return self._sessionPost('account/transfer', params)

  def _newOrder(self, client_order_id, symbol_code, side, quantity, price=None):
    params = {
        'symbol': symbol_code, 'side': side, 'quantity': quantity,
    }
    if price:
      params['price'] = price
    return self._sessionPut('order/%s' % client_order_id, params)

  def _getOrder(self, client_order_id, wait=None):
    params = {'wait': wait} if wait else {}
    return self._sessionGet('order/%s' % client_order_id, params)

  def _cancelOrder(self, client_order_id):
    return self._sessionDelete('order/%s' % client_order_id)

  def _withdraw(self, currency_code, amount, address, network_fee=None):
    params = {
        'currency': currency_code, 'amount': amount, 'address': address,
    }
    if network_fee:
      params['networkfee'] = network_fee
    return self._sessionPost('account/crypto/withdraw'_

  def _getTransaction(self, transaction_id):
    return self._sessionGet('account/transactions/%s' % transaction_id)

  def _sessionDelete(self, resource, params=None):
    return self._session.delete(self._API_URL + resource, data=params).json()

  def _sessionGet(self, resource, params=None):
    return self._session.get(self._API_URL + resource, params=params).json()

  def _sessionPost(self, resource, params):
    return self._session.post(self._API_URL + resource, data=params).json()

  def _sessionPut(self, resource, params):
    return self._session.put(self._API_URL + resource, data=params).json()
