
import time
from flask import Flask, request, render_template, redirect, url_for, flash, session, send_file
from flask.ext.bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from models import db, Imc_alarm_ids
from settings import APP_STATIC
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import requests
from pyhpeimc.auth import *
from pyhpeimc.plat.alarms import *
from snowbridge import *

def process_imc_recover(url,snow_user,snow_passwd,auth):

    """
    function compares the ack state in snow and IMC
    :param url: A URL for the service now table
    :param snow_user: A str for the Service Now instance
    :param snow_passwd: A str for the Service Now instance
    :return: action taken by the switcher
    :rtype: int or string value of the action taken
    >>> from reconcile import *
    >>> result = reconcile('https://'devXXXXX.service-now.com/api/now/table/incident','admin','admin',{auth})
    >>> assert action != ''
    """
    local_alarms = Imc_alarm_ids.query.all()
    update = {}
    alarm = {}
    for a in local_alarms:
        # Refresh the database vars to get the snow_numner
        check = Imc_alarm_ids.query.filter_by(alarm_id=a.alarm_id).all()
        # Build alarm dict
        alarm['id'] = check[0].alarm_id

        # Get matching snow incident
        snow_url = url+'?number='+check[0].snow_number
        data = get_snow(snow_url, snow_user, snow_passwd)
        # data['result'][0]['state'] = snow incident status 1-New,2-In process, or 7-Closed
        s = data['result'][0]['state']
        # Get the status of the IMC alarm using get_alarm_status from snowbridge
        i = get_alarm_status(alarm, auth)

        print "IPROC: this is the ack from snow %s" % s
        print "IPROC: this is the ack from imc %s" % i
        print "IPROC: current alarm id is %s" % alarm['id']
        print "IPROC: this is the snow ticket %s" % check[0].snow_number

        action = "IPROC: no switcher"

        if s == '1' and i == '1': #   snow is new and imc is acknowledged
            action = "IPROC: snow is new and imc is acknowledged.....switch 1"
            # udate snow to a 2 (in-Precess)
            # Get the snow incident read values
            snow_url = url+'?number='+check[0].snow_number
            print "IPROC: This is a suspicious snow_url %s" % snow_url
            # snowObject is a dict of the snow incident
            snowObject = get_snow(snow_url, snow_user, snow_passwd)
            # get the service now system identifier for the incident, needed to update record
            sys_id = snowObject['result'][0]['sys_id']
            # set the "In-Progress" status on the service now incident 1 = "In Process"
            update['state'] = "2"
            # Set the URL for the PUT
            snow_url = url+'/'+sys_id
            print "IPROC: This is a PUT url %s " % snow_url
            print  update
            # Update service now incident record
            snowObject = ack_snow(update, snow_url, snow_user, snow_passwd)
            print "IPROC: this is the return_code from snow %s" % snowObject
            # update local to a 1 (acknowledged)
            alarm['userAckType'] ="1"
            # Save local database
            update_local_db(alarm)

        if s == '1' and i == '7': #   snow is new and imc is closed
            action = "IPROC: snow is new and imc is closed.....switch 2"
            # Get the snow incident read values
            snow_url = url+'?number='+check[0].snow_number
            # snowObject is a dict of the snow incident
            snowObject = get_snow(snow_url, snow_user, snow_passwd)
            # get the service now system identifier for the incident, needed to update record
            sys_id = snowObject['result'][0]['sys_id']
            # set the "In-Progress" status on the service now incident 1 = "In Process"
            update['state'] = "7"
            # Set the URL for the PUT
            snow_url = url+'/'+sys_id
            # Update service now incident record
            snowObject = ack_snow(update, snow_url, snow_user, snow_passwd)

            # update local to a 1 (closed)
            alarm['userAckType'] ="7"
            # Save local database
            update_local_db(alarm)

        if s == '2' and i == '0': #   snow is In Process and imc is new
            action = "IPROC: now is In Process and imc is new.....switch 3"
            # udate IMC to userAckType['1'] acknowledged
            result = acknowledge_alarm(alarm['id'], auth.creds, auth.url)
                # TODO check this return, write to error db
            # update local to a 1 (acknowledged)
            alarm['userAckType'] ="1"
            # Save local database
            update_local_db(alarm)

        if s == '2' and i == '7':  #   snow is in process and imc is closed
            action = "IPROC: snow is in process and imc is closed.....switch 4"
            # udate snow to closed - 7
            snow_url = url+'?number='+check[0].snow_number
            # snowObject is a dict of the snow incident
            snowObject = get_snow(snow_url, snow_user, snow_passwd)
            # get the service now system identifier for the incident, needed to update record
            sys_id = snowObject['result'][0]['sys_id']
            # set the "In-Progress" status on the service now incident 1 = "In Process"
            update['state'] = "7"
            # Set the URL for the PUT
            snow_url = url+'/'+sys_id
            # Update service now incident record
            snowObject = ack_snow(update, snow_url, snow_user, snow_passwd)
            # update local to a 7 (Closed)
            # update local to a 1 (closed)
            alarm['userAckType'] ="7"
            # Save local database
            update_local_db(alarm)

        if s == '7' and i == '0': #   snow is closed and imc is realtime new
            action = "IPROC: snow is closed and imc is realtime new....switch 5"
            # recover IMC
            # update local to a 7 (Closed)
            # udate IMC to userAckType['1'] acknowledged
            result = recover_alarm(alarm['id'], auth.creds, auth.url)
                # TODO check this return, write to error db

            # update local to a 1 (acknowledged)
            alarm['userAckType'] ="7"
            # Save local database
            update_local_db(alarm)

        if s == '7' and i == '1': #   snow is closed and imc is acknowledged
            action = "IPROC: snow is closed and imc is acknowledged.....switch 6"
            # udate IMC to userAckType['1'] acknowledged
            result = recover_alarm(alarm['id'], auth.creds, auth.url)
                # TODO check this return, write to error db

            # update local to a 1 (acknowledged)
            alarm['userAckType'] ="7"
            # Save local database
            update_local_db(alarm)



    return action
