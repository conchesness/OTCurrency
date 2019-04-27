from flask import Flask
from mongoengine import connect
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or os.urandom(20)
connect("otcurrency", host='mongodb://admin:admin01@ds058048.mlab.com:58048/otcurrencysb')
# connect("otcurrency", host='mongodb://admin:admin01@ds038888.mlab.com:38888/otcurrency')
from .routes import *
