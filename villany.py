from app import app, db
from flask import render_template, request, redirect, session
from random import randint
from os import abort

@app.route("/question_villany/<int:questionnumber>")
def Question_villany(questionnumber: int):
    amount_of_villany = db.session.execute("SELECT COUNT(*) FROM Questions_villany").fetchone()[0]
    questo = randint(1, amount_of_villany)
    questionsqlcmd = "SELECT question_villany FROM Questions_villany WHERE id=:questo"
    question = db.session.execute(questionsqlcmd, {"questo":questo}).fetchone()[0]
    secsqlcomd = "SELECT option_villany, truth FROM Options_villany WHERE questo=:questo"
    answers = db.session.execute(secsqlcomd, {"questo":questo}).fetchall()
    return render_template("Villain_page.html", question=question, answers=answers, questionnumber=questionnumber)

@app.route("/villany_question_check", methods=["POST"])
def Villany_question_check():
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
        return redirect("/villany_finished")
    direction = "/question_villany/"+str(ordernumber)
    return redirect(direction)

@app.route("/villany_finished")
def villany_finished():
    return render_template("finish.html")
