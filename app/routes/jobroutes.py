from app.routes import app
from flask import render_template, session, request, redirect, flash, url_for
from app.Forms import JobForm
from app.Data import Transaction, User, Job
import requests
from datetime import datetime

@app.route('/jobs')
def jobs():
    if not session.get("access_token"):
        return redirect("/oauth2callback")
    allJobs = Job.objects.order_by('+createdatetime')

    return render_template('jobs.html', allJobs=allJobs)

@app.route('/job/<jobID>')
def job(jobID):
    if not session.get("access_token"):
        return redirect("/oauth2callback")
    job = Job.objects.get(pk=jobID)

    return render_template('job.html', job=job)


@app.route('/newjob', methods=['GET', 'POST'])
def newjob():
    if not session.get("access_token"):
        return redirect("/oauth2callback")
    form = JobForm()
    currUserObj = User.objects.get(name=session['displayName'])

    if request.method == 'POST' and form.validate_on_submit():
        newJob = Job(requestedby=currUserObj,
                     title=form.title.data,
                     difficulty=form.difficulty.data,
                     desc=form.desc.data,
                     createdatetime=datetime.today())
        newJob.save()
        return redirect(f'/job/{newJob.id}')

    return render_template('jobform.html', form=form)

@app.route('/editjob/<jobID>', methods=['GET', 'POST'])
def editjob(jobID):
    if not session.get("access_token"):
        return redirect("/oauth2callback")
    form = JobForm()
    currUserObj = User.objects.get(name=session['displayName'])
    editJob = Job.objects.get(pk=jobID)

    if request.method == 'POST' and form.validate_on_submit():
        if session['displayName'] == editJob.requestedby.name:
            editJob.reload()
            editJob.update(title=form.title.data, difficulty=form.difficulty.data, desc=form.desc.data)
            flash("Job was edited.")

        else:
            flash("You can't edit a job you didn't post.")
        return redirect(f'/job/{editJob.id}')

    form.title.data = editJob.title
    form.difficulty.data = editJob.difficulty
    form.desc.data = editJob.desc

    return render_template('jobform.html', form=form)

@app.route('/deletejob/<jobID>')
def deletejob(jobID):
    if not session.get("access_token"):
        return redirect("/oauth2callback")
    currUserObj = User.objects.get(name=session['displayName'])
    deleteJob = Job.objects.get(pk=jobID)
    if session['displayName'] == deleteJob.requestedby.name:
        deleteJob.delete()
        flash("Job successfully deleted.")
    else:
        flash("You can't delete a job you didn't create.")
    return redirect('/jobs')

@app.route('/volunteer/<jobID>/<un>')
@app.route('/volunteer/<jobID>')
def volunteer(jobID, un="0"):
    if not session.get("access_token"):
        return redirect("/oauth2callback")


    job=Job.objects.get(pk=jobID)
    volunteer=User.objects.get(googleid=session["googleID"])


    if un == "0":
        if volunteer.googleid == job.requestedby.id:
            flash(f"You can't volunteer for a job that you created")
            return redirect(f'/job/{job.id}')
        job.update(claimedby=volunteer.id)
    elif un == "1" and job.claimedby.googleid == session['googleID']:
        job.update(claimedby=None)
        return redirect('/jobs')

    return redirect(f'/job/{job.id}')
