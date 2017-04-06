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

Functions to interact with Sevice Now and snowBridge local databases
03212017 Initial release.


'''


import time
from flask import Flask, request, render_template, redirect, url_for, flash, session, send_file
from flask.ext.bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from models import db, Imc_alarm_ids, Imc_devices
from settings import APP_STATIC
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from snowbridge import *
import requests
from pyhpeimc.auth import *
from pyhpeimc.plat.alarms import *
from pyhpeimc.plat.device import *
from reconcile import *
from process_imc_recover import *

imc_user = "admin"
imc_passwd = "admin"
imc_host = "10.132.0.15"
snow_user = "admin"
snow_passwd = "xxxxxx!"
instance = "dxxxxxxx4"
url = 'https://'+instance+'.service-now.com/api/now/table/incident'
dev_url = 'https://'+instance+'.service-now.com/api/now/table/u_imcdevices'

# Configuring a connection to the VSD API

auth = IMCAuth("http://", imc_host, "8080", imc_user, imc_passwd)
c = 1
while True:
    # IMC has a habit of denying the first request...try twice!
    # Get real time alarms from IMC
    try:
        alarms = get_realtime_alarm('admin', auth.creds, auth.url)
        assert type(alarms) is list
    except:
        pass
    # Get real time alarms from IMC
    try:
        alarms = get_realtime_alarm('admin', auth.creds, auth.url)
        assert type(alarms) is list
    except:
        print "Failure to communicate with IMC"


    print "Success reading alarms from IMC..........."
    status = "snowBridge is operational"
    print status
    for alarm in alarms:
        # Step one. Look for the alarm in the local data base
        print "Step 1: checking local database"
        check = Imc_alarm_ids.query.filter_by(alarm_id=alarm['id']).all()
        # adjust the acktype to sync with snow levels 1 = new, 2 = In Porocess, 7 = closed

        # If no record, open snow incident and add alarm to local db
        if check == []:
            print "IMC Real Time alarm not in database"
            # Create new incident in Service Now

            snowObject = post_snow(alarm, url, snow_user, snow_passwd)
            # Returns a list with the incident number and the HTML return code
            snow_number = snowObject[0]
            snow_return = snowObject[1]
            print "%s, %s " % (snow_number, snow_return)
            # Write to local database
            # Reset alarm leves to match IMC for local storage
            print "Writing alarm information to local database"
            print alarm
            write_local_db(alarm, snow_return, snow_number)


        # Step Two: Check the status of the snow ticket. If it has been acknowledged
        # or closed in snow, update IMC and local database.
        # Adjust the acktype to sync with snow levels 1 = new, 2 = In Porocess, 7 = closed

        print "Comparing Service Now Incident with IMC ack status......."

        # Reconcile snow to imc
        result = reconcile(alarm, url, snow_user, snow_passwd, auth)
        print result


    # Step Three:  Now that all the realtime alarms have been processes. Look in the local db and
    # check for realtime alarms that have been recovered in IMC. They will not be
    # processed in the above loop as it it only for realtime alarms, not recovered.
    print "Looking for any RT alarms that have been recovered by IMC....updating"
    print
    print
    result = process_imc_recover(url, snow_user, snow_passwd, auth)

    # Step Four:
    # Delete all local db alarms that are closed with a value of 7 userAckType
    print "Removing closed alarms from the local snowbridge database"
    local_alarms = Imc_alarm_ids.query.all()
    for a in local_alarms:
        # Returns a list of fields whare the alarm id matches query
        check = Imc_alarm_ids.query.filter_by(alarm_id=a.alarm_id).all()
        if check[0].userAckType == "7":
            db.session.delete(check[0])
            db.session.commit()
    # Step Five:
    # Sync IMC devices to service now
    print "Getting devices from IMC`"
    dev_list = get_all_devs(auth.creds,auth.url,network_address=None)
    c = 0
    print "snowBridge has is now updating devices between IMC and Service Now %s" % c
    print
    print "=======S=N=O=W==B=R=I=D=G=E====SNOW/IMC===Add Device================"
    print "|               Adding device..............                        |"
    print "+------------------------------------------------------------------+"
    print
    print
    print
    # snow_return = '400'
    for i in dev_list:

        check = Imc_devices.query.filter_by(imc_id=i['id']).all()

        # If no record, device to snow and add device to local db
        if check == []:
            print "Device not in local snowbridge database....adding...sending to snow"
            # Create new device in Service Now

            snowObject = load_snow(i, dev_url, snow_user, snow_passwd)

            # Returns a HTML return code
            print snowObject
            print type(snowObject)


            print "After the device is added to SNOW this is the return %s,  " % (snowObject)
            # Write to local database
            #print i
            write_device_db(i, snowObject)
            print '.....added'

    c = c + 1
    print "......All Devices are sync'd"
    time.sleep(2)


    print "snowBridge has completed %s Service Now and IMC sync cycles" % c
    print
    print "=======S=N=O=W==B=R=I=D=G=E====SNOW/IMC===ALARM=SYNC================"
    print "|               Sleeping.......5 minutes                           |"
    print "+------------------------------------------------------------------+"
    print
    print
    print

    c = c + 1
    time.sleep(60)
