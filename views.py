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

Flask script that builds a bridge between HPE IMC and Service Now

KEY: +------------------------------------------------------+
     |   Service now state = 1 incident is new
     |   Service now state = 2 incident is In Process
     |   Service now state = 7 incident is closed
     |   IMC Real Time Alarm userAckType  = 0 incident is unacknowledged
     |   IMC Real Time Alarm userAckType  = 1 incident is acknowledged
     |   get_alarm_details = 0  alarm is unacknowledged
     |   get_alarm_details = 1  alarm is acknowledged
     |   get_alarm_details = 7  alarm is recovered
     +------------------------------------------------------+


     03302017 Initial release.


'''

import time
from flask import Flask, request, render_template, redirect, url_for, flash, session, send_file
from flask.ext.bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from models import db, Imc_alarm_ids
from settings import APP_STATIC
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from snowbridge import *
import requests
from pyhpeimc.auth import *
from pyhpeimc.plat.alarms import *

# Locked down upload folder never hurts...
UPLOAD_FOLDER = APP_STATIC
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

bootstrap = Bootstrap(app)

# Routes
@app.route('/index', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    # On post get all the credentials
    if request.method == 'POST':
        imc_user = request.form.get('imc_user')
        imc_passwd = request.form.get('imc_passwd')
        imc_host = request.form.get('imc_host')
        snow_user = request.form.get('snow_user')
        snow_passwd = request.form.get('snow_passwd')
        instance = request.form.get('instance')
        snow_url = 'https://'+instance+'.service-now.com/api/now/table/incident'

        # Configuring a connection to the VSD API

        auth = IMCAuth("http://", imc_host, "8080", imc_user, imc_passwd)

        while True:
            status = "snowBridge is operational"
            # Get real time alarms from IMC
            try:
                alarms = get_realtime_alarm('admin', auth.creds, auth.url)
                assert type(alarms) is list
            except:
                return render_template('comm_error_imc.html', imc_user= imc_user, imc_passwd=imc_passwd)

            for alarm in alarms:
                # Step one. Look for the alarm in the local data base
                check = Imc_alarm_ids.query.filter_by(alarm_id=alarm['id']).all()
                # If no record, open snow incident and add alarm to local db
                if check == []:
                    # Create new incident in Service Now
                    snowObject = post_snow(alarm, snow_url, snow_user, snow_passwd)
                    # Returns a list with the incident number and the HTML return code
                    snow_number = snowObject[0]
                    snow_return = snowObject[1]
                    # Write to local database
                    write_local_db(alarm, snow_return, snow_number)

                # Step two: Check if the incident has been acknowledged on IMC
                # Initially, userAckType = 0, if the incoming RT alarm does not match
                # That is because it has been acknowledged We never see recovered alarms inthe
                # Real time alarms.
                check = Imc_alarm_ids.query.filter_by(alarm_id=alarm['id']).all()

                if alarm['userAckType'] != check[0].userAwkType:
                    #The realtime alarm has been acknowledged! , no other possibility
                    alarm['userAckType'] ="1"
                    # Save local database
                    update_local_db(alarm)
                    # Get the snow incident read values
                    snow_url = snow_url+'?number='+check[0].snow_number
                    # snowObject is a dict of the snow incident
                    snowObject = get_snow(snow_url, snow_user, snow_passwd)
                    # get the service now system identifier for the incident, needed to update record
                    sys_id = snowObject['result'][0]['sys_id']
                    # set the "In-Progress" status on the service now incident 1 = "In Process"
                    alarm['state'] = "1"
                    # Set the URL for the PUT
                    snow_url = 'https://dev30543.service-now.com/api/now/table/incident/'+sys_id
                    # Update service now incident record
                    snowObject = ack_snow(alarm, snow_url, snow_user, snow_passwd)

                # Step three: Check if the incident has been acknowledged on service now
                # Initially, userAckType = 0, if the incoming service now "state" does not match
                # That is because it has been acknowledged, or closed
                check = Imc_alarm_ids.query.filter_by(alarm_id=alarm['id']).all()
                snow_url = 'https://dev30543.service-now.com/api/now/table/incident?number='+check[0].snow_number
                data = get_snow(snow_url, snow_user, snow_passwd)
                if data['result'][0]['state'] != check[0].userAckType:
                    # set local db variables
                    alarm['userAckType'] = data['result'][0]['state']
                    alarm_id = alarm['id']
                    # Save local database
                    update_local_db(alarm)
                     # If it is a 2 service now ack'd the incident, If its 7, snow closed it.
                    if data['result'][0]['state'] == '1':
                         pass
                    if data['result'][0]['state'] == '2':
                         # Acknowledge Alarm in IMC
                         result = acknowledge_alarm(alarm_id, auth.creds, auth.url)
                    if data['result'][0]['state'] == '7':
                         # Recover the alarm in IMC
                         result = recover_alarm(alarm_id, auth.creds, auth.url)

            # Setp four: Check the status of all snow tickets in the local database
            # Get all local alarm records from IMC and reconcile all alarm states:
            # Alarms in the database will no longer be processed by the realtime loop (steps 1-3)
            # If the are acknowleded in IMC. IMC takes them out of the real time alarms.
            # This step just cleans up the two systems.
            # Get all local alarms in the database
            localdb = Imc_alarm_ids.query.all()
            for a in localdb:
                # Get matching snow incident
                snow_url = 'https://dev30543.service-now.com/api/now/table/incident?number='+a.snow_number
                data = get_snow(snow_url, snow_user, snow_passwd)
                # data['result'][0]['state'] = snow incident status 1-New,2-In process, or 7-Closed
                s = data['result'][0]['state']
                # get alarm details from IMC
                alarm_details = get_alarm_details(a.alarm_id, auth.creds, auth.url)
                #alarm_details['ackStatus'] is the status of the alarm in IMC
                i = alarm_details['ackStatus']
                if s == '1' and i == '1': #   snow is new and imc is acknowledged
                    # udate snow to a 2 (in-Precess)
                    # Get the snow incident read values
                    snow_url = snow_url+'?number='+check[0].snow_number
                    # snowObject is a dict of the snow incident
                    snowObject = get_snow(snow_url, snow_user, snow_passwd)
                    # get the service now system identifier for the incident, needed to update record
                    sys_id = snowObject['result'][0]['sys_id']
                    # set the "In-Progress" status on the service now incident 1 = "In Process"
                    alarm['state'] = "1"
                    # Set the URL for the PUT
                    snow_url = 'https://dev30543.service-now.com/api/now/table/incident/'+sys_id
                    # Update service now incident record
                    snowObject = ack_snow(alarm, snow_url, snow_user, snow_passwd)

                    # update local to a 1 (acknowledged)
                    alarm['userAckType'] ="1"
                    # Save local database
                    update_local_db(alarm)

                if s == '1' and i == '7': #   snow is new and imc is closed
                    # Get the snow incident read values
                    snow_url = snow_url+'?number='+check[0].snow_number
                    # snowObject is a dict of the snow incident
                    snowObject = get_snow(snow_url, snow_user, snow_passwd)
                    # get the service now system identifier for the incident, needed to update record
                    sys_id = snowObject['result'][0]['sys_id']
                    # set the "In-Progress" status on the service now incident 1 = "In Process"
                    alarm['state'] = "7"
                    # Set the URL for the PUT
                    snow_url = 'https://dev30543.service-now.com/api/now/table/incident/'+sys_id
                    # Update service now incident record
                    snowObject = ack_snow(alarm, snow_url, snow_user, snow_passwd)

                    # update local to a 1 (closed)
                    alarm['userAckType'] ="7"
                    # Save local database
                    update_local_db(alarm)

                if s == '2' and i == '0': #   snow is In Process and imc is new
                    # udate IMC to userAckType['1'] acknowledged
                    result = acknowledge_alarm(a.alarm_id, auth.creds, auth.url)
                        # TODO check this return, write to error db
                    # update local to a 1 (acknowledged)
                    alarm['userAckType'] ="1"
                    # Save local database
                    update_local_db(alarm)

                if s == '2' and i == '7':  #   snow is in process and imc is closed
                    # udate snow to closed - 7
                    snow_url = snow_url+'?number='+check[0].snow_number
                    # snowObject is a dict of the snow incident
                    snowObject = get_snow(snow_url, snow_user, snow_passwd)
                    # get the service now system identifier for the incident, needed to update record
                    sys_id = snowObject['result'][0]['sys_id']
                    # set the "In-Progress" status on the service now incident 1 = "In Process"
                    alarm['state'] = "7"
                    # Set the URL for the PUT
                    snow_url = 'https://dev30543.service-now.com/api/now/table/incident/'+sys_id
                    # Update service now incident record
                    snowObject = ack_snow(alarm, snow_url, snow_user, snow_passwd)
                    # update local to a 7 (Closed)
                    # update local to a 1 (closed)
                    alarm['userAckType'] ="7"
                    # Save local database
                    update_local_db(alarm)

                if s == '7' and i == '0': #   snow is closed and imc is realtime new
                    # recover IMC
                    # update local to a 7 (Closed)
                    # udate IMC to userAckType['1'] acknowledged
                    result = recover_alarm(a.alarm_id, auth.creds, auth.url)
                        # TODO check this return, write to error db

                    # update local to a 1 (acknowledged)
                    alarm['userAckType'] ="7"
                    # Save local database
                    update_local_db(alarm)

                if s == '7' and i == '1': #   snow is closed and imc is acknowledged
                    # udate IMC to userAckType['1'] acknowledged
                    result = recover_alarm(a.alarm_id, auth.creds, auth.url)
                        # TODO check this return, write to error db

                    # update local to a 1 (acknowledged)
                    alarm['userAckType'] ="7"
                    # Save local database
                    update_local_db(alarm)




            return render_template('state.html', state = status)
            time.sleep(20)

    return render_template('login.html')




@app.route('/logout')
def logout():
    return redirect(url_for('index'))


@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/about')
def about():
    return redirect('http://www.wookieware.com')


if __name__ == '__main__':
    #db.create_all()
    app.secret_key = 'SuperSecret'
    app.debug = True
    app.run(host='0.0.0.0')
