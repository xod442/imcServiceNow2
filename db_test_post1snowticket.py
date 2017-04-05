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
device= {}
# Set the request parameters

snow_url = 'https://dev32384.service-now.com/api/now/table/u_imcdevices'
snow_user = 'admin'
snow_passwd = 'Grape123!'
device['id'] = "1"
device['sysOid'] = '1.4.3.2.5.6.7.8.5555.44.35.22.1'
device['label'] = 'riock'
device['ip'] = '10.10.10.1u'
device['mask'] = '255.255.255.0'
device['contact'] = 'rick'
device['location'] = 'MyLab'
device['typeName'] = 'FlexFabric'


print snow_url
print snow_passwd
print snow_user
print device
# Get a single record from snow
snowObject = load_snow(device, snow_url, snow_user, snow_passwd)

print snowObject
print type(snowObject)
