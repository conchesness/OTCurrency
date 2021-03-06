from app.routes import app
from flask import render_template, session, redirect, request, flash, url_for
from app.Data import User, Transaction, Role

# @app.route('/nogoogid')
# def nogoogid():
#     nogoogids=User.objects(googleid=None)
#     for user in nogoogids:
#         user.delete()
#     nogoogids=User.objects(googleid=None)
#
#     return render_template('scripts.html', users=nogoogids)

# @app.route('/fandlname')
# def fandlname():
#     if session.get("access_token"):
#         users=User.objects()
#         for user in users:
#             space=user.name.find(" ")
#             fname=user.name[0:space]
#             lname=user.name[space+1:]
#             flash(f'{user.name} {fname} {lname}')
#             editUser=User.objects.get(name=user.name)
#             editUser.update(fname=fname,lname=lname)
#
#     return render_template('scripts.html')

# @app.route('/addrole')
# def addrole():
#     if not session.get("access_token"):
#         return redirect(url_for('login'))
#     teacher=Role.objects.get(name='teacher')
#     student=Role.objects.get(name='student')
#     users=User.objects()
#     for user in users:
#         if user.email and user.email[:1] == 's':
#             user.update(role=student.id)
#         elif user.email and user.email[:1] != 's':
#             user.update(role=teacher.id)
#         user.reload()
#         flash(f'{user.name} email is {user.email} role is {user.role.name}')
#
#
#     return render_template('scripts.html')


@app.route('/deletenegtrans')
def deletenegtrans():
    if not session.get("access_token"):
        return redirect(url_for('login'))
    else:
        # Transaction.objects(amount__lte = 0).delete()
        ltzero=Transaction.objects(amount__lte = 0).count()
        flash(f'{ltzero}')
        Transaction.objects(amount__lte = 0).delete()
        ltzero=Transaction.objects(amount__lte = 0).count()
        flash(f'{ltzero}')

        return render_template('scripts.html')

@app.route('/updatewallets')
def updatewallets():
    #update transaction values on user objects
    if not session.get("access_token"):
        return redirect(url_for('login'))
    if not session['role'] == 'admin':
        return redirect('/')
    else:
        allUsers=User.objects()
        for user in allUsers:
            user.reload()
            amtReceived = Transaction.objects(recipient=user.id).sum('amount')
            amtGiven = Transaction.objects(giver=user.id).sum('amount')
            numReceived = Transaction.objects(recipient=user.id).count()
            numGiven = Transaction.objects(giver=user.id).count()
            numtrans=numReceived+numGiven
            wallet=amtReceived+amtGiven
            user.update(wallet=wallet,reputation=amtGiven,numtrans=numtrans)
        return redirect(url_for('users'))

# @app.route('/increasewallets')
# def increasewallets():
#     allUsers = User.objects()
#     giver = User.objects.get(googleid="999999999")
#     for user in allUsers:
#         newTransaction = Transaction()
#         newTransaction.recipient = user.id
#         newTransaction.giver = giver.id
#         newTransaction.amount = 40
#         newTransaction.reason = 'Top Up'
#         newTransaction.category = 'Top Up'
#         newTransaction.save()
#         flash(f'{giver.name} gave 40 to {user.name}')
#
#     return render_template('scripts.html')
