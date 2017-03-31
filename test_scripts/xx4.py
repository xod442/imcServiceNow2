import time
from flask import Flask, request, render_template, redirect, url_for, flash, session, send_file
from flask.ext.bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from models import db, Imc_alarm_ids
from settings import APP_STATIC
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from snow_py import *
import requests
from pyhpeimc.auth import *
from pyhpeimc.plat.alarms import *
from snowbridge import *

db.create_all()
# Locked down upload folder never hurts...
UPLOAD_FOLDER = APP_STATIC
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

bootstrap = Bootstrap(app)

imc_user = "admin"
imc_passwd = "admin"
imc_host = "10.132.0.15"
snow_user = "admin"
snow_passwd = "Grape123!"
instance = "dev30543"
snow_url = 'https://dev30543.service-now.com/api/now/table/incident'
varz = []
data = {}
dump = []
alarm = {}
imc_test_url = 'http://'+imc_host+':8080'
# Configuring a connection to the VSD API
#
#   Write logfile to local database
#
# Routes
alarm['severity'] = "1"
alarm['userAckUserName'] ='admin'
alarm['deviceDisplay'] = '10.10.10.10'
alarm['faultDesc'] = "Its down"
alarm['userAckType'] = "0"
alarm['id'] = "210"
alarm['faultTime'] = "1490648244"
snow_return = "401"

print alarm['id']
print snow_return
print alarm['faultDesc']
print alarm['deviceDisplay']
print alarm['severity']
print alarm['faultTime']
print alarm['userAckUserName']
print alarm['userAckType']

write_local_db(alarm, snow_return)

'''
logfile = Imc_alarm_ids(alarm['id'],snow_return,alarm['faultDesc'],alarm['deviceDisplay'],
alarm['severity'],alarm['faultTime'],alarm['userAckUserName'], alarm['userAckType'])
print logfile
db.session.add(logfile)
db.session.commit()
'''
print "Peace!"
