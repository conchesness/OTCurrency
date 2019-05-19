from app.routes import app
from flask import render_template, session, request, redirect, flash
from app.Forms import JobForm
from app.Data import Transaction, User, Job
import requests
from datetime import datetime

@app.route('/jobs')
def jobs():
    allJobs = Job.objects.order_by('+createdatetime')

    return render_template('jobs.html', allJobs=allJobs)

@app.route('/newjob', methods=['GET', 'POST'])
def newjob():
    form = JobForm()
    currUserObj = User.objects.get(name=session['displayName'])

    if request.method == 'POST' and form.validate_on_submit():
        newJob = Job(requestedby=currUserObj,title=form.title.data, hours=form.hours.data, desc=form.desc.data, createdatetime=datetime.today())
        newJob.save()
        return redirect('/jobs')

    return render_template('jobform.html', form=form)

@app.route('/editjob/<jobID>', methods=['GET', 'POST'])
def editjob(jobID):
    form = JobForm()
    currUserObj = User.objects.get(name=session['displayName'])
    editJob = Job.objects.get(pk=jobID)

    if request.method == 'POST' and form.validate_on_submit():
        if session['displayName'] == editJob.requestedby.name:
            editJob.reload()
            editJob.update(title=form.title.data, hours=form.hours.data, desc=form.desc.data)
            flash("Job was edited.")

        else:
            flash("You can't edit a job you didn't post.")
        return redirect('/jobs')

    form.title.data = editJob.title
    form.hours.data = editJob.hours
    form.desc.data = editJob.desc

    return render_template('jobform.html', form=form)

@app.route('/deletejob/<jobID>')
def deletejob(jobID):
    currUserObj = User.objects.get(name=session['displayName'])
    deleteJob = Job.objects.get(pk=jobID)
    if session['displayName'] == deleteJob.requestedby.name:
        deleteJob.delete()
        flash("Job successfully deleted.")
    else:
        flash("You can't delete a job you didn't create.")
    return redirect('/jobs')
