"""Library for sending email via smtp interface."""
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
import json
import getpass
import os
 

_CREDENTIALS_PATH = os.path.expanduser('~') + '/credentials/smtp.json'


def _loadCredentials():
  """Loads stmp credentials from a json file.

  File format:
    {
      "hostname": "smtp.gmail.com",
      "port": 587,
      "user": "gmail address",
      "password": "gmail password"
    }
  """
  with open(_CREDENTIALS_PATH, 'r') as f:
    return json.loads(f.read())


class Email(object):

  def __init__(self):
    self._credentials = _loadCredentials()

  def send(self, subject, body, to_addr, from_addr=None):
    credentials = self._credentials
    msg = MIMEMultipart()

    msg['From'] = from_addr if from_addr else credentials['user']
    msg['To'] = to_addr
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(credentials['hostname'], credentials['port'])
    server.starttls()
    server.login(credentials['user'], credentials['password'])
    server.sendmail(credentials['user'], to, msg.as_string())
    server.quit()
