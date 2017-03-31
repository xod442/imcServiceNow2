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
from snowbridge import *

# Set the request parameters
snow_number = 'IMC0000-354'
snow_url = 'https://dev30543.service-now.com/api/now/table/incident?number='+snow_number
snow_user = 'admin'
snow_passwd = 'Grape123!'


print snow_url
print snow_passwd
print snow_user
# Get a single record from snow
snowObject = get_snow(snow_url, snow_user, snow_passwd)

print snowObject['result'][0]['sys_id']
print type(snowObject)
