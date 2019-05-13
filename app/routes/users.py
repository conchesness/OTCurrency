from app.routes import app
from flask import render_template, session, request, redirect, flash
from .Classes import Transaction, User
import requests

@app.route('/users')
@app.route('/users/<page>')
def users(page=1):
    paginatedUsers = User.objects.order_by('+name').paginate(page=int(page),per_page=12)
    # paginatedUsers = User.objects.paginate(page=1, per_page=10).order_by('+name')

    return render_template('users.html',users=paginatedUsers)

@app.route('/transactions/<userID>')
def transactionsbyusers(userID):
    received = Transaction.objects(recipient=userID).order_by('-createdate')
    giver = Transaction.objects(giver=userID).order_by('-createdate')
    user = User.objects.get(pk=userID)

    return render_template('transbyuser.html', received=received, giver=giver, user=user)

@app.route('/userstartswith/<alpha>')
def userstartswith(alpha):
    alphaUsers = User.objects(name__istartswith=alpha).paginate(page=1,per_page=10)

    return render_template('users.html',users=alphaUsers,page=1)
