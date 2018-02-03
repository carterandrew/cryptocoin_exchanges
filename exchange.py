"""A base Exchange class."""

import json
from abc import ABCMeta


class Exchange:
  __metaclass__ = ABCMeta

  _API_KEY = None
  _API_SECRET = None
  _API_URL = None
  _CREDENTIALS_PATH = None
  _NAME = None

  def _loadCredentials(self):
    """Loads API credentials from a json file.

    File format:
      {
        "apikey": "yourapikey",
        "secret": "yoursecretkey"
      }
    """
    with open(self._CREDENTIALS_PATH, 'r') as f:
      return json.loads(f.read())

  def name(self):
    return self._NAME

  def credentialsPath(self):
    return self._CREDENTIALS_PATH

  # Generally-public methods
  def getPairs(self):
    raise NotImplementedError()

  # Authenticated Methods
  def getBalances(self, pair=None):
    raise NotImplementedError()

  def getDepositAddress(self, coin):
    raise NotImplementedError()

  def getOrder(self, orderId):
    raise NotImplementedError()

  def cancelOrder(self, orderId, pair=None):
    raise NotImplementedError()

  def buyLimit(self, pair, amount, price):
    raise NotImplementedError()

  def sellLimit(self, pair, amount, price):
    raise NotImplementedError()
