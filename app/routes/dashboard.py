from app.routes import app
from flask import render_template, session, request, redirect, flash, Markup
from app.Forms import GiveForm
from app.Data import Transaction, User, Role
import requests
from datetime import datetime
from mongoengine.queryset.visitor import Q
from .gibberish import *

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not session.get("access_token"):
        return redirect("/oauth2callback")

    form = GiveForm.new()
    currUser = User.objects.get(googleid=session['googleID'])
    received = Transaction.objects(recipient=currUser.id).sum('amount')
    given = Transaction.objects(giver=currUser.id).sum('amount')
    myWallet = received-given

    #if request.method == 'POST' and form.validate():
    if request.method == 'POST' and form.validate():
        validTransaction = False

        if classifygibberish(form.reason.data) > 80 or len(form.reason.data) < 50:
            flash(f"Please write a better reason for giving {form.amount.data} coin to {form.recipient.data}. It can't be gibberish and it must be at least 50 characters.")
            return redirect("/dashboard")

        if form.recipient.data == "The Undertaker":
            flash(Markup("<img width='200' src='/static/undertaker.jpg'>&nbsp;&nbsp;You can't give to The Undertaker. The Undertaker laughs at you. Haaaa haaaa haaa"))
            return redirect("/dashboard")

        # check that giver isn't giving money to themselves
        if (currUser.name == form.recipient.data):
            flash(f"hey {currUser.fname}, you can't give it to yourself.")
            return redirect("/dashboard")

        if int(form.amount.data) < 6 and int(form.amount.data) > 0:
            pass
        else:
            flash('You can only give between 0 and 5')
            return redirect("/dashboard")

        # check if giver has enough money
        if (int(myWallet) >= int(form.amount.data)):
            pass
        else:
            flash(f"You can't send {form.amount.data} when you only have {myWallet}")
            return redirect("/dashboard")

        if currUser.gaveto != form.recipient.data:
            pass
        else:
            flash("You can't give to the same person twice in a row.")
            return redirect("/dashboard")

        # Transaction passed all checks
        # get giver data
        currUser.reload()
        # get recipient data
        recipientUser = User.objects.get(name=form.recipient.data)
        # create the transaction
        newTransaction = Transaction()
        newTransaction.giver = currUser
        newTransaction.recipient = recipientUser
        newTransaction.amount = form.amount.data
        newTransaction.reason = form.reason.data
        newTransaction.category = form.category.data
        newTransaction.createdate = datetime.now()
        newTransaction.save()

        #load currUser
        currUser.update(gaveto=form.recipient.data)

        flash(f"You successfully sent {form.amount.data} currency to {form.recipient.data}")
        return redirect("/dashboard")

    # Update session and other variables
    currUser.reload()
    userTransactions = Transaction.objects(Q(giver=currUser.id) | Q(recipient=currUser.id)).order_by('-createdate')
    userTransactions = userTransactions[:10]
    received = Transaction.objects(recipient=currUser.id).sum('amount')
    given = Transaction.objects(giver=currUser.id).sum('amount')
    myWallet = received-given
    numReceived = Transaction.objects(recipient=currUser.id).count()
    numGiven = Transaction.objects(giver=currUser.id).count()
    numtrans=numReceived+numGiven
    currUser.update(wallet=myWallet,reputation=given, numtrans=numtrans)
    session["wallet"] = myWallet
    session["reputation"] = given

    #form.recipient.choices = [(row.name, row.name) for row in User.objects()]

    return render_template('dashboard.html', wallet=myWallet, reputation=given,
                            form=form, totalTransactions = numtrans, userTransactions = userTransactions,
                            user=currUser)
