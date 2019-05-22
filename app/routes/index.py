import requests
from app.routes import app
from flask import render_template, session, redirect, request, flash
from requests_oauth2.services import GoogleClient
from requests_oauth2 import OAuth2BearerToken
from app.Data import User, Transaction
from collections import Counter
from mongoengine.queryset.visitor import Q

undertaker = User.objects.get(googleid='999999999')

@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get("access_token"):
        return redirect("/about")
    ledgerTransactions = list(Transaction.objects[:9])[::-1]

    totalMoney=Transaction.objects(Q(giver__ne = undertaker.id) & Q(recipient__ne = undertaker.id)).sum('amount')
    totalTransactions = Transaction.objects(Q(giver__ne = undertaker.id) & Q(recipient__ne = undertaker.id)).count()
    ledgerTransactions=Transaction.objects(Q(giver__ne = undertaker.id) & Q(recipient__ne = undertaker.id))[:20].order_by('-createdate')

    # leaderboardUsers = list(User.objects.order_by('-reputation')[:9])
    leaderboardUsers = User.objects.order_by('-reputation')

    #get the categories that have been used
    #and how many transactions of that Category
    categoryList = Counter([transaction.category for transaction in Transaction.objects])
    categories = [[category,categoryList[category]] for category in categoryList]

    return render_template('index.html',
                           ledgerTransactions=ledgerTransactions, leaderboardUsers=leaderboardUsers,
                           totalMoney=str(totalMoney), totalRep=str(totalMoney),
                           totalTransactions=str(totalTransactions),
                           categories=categories)


@app.route('/transvote/<transID>/<vote>/<dash>')
@app.route('/transvote/<transID>/<vote>')
def transvote(transID, vote, dash='notdash'):
    if not session.get("access_token"):
        return redirect("/oauth2callback")
    transaction = Transaction.objects.get(pk=transID)
    currUser = User.objects.get(googleid=session['googleID'])

    if currUser in transaction.voters:
        flash("You've already voted on that transaction")
    elif currUser == transaction.giver:
        flash("You can't vote on your own transaction.")
    elif currUser == transaction.recipient and vote == "up":
        transaction.thanks = True
        transaction.reload()
        transaction.update(thanks=True)
        flash("We will tell them thanks!")
    elif currUser == transaction.recipient and vote == "down":
        flash("Don't be a jerk.")
    else:
        if vote == "up":
            if transaction.upvote:
                upvotes = transaction.upvote + 1
                transaction.reload()
                transaction.update(upvote=upvotes)
            else:
                transaction.reload()
                transaction.update(upvote=1)
        if vote == "down":
            if transaction.downvote:
                downvotes = transaction.downvote + 1
                transaction.reload()
                transaction.update(downvote=downvotes)
            else:
                transaction.reload()
                transaction.update(downvote=1)

        transaction.update(push__voters=currUser.pk)
    if dash == "dash":
        return redirect("/dashboard")
    else:
        return redirect("/")
