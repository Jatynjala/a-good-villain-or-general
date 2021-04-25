from app import app, db
from flask import render_template, request, redirect, session
from random import randint
from os import abort

@app.route("/question_war/<int:questionnumber>")
def Question_war(questionnumber: int):
    amount_of_war = db.session.execute("SELECT COUNT(*) FROM Questions_war").fetchone()[0]
    questi = randint(1, amount_of_war)
    questionsqlcmd = "SELECT question_war FROM Questions_war WHERE id=:questi"
    question = db.session.execute(questionsqlcmd, {"questi":questi}).fetchone()[0]
    secsqlcomd = "SELECT option_war, truth FROM Options_war WHERE questi=:questi"
    answers = db.session.execute(secsqlcomd, {"questi":questi}).fetchall()
    return render_template("War_page.html", question=question, answers=answers, questionnumber=questionnumber)

@app.route("/war_question_check", methods=["POST"])
def War_question_check():
    if session["session_number"] != request.form["session_number"]:
        abort(403)
    username = session["username"]
    if request.form["answer"] == "1":
        successes = db.session.execute("SELECT successes FROM Users WHERE username=:username", {"username":username}).fetchone()[0]+1
        rightanswer = "UPDATE Users SET successes=:successes WHERE username=:username"
        db.session.execute(rightanswer, {"successes":successes, "username":username})
        db.session.commit()
    ordernumber = int(request.form["ordernumber"])
    ordernumber += 1
    if ordernumber > 3:
        newtries = db.session.execute("SELECT tries FROM Users WHERE username=:username", {"username":username}).fetchone()[0]+1
        questionend = "UPDATE Users SET tries=:newtries WHERE username=:username"
        db.session.execute(questionend, {"newtries":newtries, "username":username})
        db.session.commit()
        return redirect("/war_finished")
    direction = "/question_war/"+str(ordernumber)
    return redirect(direction)

@app.route("/war_finished")
def war_finished():
    return render_template("finish.html")
