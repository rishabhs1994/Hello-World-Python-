from __future__ import division
from time import sleep
import json
import httplib2
from mailgun import *
from pagerduty import *
from urllib import urlencode
from httplib2 import Http
import json
import sys
import base64

h = Http()
h.add_credentials("Rishabh", "Rishabh")
url = 'http://localhost:5000/home'
req_per_minute = float(raw_input("Enter the number of requests per minute: "))
count_email = 1

interval = (60.0 / req_per_minute)
def SendRequests(url, req_per_minute):
	requests = 0 
	while requests < req_per_minute:
		resp, content = h.request(url,'GET')
		if resp['status'] != '200':
			print "Rate Limit reached"
			global count_email
			if(count_email == 1):
				count_email = 2
				send_simple_message()
				#notify_pagerduty()
				break
		else:
			print  "Number of Requests: ", requests+1 
			print resp
		requests = requests + 1 
		sleep(interval)

print "Sending Requests..."
SendRequests(url, req_per_minute)