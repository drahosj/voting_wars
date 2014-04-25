from flask import Flask, render_template
from db import db_session, init_db
from models import TeamScore
from sqlalchemy import desc

init_db()

app = Flask(__name__)

@app.route("/plus1/<teamname>")
def onepoint(teamname):
    q = db_session.query(TeamScore).filter(TeamScore.teamName == teamname)
    r = q.all()
    newScore = r[0].score + 1
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
