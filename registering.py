from flask import render_template, request, redirect, session
from os import urandom
from werkzeug.security import generate_password_hash
from app import app, db

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
