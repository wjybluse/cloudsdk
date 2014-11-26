__author__ = 'wan'
# AWS SigV2 signing tool
#
# This script allows you to manually sign HTTP query API requests to AWS
#
# Pass a url in quotes as an argument (with optional 'GET ' prepended, in
# case you are building and copying the request in a HTTP client, such as Paw).
#
# Note: For most services, you need to specify the API 'Version' date.
#
# USAGE:
# queryv2.py "https://iam.amazonaws.com/?Action=ListUsers&Version=2010-05-08"
# queryv2.py "GET https://ec2.amazonaws.com/?Action=DescribeRegions&Version=2013-10-15"
#
# The script assumes that you have the access_key and
# secret_key environment variables set to your AWS credentials.
# To set these up, see the following topics:
# Windows:
# http://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/InstallEC2CommandLineTools.html#set-aws-credentials
# Mac or Linux:
#       http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/SettingUp_CommandLine.html#setting_up_ec2_command_linux

import urllib
import datetime
import hmac
import hashlib
import base64
import urlparse
import requests

url = 'https://ec2.amazonaws.com?Action=DescribeInstances&Version=2013-10-15'

parsed_url = urlparse.urlparse(url)
query_params = urlparse.parse_qsl(parsed_url.query)

# Create timestamp for AUTHPARAMS
timestamp = datetime.datetime.utcnow().isoformat()

# Pull credentials from env vars
access_key = 'AKIAI3AIHM7BAUQAIETQ'
secret_key = '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'

# Set AUTHPARAMS
AUTHPARAMS = [
    ('AWSAccessKeyId', access_key),
    ('SignatureVersion', '2'),
    ('SignatureMethod', 'HmacSHA256'),
    ('Timestamp', timestamp)
]

# Combine query_params and AUTHPARAMS to the query list
query = query_params + AUTHPARAMS

# Sort the query params by key name
sorted_query = sorted(query)

# Urlencode the sorted query
query_string = urllib.urlencode(sorted_query)

# Replace '+' with '%20' in query string; the previous method replaces
# blank spaces with '+' symbols, and AWS expects '%20' instead.
query_string = query_string.replace('+', '%20')

# Create the canonical string for signing
string_to_sign = 'GET\n' + parsed_url.netloc + '\n' + '/\n' + query_string

# Create the signature from the string_to_sign and the secret_key
signature = hmac.new(
    key=secret_key,
    msg=string_to_sign,
    digestmod=hashlib.sha256).digest()

# Base 64 encode and urlencode the signature
signature = base64.encodestring(signature).strip()
urlencoded_signature = urllib.quote_plus(signature)

# Complete the request
signed_string = parsed_url.scheme + '://' + parsed_url.netloc + '?' + query_string + "&Signature=" + urlencoded_signature
# Send the request
r = requests.get(signed_string)

print "\nAWS SigV2 signing tool"

# Print the request and subsequent response
print "\nBEGIN REQUEST"
print "++++++++++++++++++++++++++++++++++++"
print signed_string

print "\nBEGIN RESPONSE"
print "++++++++++++++++++++++++++++++++++++"
print(r.text)