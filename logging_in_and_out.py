from flask import render_template, request, redirect, session
from os import urandom
from werkzeug.security import check_password_hash
from app import app, db

@app.route("/log_in")
def log_in():
    return render_template("log_in.html")

@app.route("/log_in_check", methods=["POST"])
def log_in_check():
    username = request.form["username"]
    password = request.form["password"]
    sqlcommand = "SELECT pasword FROM Users WHERE username=:username"
    result = db.session.execute(sqlcommand, {"username":username})
    user = result.fetchone()
    if user == None:
        return redirect("/log_in_fail")
    else:
        hv = user[0]
        if check_password_hash(hv,password):
            session["username"] = username
            session["session_number"] = urandom(16).hex()
            return redirect("/main")
        else:
            return redirect("/log_in_fail")

@app.route("/log_in_fail")
def log_in_fail():
    return render_template("log_in_fail.html")

@app.route("/log_out")
def log_out():
    del session["username"]
    del session["session_number"]
    return redirect("/start")
