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
@app.route('/index', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    # On post get all the credentials
    if request.method == 'POST':
        alarm['severity'] = 1
        alarm['userAckUserName'] ='admin`'
        alarm['deviceDisplay'] = '10.10.10.10'
        alarm['faultDesc'] = "Its down"
        alarm['userAckType'] = 0
        alarm['id'] = 102
        alarm['faultTime'] = 1490648244
        snow_return = 401
        check = Imc_alarm_ids.query.filter_by(alarm_id=alarm['id']).all()
        if check:
            flash('Database Error...duplicate records', 'error')
        else:
            logfile = Imc_alarm_ids(alarm['severity'],alarm['userAckUserName'],
                alarm['deviceDisplay'],alarm['faultDesc'],alarm['userAckType'],
                    alarm['id'],alarm['faultTime'], snow_return)
        db.session.add(logfile)
        db.session.commit()
        flash('Record was successfully added')
        return render_template('blank.html', vars = logfile)


@app.route('/logout')
def logout():
    session.pop('userx', None)
    session.pop('passwd', None)
    session.pop('org', None)
    session.pop('ipaddress', None)
    session.pop('enterprise', None)
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
