import requests
from app.routes import app
from flask import render_template, session, redirect, request, flash
from requests_oauth2.services import GoogleClient
from requests_oauth2 import OAuth2BearerToken
from .Classes import User, Transaction
from collections import Counter

google_auth = GoogleClient(
    client_id=("1048349222266-n5praijtbm6a7buc893avtvmtr0k301p"
               ".apps.googleusercontent.com"),
    client_secret="gAarFeNq1vKtGXaxo96FS5H0",
    redirect_uri="http://localhost:5000/oauth2callback"
    # redirect_uri="http://otcurrency.appspot.com/oauth2callback"
    # "http://localhost:5000/oauth2callback"
    # "https://computerinv-216303.appspot.com/oauth2callback"
)


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
    currUser = User.objects.get(pk=transID)
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


@app.route('/login')
def login():
    if not session.get("access_token"):
        return redirect("/oauth2callback")
    with requests.Session() as s:
        s.auth = OAuth2BearerToken(session["access_token"])
        r = s.get("https://www.googleapis.com/plus/v1/people/me?access_token={}".format(session.get("access_token")))
    r.raise_for_status()

    data = r.json()

    if data["domain"] != "ousd.org":
        return "Please Sign in with your OUSD account"

    # Save some session variables
    session["displayName"] = data["displayName"]
    session["image"] = data["image"]["url"]
    session["googleID"] = data["id"]

    # TODO: change this to a 'get' so it doesn't iterate ovar all users
    # probably need to store the unique googleID string in the User table

    # If the user exists, update sme stuff
    try:
        editUser = User.objects.get(name=session["displayName"])
        session["wallet"] = editUser.wallet
        session["reputation"] = editUser.reputation
        # next lines inject some google values in to the User table. This code will only be needed
        # for updates eventually as the same values are created for new users.
        editUser.reload()
        editUser.update(email=data["emails"][0]["value"], googleid = data["id"], image=session["image"])
        flash(f'{session["displayName"]} successfully logged in to an existing account.')
        return redirect("/")
    except:
        # if the user does not exists, create it

        newUser = User()
        newUser.name = session["displayName"]
        newUser.image = session["image"]
        newUser.email = data["emails"][0]["value"]
        newUser.googleid = data["id"]
        # instead of giving 10 here we should create a transaction of 10 given by "the system"
        newUser.wallet = "0"
        newUser.reputation = "0"
        newUser.save()
        newUser.reload()
        # This creates a new transaction given 10 to the New User (from the newUser)
        newTransaction = Transaction()
        newTransaction.giver = newUser.id
        newTransaction.recipient = newUser.id
        newTransaction.amount = 10
        newTransaction.reason = "New User"
        newTransaction.category = "New User"
        newTransaction.createdate = datetime.now()
        newTransaction.save()
        flash("New User created! Welcome. ")
    return redirect("/")


@app.route("/oauth2callback")
def google_oauth2callback():
    code = request.args.get("code")
    error = request.args.get("error")
    if error:
        return "error :( {!r}".format(error)
    if not code:
        return redirect(google_auth.authorize_url(
            scope=["profile", "email"],
            response_type="code",
        ))
    data = google_auth.get_token(
        code=code,
        grant_type="authorization_code",
    )
    session["access_token"] = data.get("access_token")
    return redirect("/login")


@app.route("/logout")
def logout():
    [session.pop(key) for key in list(session.keys()) if key != '_flashes']

    return redirect("/")
