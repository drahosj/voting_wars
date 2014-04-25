from flask import Flask, render_template
from flask import request, redirect
import random
from db import db_session, init_db
from models import TeamScore
from sqlalchemy import desc

init_db()

app = Flask(__name__)

@app.route("/<teamname>/plus1")
def onepoint(teamname):
    q = db_session.query(TeamScore).filter(TeamScore.teamName == teamname)
    r = q.all()
    newScore = r[0].score + 1
    q.update({TeamScore.score : newScore})
    print r[0]
    print newScore
    db_session.commit()
    return redirect("/")
    #return "Team %s new score %d" % (teamname, newScore)

@app.route("/<teamname>/plus5")
def fivepoint(teamname):
    q = db_session.query(TeamScore).filter(TeamScore.teamName == teamname)
    r = q.all()
    newScore = r[0].score + 5
    q.update({TeamScore.score : newScore})
    print r[0]
    print newScore
    db_session.commit()
    return redirect("/")
    #return "Team %s new score %d" % (teamname, newScore)

@app.route("/<teamname>/plus50")
def fiftypoint(teamname):
##needs to check secret against stored secret in db##
    q = db_session.query(TeamScore).filter(TeamScore.teamName == teamname)
    r = q.all()
    
    provided_secret = request.args.get('secret');

    new_secret = random.randrange(100)


    if r[0].secret != int(provided_secret):
        q.update({TeamScore.secret : new_secret})
        return redirect("/")
#        return "Wrong Secret! (provided %s, expected %d)" % (provided_secret, r[0].secret)

    newScore = r[0].score + 50
    q.update({TeamScore.score : newScore, TeamScore.secret : new_secret})
    print r[0]
    print newScore
    db_session.commit()
    return redirect("/")
    #return "Team %s new score %d" % (teamname, newScore)

@app.route("/<teamname>/votefor")
def votefor(teamname):
###put secret in db and render in template###
    q = db_session.query(TeamScore).filter(TeamScore.teamName == teamname)
    secret = random.randrange(100)
    q.update({TeamScore.secret : secret})
    db_session.commit()
    return render_template("vote.html", TEAMNAME=teamname, SECRET=secret)

@app.route("/supersecret/create/<teamname>")
def create(teamname):
    add = TeamScore(team=teamname, score=0)
    db_session.add(add)
    db_session.commit()
    return "Team %s created" % teamname

@app.route("/supersecret/delete/<teamname>")
def delete(teamname):
    q = db_session.query(TeamScore).filter(TeamScore.teamName == teamname)
    print q
    print q.all()
    q.delete()
    db_session.commit()
    return "Team %s deleted" % teamname

@app.route("/")
def scores():
    teamScores = db_session.query(TeamScore).order_by(desc(TeamScore.score)).all()
    print teamScores
    return render_template("scoreboard.html", SCORES=teamScores)


if __name__ == "__main__":
    app.debug = True
    app.run("0.0.0.0")
