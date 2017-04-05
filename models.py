
'''
 Copyright 2016 wookieware.

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
__copyright__ = "Copyright 2016, wookieware."
__credits__ = ["Rick Kauffman"]
__license__ = "Apache2"
__version__ = "1.0.0"
__maintainer__ = "Rick Kauffman"
__email__ = "rick@rickkauffman.com"
__status__ = "Prototype"

Script builds database for switchdb

'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import APP_ROOT
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+os.path.join(APP_ROOT,'imcServiceNow.db')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Logfile table
class Imc_alarm_ids(db.Model):
    alarm_id = db.Column(db.Integer,primary_key=True)
    snow_return = db.Column(db.String(6))
    faultDesc = db.Column(db.String(150))
    deviceDisplay = db.Column(db.String(15))
    severity = db.Column(db.String(2))
    faultTime = db.Column(db.String(15))
    userAckUserName = db.Column(db.String(25))
    userAckType = db.Column(db.String(2))
    snow_number = db.Column(db.String(20))


    def __init__(self,
                alarm_id,
                snow_return,
                faultDesc,
                deviceDisplay,
                severity,
                faultTime,
                userAckUserName,
                userAckType,
                snow_number):

        self.alarm_id = alarm_id
        self.snow_return = snow_return
        self.faultDesc = faultDesc
        self.deviceDisplay = deviceDisplay
        self.severity = severity
        self.faultTime = faultTime
        self.userAckUserName = userAckUserName
        self.userAckType = userAckType
        self.snow_number = snow_number


    def __repr__(self):
        return '<Imc_alarm_ids %r>' % self.alarm_id

        #return '<Imc_alarm_ids %r>' % self.alarm_id,self.snow_return,self.faultDesc,self.deviceDisplay,self.severity,self.faultTime,self.userAckUserName ,self.userAckType,self.snow_number

class Elogfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    e_time = db.Column(db.String(50))
    e_msg = db.Column(db.String(150))

    def __init__(self,e_time,e_msg):
        self.e_time = e_time
        self.e_msg = e_msg

    def __repr__(self):
        return '<Elogfile %r>' % self.e_time


#Logfile table
class Imc_devices(db.Model):
    imc_id = db.Column(db.Integer,primary_key=True)
    label = db.Column(db.String(25))
    ip = db.Column(db.String(20))
    mask = db.Column(db.String(20))
    contact = db.Column(db.String(50))
    location = db.Column(db.String(100))
    sysOid = db.Column(db.String(30))
    typeName = db.Column(db.String(20))
    snow_return = db.Column(db.String(5))



    def __init__(self,
                imc_id,
                label,
                ip,
                mask,
                contact,
                location,
                sysOid,
                typeName,
                snow_return):

        self.imc_id = imc_id
        self.label = label
        self.ip = ip
        self.mask = mask
        self.contact = contact
        self.location = location
        self.sysOid = sysOid
        self.typeName = typeName
        self.snow_return = snow_return



    def __repr__(self):
        return '<Imc_devices %r>' % self.imc_id
