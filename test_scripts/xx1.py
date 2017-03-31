import time

import requests
from pyhpeimc.auth import *
from pyhpeimc.plat.alarms import *

imc_user = "admin"
imc_passwd = "admin"
imc_host = "10.132.0.15"
snow_user = "admin"
snow_passwd = "Grape123!"
instance = "dev30543"
snow_url = 'https://dev30543.service-now.com/api/now/table/incident'
varz = []
data = {}
dump = []
imc_test_url = 'http://'+imc_host+':8080'
# Configuring a connection to the VSD API


auth = IMCAuth("http://", imc_host, "8080", imc_user, imc_passwd)
#print auth
count = 1
# Get real time alarms from IMC
try:
    alarms = get_realtime_alarm('admin', auth.creds, auth.url)
    assert type(alarms) is list
except:
    print "IMc no"

for alarm in alarms:

    print alarm

    # Build dictionary for Service Now incedent report

    priority = alarm['severity']
    short_description = "Generated by HPE IMC Alarm ID %s Host IP:%s" % (alarm['id'],alarm['deviceDisplay'])
    description = alarm['faultDesc']
    # Now we have to ensure the strings are not unicode, service now will return 400 if they are
    priority = priority.encode('utf-8')
    short_description = short_description.encode('utf-8')
    description = description.encode('utf-8')
    print priority
    data['priority'] = priority
    data['number'] = "IMC0000-"+str(alarm['id'])
    data['short_description'] = short_description
    data['description'] = description
    data = str(data)
    #print data
    # Write record to Service Now
    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}
    print 'sending request'
    # Do the HTTP POST to Snow
    #response = requests.post(snow_url, auth=(snow_user, snow_passwd), headers=headers ,data=data)
    #count = count + 1
    # Check for HTTP codes other than 200
    #if response.status_code != 201:
        #varz = [response.status_code, response.headers, response.json, snow_url, snow_user,snow_passwd, data, count]
        #print varz
    #data = {}


print "finito!"