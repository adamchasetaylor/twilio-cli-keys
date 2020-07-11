import os
import keyring
import getpass
import json
from twilio.rest import Client
from dotenv import load_dotenv
load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_CLI_CONFIG = os.getenv('TWILIO_CLI_CONFIG')

os.system('twilio profiles:list -l debug')

try:
  f = open(TWILIO_CLI_CONFIG)
except IOError:
  cli_config = { "email": {}, "prompts": {}, "projects": [], "activeProject": None}
else:
  with f:
    cli_config = json.load(f)

def updateConfig(cli_config,sid,friendly_name):
  new_profile = { "id": friendly_name, "accountSid": sid }
  cli_config['projects'].append(new_profile)
  print(cli_config)

def checkConfig(cli_config,sid):
  for project in cli_config['projects']:
    if project['accountSid'] == sid:
      return True
  return False

def checkConfigParent(cli_config,friendly_name):
  for project in cli_config['projects']:
    if project['id'] == friendly_name:
      return True
  return False


def createParentAuth(sid,friendly_name):
  if checkConfigParent(cli_config,friendly_name):
    print("Key Already Exists in Config")
  else:
    print("FRIENDLY_NAME",friendly_name)
    print("ACCOUNT_SID",sid)
    mykey = f"{TWILIO_ACCOUNT_SID}|{TWILIO_AUTH_TOKEN}"
    keyring.set_password("twilio-cli", friendly_name, mykey)
    updateConfig(cli_config,sid,friendly_name)

def createKey(myclient,sid,friendly_name):
  if checkConfig(cli_config,sid):
    print("Key Already Exists in Config")
  else:
    new_key = myclient.new_keys.create(friendly_name='twilio-cli-keys generated key')
    #myclient.keys(new_key.sid).delete()
    print("FRIENDLY_NAME",friendly_name)
    print("ACCOUNT_SID",sid)
    print("KEY",new_key.sid)
    print("SECRET",new_key.secret)
    mykey = f"{new_key.sid}|{new_key.secret}"
    keyring.set_password("twilio-cli", friendly_name, mykey)
    updateConfig(cli_config,sid,friendly_name)

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
accounts = client.api.accounts.list(status='active', limit=20)

for record in accounts:

  if TWILIO_ACCOUNT_SID == record.sid:
    friendly_name = record.friendly_name
    myclient = client
    parentaccount_name = f"{record.friendly_name} ACCOUNT/TOKEN"
    createParentAuth(record.sid,parentaccount_name)
  else:
    print("https://www.twilio.com/console/project/subaccounts")
    friendly_name = f"{record.friendly_name} SUBACCOUNT"
    token=getpass.getpass(f"enter token for \"{record.friendly_name}\":")
    myclient = Client(record.sid,token)

  createKey(myclient,record.sid,friendly_name)

  with open(TWILIO_CLI_CONFIG, 'w') as fp:
    json.dump(cli_config, fp)