from .misc import graph
from app.routes import app
from flask import render_template


@app.route("/stats")
def stats():
    graph()
    return render_template("stats.html")

