'''
 Copyright 2016 Hewlett Packard Enterprise Development LP.
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
       http://www.apache.org/licenses/LICENSE-2.0
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
__author__ = "@netmanchris"
__copyright__ = "Copyright 2016, Hewlett Packard Enterprise Development LP."
__credits__ = ["Rick Kauffman"]
__license__ = "Apache2"
__version__ = "1.0.0"
__maintainer__ = "Rick Kauffman"
__email__ = "rick@rickkauffman.com"
__status__ = "Prototype"
'''

#GET SERVICE NOW
 #Need to install requests package for python
 #sudo easy_install requests

import requests
import json

# Set the request parameters
snow_url = 'https://dev30543.service-now.com/api/now/table/incident?sysparm_limit=100'
snoww_user = 'admin'
snow_passwd = 'Grape123!'

# Set proper headers
headers = {"Accept":"application/json"}

# Do the HTTP request
response = requests.get(url, auth=(user, pwd), headers=headers )

# Check for HTTP codes other than 200
if response.status_code != 200:
    print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
    exit()
# Decode the JSON response into a dictionary and use the data
#print('Status:',response.status_code,'Headers:',response.headers,'Response:',response.json())
#print('Cookies', response.cookies)
print type(response.text)
c = 0
data = json.loads(response.text)
print data['result'][0]['number']
print len(data['result'])
for i in data['result']:
    print data['result'][c]['number']
    c = c + 1

f = open ('/home/rick/projects/imcServiceNow/fields.text', 'w')
x = []
x = response.text.split(',')
print  type(x)
print  len(x)
cr = '\n'
print '------------------------------------------------------------'
#print x

for i in x:
   f.write(i)
   print i
   f.write(cr)
   print


f.close()
