from flask import Flask, render_template
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
    return "Team %s new score %d" % (teamname, newScore)

##disabled until redis is added##
#@app.route("/<teamname>/plus5")
def fivepoint(teamname):
    ###check secret from args against secret stored in redis###
    q = db_session.query(TeamScore).filter(TeamScore.teamName == teamname)
    r = q.all()
    newScore = r[0].score + 5
    q.update({TeamScore.score : newScore})
    print r[0]
    print newScore
    db_session.commit()
    return "Team %s new score %d" % (teamname, newScore)

@app.route("/votefor/<teamname>")
def votefor(teamname):
    ###put secret in redis###
    return renderTemplate("vote.html", TEAMNAME=teamname)

@app.route("/<teamname>/plus50")
def fiftypoint(teamname):
    q = db_session.query(TeamScore).filter(TeamScore.teamName == teamname)
    r = q.all()
    newScore = r[0].score + 50
    q.update({TeamScore.score : newScore})
    print r[0]
    print newScore
    db_session.commit()
    return "Team %s new score %d" % (teamname, newScore)

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
    app.run()
