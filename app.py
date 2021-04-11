from flask import Flask
from flask import render_template, request, redirect, session
from os import getenv, urandom
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/start")
def start():
    return render_template("start.html")

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

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register_check", methods=["POST"])
def register_check():
    username = request.form["username"]
    password = request.form["password"]
    if len(username)<8:
        return redirect("/register_fail")
    if len(password)<8:
        return redirect("/register_fail")
    hash_value = generate_password_hash(password)
    firstsqlcmd = "SELECT username FROM Users WHERE username=:username"
    result = db.session.execute(firstsqlcmd, {"username":username})
    user = result.fetchone()
    if user != None:
        return redirect("/register_fail")
    secondsql = "SELECT pasword FROM Users WHERE pasword=:hash_value"
    result = db.session.execute(secondsql, {"hash_value":hash_value})
    user = result.fetchone()
    if user != None:
        return redirect("/register_fail")
    sqlcmd = "INSERT INTO Users (username, pasword, status, tries, successes) VALUES (:username, :password, 'user', 0, 0)"
    db.session.execute(sqlcmd, {"username":username, "password":hash_value})
    db.session.commit()
    session["username"] = username
    session["session_number"] = urandom(16).hex()
    return redirect("/main")

@app.route("/register_fail")
def register_fail():
    return render_template("register_fail.html")

@app.route("/main")
def main():
    cmd = "SELECT tries, successes FROM Users WHERE username=:username"
    username = session["username"]
    result = db.session.execute(cmd, {"username":username})
    user = result.fetchone()
    tries = user[0]
    rights = user[1]
    average = 0
    if tries != 0:
        average = rights/tries
    return render_template("main.html", average=average, username=username)

@app.route("/log_out")
def log_out():
    del session["username"]
    del session["session_number"]
    return redirect("/start")
