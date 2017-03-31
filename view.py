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
from reconcile import *
from process_imc_recover import *

imc_user = "admin"
imc_passwd = "admin"
imc_host = "10.132.0.15"
snow_user = "admin"
snow_passwd = "Grape123!"
instance = "dev30543"
url = 'https://'+instance+'.service-now.com/api/now/table/incident'

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

        # Step two: Check if the incident has been acknowledged on IMC
        # Initially, userAckType = 0, if the incoming RT alarm does not match
        # That is because it has been acknowledged We never see recovered alarms inthe
        # Real time alarms.
        print "step 2...comparing ack from IMC rt alarm with the local db"
        check = Imc_alarm_ids.query.filter_by(alarm_id=alarm['id']).all()
        print check[0].userAckType
        print alarm['userAckType']

        if alarm['userAckType'] != check[0].userAckType:
            print "Alarm acknowledged on IMC....updating local database and Service Now"
            #The realtime alarm has been acknowledged! , no other possibility
            alarm['userAckType'] ="1"
            # Save local database
            update_local_db(alarm)
            # Get the snow incident read values
            snow_url = url+'?number='+check[0].snow_number
            print "This is a suspicious snow_url %s" % snow_url
            # snowObject is a dict of the snow incident
            snowObject = get_snow(snow_url, snow_user, snow_passwd)
            # get the service now system identifier for the incident, needed to update record
            sys_id = snowObject['result'][0]['sys_id']
            # set the "In-Progress" status on the service now incident 1 = "In Process"
            alarm['state'] = "2"
            # Set the URL for the PUT
            snow_url = url+'/'+sys_id
            # Update service now incident record
            snowObject = ack_snow(alarm, snow_url, snow_user, snow_passwd)

        # Step three: Check the status of the snow ticket
        # Alarms in the database will no longer be processed by the realtime loop (steps 1-2)
        # if the are acknowleded in IMC.
        # IMC takes them out of the real time alarms.
        # This step just cleans up the two systems.


        print "Comparing Service Now Incident with IMC ack status......."

        # Reconcile snow to imc
        result = reconcile(alarm, url, snow_user, snow_passwd, auth)
        print result


    # Now that all the realtime alarms have been processes. Look in the local db and
    # check for realtime alarms that have been recovered in IMC. They will not be
    # processed in the above loop as it it only for realtime alarms, not recovered.
    print "Looking for any RT alarms that have been recovered by IMC....updating"
    print
    print
    result = process_imc_recover(url, snow_user, snow_passwd, auth)

    c = c + 1
    print "snowBridge has completed %s Service Now and IMC sync cycles" % c
    print
    print "=======S=N=O=W==B=R=I=D=G=E====SNOW/IMC===ALARM=SYNC================"
    print "|               Sleeping.......5 minutes                           |"
    print "+------------------------------------------------------------------+"
    print
    print
    print
    time.sleep(3000)
