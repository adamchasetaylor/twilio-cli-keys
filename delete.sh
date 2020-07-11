#!/bin/bash

# Based on Slack Conversation, to ensure the ENV variables are not being set
unset TWILIO_ACCOUNT_SID && unset TWILIO_API_KEY && unset TWILIO_API_SECRET

# Clear out the Twilio CLI hidden config for User
cd
rm -rf .twilio-cli

# Delete MacOS Keychain Entries for twilio-cli
while security delete-generic-password  -s 'twilio-cli' >/dev/null
do true; done