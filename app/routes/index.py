import requests
from app.routes import app
from flask import render_template, session, redirect, request, flash
from app.Data import User, Transaction
from collections import Counter


@app.route('/', methods=['GET', 'POST'])
def index():
    ledgerTransactions = Transaction.objects.order_by('-createdate')
    # get totalmoney
    totalMoney = 0
    for transaction in ledgerTransactions:
        totalMoney += transaction.amount
    totalTransactions = len(list(Transaction.objects.order_by('-createdate')))

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


@app.route('/transvote/<transID>/<vote>')
def transvote(transID, vote):
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

    return redirect("/")
