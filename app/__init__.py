from flask import Flask
from mongoengine import connect
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or os.urandom(20)
connect("otcurrency", host='mongodb://admin:admin01@ds038888.mlab.com:38888/otcurrency')
# connect("otcurrency", host='mongodb://admin:admin01@ds060968.mlab.com:60968/otcurrencysb2')
from .routes import *















