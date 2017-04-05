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
snow_passwd = "xxxxxxxx"
instance = "xxxxxxx"
url = 'https://'+instance+'.service-now.com/api/now/table/incident'

# Configuring a connection to the VSD API

auth = IMCAuth("http://", imc_host, "8080", imc_user, imc_passwd)
c = 1
db.create_all()
