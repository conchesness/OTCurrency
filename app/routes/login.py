import requests
from app.routes import app
from flask import render_template, session, redirect, request, flash
from requests_oauth2.services import GoogleClient
from requests_oauth2 import OAuth2BearerToken
from app.Data import User, Transaction
from datetime import datetime

google_auth = GoogleClient(
    client_id=("1048349222266-n5praijtbm6a7buc893avtvmtr0k301p"
               ".apps.googleusercontent.com"),
    client_secret="gAarFeNq1vKtGXaxo96FS5H0",
    redirect_uri="http://localhost:5000/oauth2callback"
    # redirect_uri="http://otcurrency.appspot.com/oauth2callback"
    # "http://localhost:5000/oauth2callback"
    # "https://computerinv-216303.appspot.com/oauth2callback"
)

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
        editUser.update(email=data["emails"][0]["value"],
                        googleid=data["id"],
                        image=session["image"],
                        fname=data['name']['givenName'],
                        lname=data['name']['familyName'])
        flash(f'{session["displayName"]} successfully logged in to an existing account.')
        return redirect("/")
    except:
        # if the user does not exists, create it

        newUser = User()
        newUser.name = session["displayName"]
        newUser.image = session["image"]
        newUser.email = data["emails"][0]["value"]
        newUser.googleid = data["id"]
        newUser.fname = data['name']['givenName']
        newUser.lname = data['name']['familyName']
        # instead of giving 10 here we should create a transaction of 10 given by "the system"
        newUser.wallet = "0"
        newUser.reputation = "0"
        newUser.save()
        flash("New User created! Welcome. ")
        newUser.reload()
        # This creates a new transaction giving 10 to the New User (from the newUser)

        # Giver is Stephen Wright
        # newTransGiver=User.objects.get(googleid='118043475517321263044')

        # Giver is the Undertaker
        newTransGiver=User.objects.get(googleid='999999999')
        newTransaction = Transaction()
        newTransaction.giver = newTransGiver.id
        newTransaction.recipient = newUser.id
        newTransaction.amount = 50
        newTransaction.reason = "Welcome to OTCurrency!"
        newTransaction.category = "New User"
        newTransaction.createdate = datetime.now()
        newTransaction.save()

        # Now set the wallet, reputation and numtrans calues for the new user
        newUser.reload()
        newUserReceived=Transaction.objects(giver=newUser.id).sum('amount')
        newUserGiven=Transaction.objects(recipient=newUser.id).sum('amount')
        numTrans=Transaction.objects(giver=newUser.id).count()+Transaction.objects(recipient=newUser.id).count()
        newUser.update(wallet=newUserReceived-newUserGiven,numtrans=numTrans, reputation=newUserGiven)
        flash(f'New user transaction ID#: {newTransaction.id} was just created.')

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
