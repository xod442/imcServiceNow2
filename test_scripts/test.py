#!/usr/bin/env python
'''
  2017 wookieware.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


__author__ = "@netwookie"
__copyright__ = "2017, wookieware.."
__credits__ = ["Rick Kauffman"]
__license__ = "Apache2"
__version__ = "1.0.0"
__maintainer__ = "Rick Kauffman"
__email__ = "rick@rickkauffman.com"
__status__ = "Prototype"

Functions to interact with Sevice Now and snowBridge local database
03212017 Initial release.


'''

import time
from flask import Flask, request, render_template, redirect, url_for, flash, session, send_file
from flask.ext.bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from models import db, Imc_alarm_ids, Elogfile
import json
import requests
from datetime import datetime
from pyhpeimc.auth import *
from pyhpeimc.plat.alarms import *
'''
alarm = {}
alarm['id'] = "221"
check = Imc_alarm_ids.query.filter_by(alarm_id=alarm['id']).all()
print check[0].alarm_id
print type(check[0])
'''
alarm = {}
alarm_id = '108'
auth = IMCAuth("http://", "10.132.0.15", "8080", "admin", "admin")
alarm_details = get_alarm_details(alarm_id, auth.creds, auth.url)
print alarm_details
print type(alarm_details)
print alarm_details['ackStatus']
if alarm_details['ackStatus'] == '1' and alarm_details['recStatus'] == "0": 
    print 'its char'
print type(alarm_details['ackStatus'])
print alarm_details['recStatus']
