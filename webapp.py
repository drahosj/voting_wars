from flask import Flask, render_template
from flask import request, redirect
from redis import StrictRedis
import random

r = StrictRedis(host='localhost', port=6379, db=0)

app = Flask(__name__)

valid_teams = []

@app.route("/<teamname>/plus1")
def onepoint(teamname):
    if teamname in valid_teams:
        r.incrby("score:%s" % teamname, 1)
    return redirect("/")

@app.route("/<teamname>/plus5")
def fivepoint(teamname):
    if teamname in valid_teams:
        r.incrby("score:%s" % teamname, 5)
    return redirect("/")

@app.route("/<teamname>/plus50")
def fiftypoint(teamname):
##needs to check secret against stored secret in db##
    provided_secret = request.args.get('secret');

    new_secret = random.randrange(100)

    expected_secret = r.get("secret:%s" % teamname)

    if int(expected_secret) != int(provided_secret):
        r.set("secret:%s" % teamname, new_secret)
        print "Wrong Secret"
        return redirect("/")

    r.set("secret:%s" % teamname, new_secret)
    if teamname in valid_teams:
        r.incrby("score:%s" % teamname, 50)
    return redirect("/")

@app.route("/<teamname>/votefor")
def votefor(teamname):
###put secret in db and render in template###
    secret = random.randrange(100)
    r.set("secret:%s" % teamname, secret)
    return render_template("vote.html", TEAMNAME=teamname, SECRET=secret)

#@app.route("/supersecret/create/<teamname>")
def create(teamname):
    r.set(("score:%s" % teamname), 0)
    return "Team %s created" % teamname

#@app.route("/supersecret/delete/<teamname>")
def delete(teamname):
    r.delete(("score:%s" % teamname))
    return "Team %s deleted" % teamname


class Team():
    def __init__(self, name, score):
        self.name = name
        self.score = score
    def getScore(self):
        return int(self.score)

@app.route("/")
def scores():
    teams = []
    for teamName in r.keys("score*"):
        teamName = teamName.split(":")[1]
        newTeam = Team(teamName, r.get("score:%s" % teamName))
        teams.append(newTeam)

    teams.sort(key=Team.getScore, reverse=True)
    return render_template("scoreboard.html", TEAMS=teams)


if __name__ == "__main__":
    app.debug = True
    for i in range (1, 32):
        valid_teams.append("Team %d" % i)
        valid_teams.append("Team RED")

    print valid_teams
    app.run("0.0.0.0")

