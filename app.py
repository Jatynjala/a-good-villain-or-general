from flask import Flask
from flask import render_template, session, request, redirect
from os import getenv, urandom, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from random import randint

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

from registering import register, register_check, register_fail
from logging_in_and_out import log_in, log_in_check, log_in_fail, log_out
from generalship import Question_war, War_question_check, war_finished
from villany import Question_villany, Villany_question_check, villany_finished

@app.route("/start")
def start():
    return render_template("start.html")

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
