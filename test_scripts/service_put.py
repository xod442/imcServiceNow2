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

#PUT SERVICE NOW

#Need to install requests package for python
#sudo easy_install requests
import requests
 #Need to install requests package for python
 #sudo easy_install requests
 import requests

 # Set the request parameters
 url = 'https://https://dev30543.service-now.com/api/now/table/incident'
 user = 'admin'
 pwd = 'Grape123!'
 
 # Set proper headers
 headers = {"Content-Type":"application/json","Accept":"application/json"}

 # Do the HTTP request
 response = requests.post(url, auth=(user, pwd), headers=headers ,data='{"short_description":"Test"}')

 # Check for HTTP codes other than 200
 if response.status_code != 201:
     print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
     exit()

 # Decode the JSON response into a dictionary and use the data

 print('Status:',response.status_code,'Headers:',response.headers,'Response:',response.json())