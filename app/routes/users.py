from app.routes import app
from flask import render_template, session, request, redirect, flash
from .Classes import Transaction, User
import requests

@app.route('/users')
@app.route('/users/<page>')
def users(page=1):
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    letters = []
    for letter in alphabet:
        if User.objects(name__istartswith=letter).count() > 0:
            letters.append(letter)
    paginatedUsers = User.objects.order_by('+name').paginate(page=int(page),per_page=10)
    if User.objects.count() > 10:
        paginate=1

    return render_template('users.html',users=paginatedUsers,letters=letters,paginate=paginate)

@app.route('/transactions/<userID>')
def transactionsbyusers(userID):
    received = Transaction.objects(recipient=userID).order_by('-createdate')
    giver = Transaction.objects(giver=userID).order_by('-createdate')
    user = User.objects.get(pk=userID)

    return render_template('transbyuser.html', received=received, giver=giver, user=user)

@app.route('/userstartswith/<alpha>')
def userstartswith(alpha):
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    letters = []
    for letter in alphabet:
        if User.objects(name__istartswith=letter).count() > 0:
            letters.append(letter)
    alphaUsers = User.objects(name__istartswith=alpha).paginate(page=1,per_page=10)
    if User.objects(name__istartswith=alpha).count() > 10:
        paginate=1
    else:
        paginate=0

    return render_template('users.html',users=alphaUsers,letters=letters,paginate=paginate)
