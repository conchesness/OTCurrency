from app.routes import app
from flask import render_template, session, request, redirect, flash, Markup, url_for
from app.Data import Transaction, User
import requests

@app.route('/users')
@app.route('/users/<page>')
def users(page=1):
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    letters = []
    for letter in alphabet:
        if User.objects(lname__istartswith=letter).count() > 0:
            letters.append(letter)

    paginatedUsers = User.objects.order_by('+lname').paginate(page=int(page),per_page=10)
    if User.objects.count() > 10:
        paginate=1
    else:
        paginate=0

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
        if User.objects(lname__istartswith=letter).count() > 0:
            letters.append(letter)
    alphaUsers = User.objects(lname__istartswith=alpha).paginate(page=1,per_page=10)
    if User.objects(lname__istartswith=alpha).count() > 10:
        paginate=1
    else:
        paginate=0

    return render_template('users.html',users=alphaUsers,letters=letters,paginate=paginate)

@app.route('/deleteuser/<userID>')
@app.route('/deleteuser/<userID>/<deleteConfirmed>')
def deleteUser(userID,deleteConfirmed='nada'):
    if not session.get("access_token"):
        flash('You are not logged in.')
        return redirect(url_for('login'))
    else:
        currUser=User.objects.get(pk=userID)
        if deleteConfirmed == 'nada':
            flash(Markup(f'Are you sure you want to delete your account? <a href="/deleteuser/{currUser.id}/yes">Yes</a> <a href="/deleteuser/{currUser.id}/no">No</a>'))
            return render_template('deleteuser.html')
        elif deleteConfirmed == 'no':
            flash(f'No, do not delete!')
            return redirect(url_for('dashboard'))
        elif deleteConfirmed == 'yes':
            flash(Markup(f'No, really, are you super duper sure? <a href="/deleteuser/{currUser.id}/superduperyes">Yes</a> <a href="/deleteuser/{currUser.id}/no">No</a>'))
            return render_template('deleteuser.html')
        elif deleteConfirmed == 'superduperyes':
            flash('Delete it')
            return render_template('deleteuser.html')
