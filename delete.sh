#!/bin/bash

cd
rm -rf .twilio-cli

while security delete-generic-password  -s 'twilio-cli' >/dev/null
do true; done