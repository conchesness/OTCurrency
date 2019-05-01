from app.routes import app
from flask import render_template, session, request, redirect, flash
from .Classes import Transaction, User
import requests

@app.route('/users')
def users():
    users = User.objects.order_by('+name')

    return render_template('users.html',users=users)

@app.route('/transactions/<userID>')
def transactionsbyusers(userID):
    received = Transaction.objects(recipient=userID).order_by('-createdate')
    giver = Transaction.objects(giver=userID).order_by('-createdate')
    user = User.objects.get(pk=userID)

    return render_template('transbyuser.html', received=received, giver=giver, user=user)
