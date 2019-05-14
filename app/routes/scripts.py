from app.routes import app
from flask import render_template, session, redirect, request, flash
from app.Data import User

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
