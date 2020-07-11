# twilio-cli-keys (macos)

Environment variables must be configured in your .env file.

TWILIO_ACCOUNT_SID=

TWILIO_AUTH_TOKEN=

TWILIO_CLI_CONFIG=

## Local Setup

cd twilio-cli-keys

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

## To Start from Scratch

./delete.sh (Be Careful here!)

./start.sh

## To Append Subaccounts

./start.sh
