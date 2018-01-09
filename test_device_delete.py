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
imc_host = "10.1.8.107"
snow_user = "admin"
snow_passwd = "Grape123!"
instance = "dev26166"
snow_url = 'https://'+instance+'.service-now.com/api/now/table/u_imcdevices'

# Configuring a connection to the VSD API

auth = IMCAuth("http://", imc_host, "8080", imc_user, imc_passwd)

while True:
    print "Getting devices from IMC`"
    # Step Four:
    # Sync IMC devices to service now
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
    while (c < len(dev_list)):
        try:
            db.session.delete(dev_list[c])
            db.session.commit()
        except:
            db.session.rollback()
        c = c + 1
    print "......All Devices are deleted"
    time.sleep(2)
