import requests
from app.routes import app
from flask import render_template, session, redirect, request, flash
from requests_oauth2.services import GoogleClient
from requests_oauth2 import OAuth2BearerToken
from app.Data import User, Transaction
from collections import Counter

google_auth = GoogleClient(
    client_id=("1048349222266-n5praijtbm6a7buc893avtvmtr0k301p"
               ".apps.googleusercontent.com"),
    client_secret="gAarFeNq1vKtGXaxo96FS5H0",
    redirect_uri="http://localhost:5000/oauth2callback"
    # redirect_uri="http://otcurrency.appspot.com/oauth2callback"
)

@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get("access_token"):
        return redirect("/about")
    ledgerTransactions = list(Transaction.objects[:9])[::-1]

    # get totalmoney
    totalMoney = 0
    for transaction in list(Transaction.objects):
        totalMoney += int(transaction.amount)
    totalTransactions = len(list(Transaction.objects))

    # leaderboardUsers = list(User.objects.order_by('-reputation')[:9])
    leaderboardUsers = list(User.objects.order_by('-reputation'))
    #get the categories that have been used
    #and how many transactions of that Category
    categoryList = Counter([transaction.category for transaction in Transaction.objects])
    categories = [[category,categoryList[category]] for category in categoryList]


    return render_template('index.html',
                            ledgerTransactions=ledgerTransactions, leaderboardUsers=leaderboardUsers,
                            totalMoney = str(totalMoney), totalRep = str(totalMoney), totalTransactions = str(totalTransactions),
                            categories = categories)

@app.route('/transvote/<transID>/<vote>')
def transvote(transID,vote):
    if not session.get("access_token"):
        return redirect("/oauth2callback")
    transaction = Transaction.objects.get(pk=transID)
    for user in User.objects:
        if user.name == session["displayName"]:
            userObj = user

    if userObj in transaction.voters:
        flash("You've already voted on that transaction")
    elif userObj == transaction.giver:
        flash("You can't up vote your transaction.")
    elif userObj == transaction.recipient and vote == "up":
        transaction.thanks = True
        transaction.reload()
        transaction.update(thanks=True)
        flash("We will tell them thanks!")
    elif userObj == transaction.recipient and vote == "down":
        flash("Don't be a jerk.")
    else:
        if vote == "up":
            if transaction.upvote:
                upvotes = transaction.upvote + 1
                transaction.reload
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

        transaction.update(push__voters=userObj.pk)

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
    # flash(data)

    if data["domain"] != "ousd.org":
        return "Please Sign in with your OUSD account"

    # Save Necessary variables
    session["displayName"] = data["displayName"]
    session["image"] = data["image"]["url"]
    session["googleid"] = data["id"]

    user = User()

    # TODO: change this to a 'get' so it doesn't iterate ovar all users
    # probably need to store the unique googleID string in the User table
    userObjs = User.objects()
    for i in userObjs:
        if i.name == session["displayName"]:
            session["wallet"] = i.wallet
            session["reputation"] = i.reputation
            # next lines are temp to inject some google values in to the User table
            i.reload()
            i.update(email = data["emails"][0]["value"],googleid = data["id"])
            return redirect("/")

    user.name = session["displayName"]
    user.image = session["image"]
    user.email = data["emails"][0]["value"]
    user.googleid = data["id"]
    user.wallet = "10"
    user.reputation = "0"
    session["wallet"] = user.wallet
    session["reputation"] = user.reputation
    user.save()

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
