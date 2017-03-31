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
alarm= {}
# Set the request parameters

snow_url = 'https://dev30543.service-now.com/api/now/table/incident'
snow_user = 'admin'
snow_passwd = 'Grape123!'
alarm['severity'] = "1"
alarm['id'] = "355"
alarm['deviceDisplay'] = "10.10.10.10"
alarm['faultDesc'] = 'Lightning hit it and it burned'


print snow_url
print snow_passwd
print snow_user
print alarm
# Get a single record from snow
snowObject = post_snow(alarm, snow_url, snow_user, snow_passwd)

print snowObject[0]
print snowObject[1]
print type(snowObject)
