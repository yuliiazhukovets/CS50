import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

from helpers import login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///squash.db")

@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email"):
            return render_template("error.html", message = "Please, provide your email.")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.html", message = "Please, provide your password.")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hashed_pass"], request.form.get("password")):
            return render_template("error.html", message = "Please, provide valid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/about")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        # error checking
        # if the user name is even there
        if not request.form.get("email"):
            return render_template("error.html", message = "Please, provide valid email")

        # if the password is there
        if not request.form.get("password"):
            return render_template("error.html", message = "Please, provide password")

        # if the password match
        if request.form.get("password") != request.form.get("confirmation"):
            return render_template("error.html", message = "Please, provide matching passwords")

        check = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))
        if len(check) != 0:
            return render_template("error.html", message = "An account with this email already exists. Please, provide a new email or log in the exsting account")

        # hash the password
        hashed_pass = generate_password_hash(request.form.get("password"))
        # add user to the database
        user_id = db.execute("INSERT INTO users (email, hashed_pass, first_name, last_name ) VALUES(?, ?, ?, ?)", request.form.get("email"), hashed_pass, request.form.get("f_name"), request.form.get("l_name"))

        session["user_id"] = user_id

        return redirect("/about")

    else:
        return render_template("register.html")

@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    if request.method == "POST":
        # get name of the team from the post request
        team = request.form['team']
        # run SQL query to get information about the team
        teams = db.execute("SELECT * FROM teams WHERE name LIKE ?", "%" + team + "%")
        #run SQL query to get a name of the current user
        name = db.execute("SELECT first_name FROM users WHERE id = ?", session["user_id"])
        # error checking - if the user provided a valid name of the team
        if len(teams) == 0:
            return render_template("error.html", message = "Please, provide a valid team name")
        fav = "favorites"
        info ="team_info"
        # adding unique ids for the forms in html file
        for i in range(len(teams)):
            fav_id = fav + str(i)
            teams[i]["favorite_id"] = fav_id
            info_id = info + str(i)
            teams[i]["team_info_id"] = info_id
        return render_template("results.html", teams = teams, username = name[0]['first_name'])
    else:
        # run SQL query to get information about all teams
        data = db.execute("SELECT * FROM teams")
        fav = "favorites"
        info ="team_info"
        # generating unique ids for the forms in html file
        for i in range(len(data)):
            fav_id = fav + str(i)
            data[i]["favorite_id"] = fav_id
            info_id = info + str(i)
            data[i]["team_info_id"] = info_id
        name = db.execute("SELECT first_name FROM users WHERE id = ?", session["user_id"])
        return render_template("search.html", teams = data, username = name[0]['first_name'])

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/ranked", methods=["GET", "POST"])
def search_ranked():
    if request.method == "POST":
        # get name of the team from the post request
        team = request.form['team']
        # run SQL query to get information about the team
        teams = db.execute("SELECT * FROM teams WHERE name LIKE ?", "%" + team + "%")
        #run SQL query to get a name of the current user
        name = db.execute("SELECT first_name FROM users WHERE id = ?", session["user_id"])
        # error checking - if the user provided a valid name of the team
        if len(teams) == 0:
            return render_template("error.html", message = "Please, provide a valid team name")
        fav = "favorites"
        info ="team_info"
        # adding unique ids for the forms in html file
        for i in range(len(teams)):
            fav_id = fav + str(i)
            teams[i]["favorite_id"] = fav_id
            info_id = info + str(i)
            teams[i]["team_info_id"] = info_id
        return render_template("results.html", teams = teams, username = name[0]['first_name'])
    else:
        # getting name of the user
        name = db.execute("SELECT first_name FROM users WHERE id = ?", session["user_id"])
        # run SQL query to get information about all teams and ordering by the rank
        teams = db.execute("SELECT * FROM teams ORDER BY rank ASC, teams.women_men DESC")
        fav = "favorites"
        info ="team_info"
        # generating ids for the forms in the html file
        for i in range(len(teams)):
            fav_id = fav + str(i)
            teams[i]["favorite_id"] = fav_id
            info_id = info + str(i)
            teams[i]["team_info_id"] = info_id
        return render_template("search.html", teams = teams, username = name[0]['first_name'])


@app.route("/favorites", methods=["GET", "POST"])
@login_required
def favorites():
    if request.method == "POST":
        # getting name and gender of the saved team
        namef = request.form.get("name1")
        genderf = request.form["gender1"]
        # run SQL query to get an id of the favorited team
        team = db.execute("SELECT id FROM teams WHERE name = ? AND women_men = ?", namef, genderf)
        # checking if a user has already saved this team before
        check = db.execute("SELECT * FROM favorites WHERE team_id = ?", team[0]["id"])
        if len(check) == 0:
            # if there is no such team - run SQL query to insert this team in the table
            db.execute("INSERT INTO favorites(user_id, team_id) VALUES(?, ?)", session["user_id"], team[0]["id"])
        return redirect("/search")
    else:
        # run SQL query to get the name of the current user
        name = db.execute("SELECT first_name FROM users WHERE id = ?", session["user_id"])
        # run SQL query to get ids of all teams that this user has previously saved
        teams_id = db.execute("SELECT team_id FROM favorites WHERE user_id = ?", session["user_id"])
        teams_info=[]
        info ="team_info"
        # running a loop to add all the favorites teams' info to one list
        for i in range(len(teams_id)):
            no = teams_id[i]["team_id"]
            temp = db.execute("SELECT * FROM (SELECT * FROM teams) WHERE id = ?", no)
            teams_info.append(temp[0])
            info_id = info + str(i)
            teams_info[i]["team_info_id"] = info_id
        return render_template("favorites.html", username = name[0]['first_name'], teams = teams_info)

@app.route("/team_info", methods=["POST"])
@login_required
def team():
    # getting name and gender of the team
    name = request.form.get("name")
    gender = request.form["gender"]
    # running SQL query to get team's info, ranks, coach and link
    team = db.execute("SELECT * FROM teams WHERE name = ? AND women_men = ?", name, gender)
    coach = db.execute("SELECT coach FROM coaches WHERE id = ?", team[0]["id"])
    ranks = db.execute("SELECT * FROM all_ranks WHERE id = ?", team[0]["id"])
    link = db.execute("SELECT * FROM links WHERE id = ?", team[0]["id"])
    return render_template("info.html", name = name, gender = gender, team_type = team[0]["varsity_club"], link = link[0]["link"], ranks = ranks, coach = coach[0]["coach"])

@app.route("/map", methods=["GET"])
@login_required
def map_page():
    # returning the template of the map
    return render_template("index.html")


@app.route("/filter_men", methods=["GET", "POST"])
@login_required
def filter_men():
    if request.method == "POST":
        # get name of the team from the post request
        team = request.form['team']
        # run SQL query to get information about the team
        teams = db.execute("SELECT * FROM teams WHERE name LIKE ?", "%" + team + "%")
        #run SQL query to get a name of the current user
        name = db.execute("SELECT first_name FROM users WHERE id = ?", session["user_id"])
        # error checking - if the user provided a valid name of the team
        if len(teams) == 0:
            return render_template("error.html", message = "Please, provide a valid team name")
        fav = "favorites"
        info ="team_info"
        # adding unique ids for the forms in html file
        for i in range(len(teams)):
            fav_id = fav + str(i)
            teams[i]["favorite_id"] = fav_id
            info_id = info + str(i)
            teams[i]["team_info_id"] = info_id
        return render_template("results.html", teams = teams, username = name[0]['first_name'])
    else:
        # run SQL query to a name of the current user
        name = db.execute("SELECT first_name FROM users WHERE id = ?", session["user_id"])
        # run SQL query to get info about all men teams
        teams = db.execute("SELECT * FROM teams WHERE women_men = 'Men' ORDER BY women_men DESC")
        fav = "favorites"
        info ="team_info"
        # generating unique ids for forms in the html form
        for i in range(len(teams)):
            fav_id = fav + str(i)
            teams[i]["favorite_id"] = fav_id
            info_id = info + str(i)
            teams[i]["team_info_id"] = info_id
        return render_template("search.html", teams = teams, username = name[0]['first_name'])

@app.route("/filter_women")
@login_required
def filter_women():
    if request.method == "POST":
        # get name of the team from the post request
        team = request.form['team']
        # run SQL query to get information about the team
        teams = db.execute("SELECT * FROM teams WHERE name LIKE ?", "%" + team + "%")
        #run SQL query to get a name of the current user
        name = db.execute("SELECT first_name FROM users WHERE id = ?", session["user_id"])
        # error checking - if the user provided a valid name of the team
        if len(teams) == 0:
            return render_template("error.html", message = "Please, provide a valid team name")
        fav = "favorites"
        info ="team_info"
        # adding unique ids for the forms in html file
        for i in range(len(teams)):
            fav_id = fav + str(i)
            teams[i]["favorite_id"] = fav_id
            info_id = info + str(i)
            teams[i]["team_info_id"] = info_id
        return render_template("results.html", teams = teams, username = name[0]['first_name'])
    else:
        # run SQL query to get a name of the current user
        name = db.execute("SELECT first_name FROM users WHERE id = ?", session["user_id"])
        # run SQL query to get info about all women teams
        teams = db.execute("SELECT * FROM teams WHERE NOT women_men = 'Men' ORDER BY women_men DESC")
        fav = "favorites"
        info ="team_info"
        # generating unique ids for forms in the html page
        for i in range(len(teams)):
            fav_id = fav + str(i)
            teams[i]["favorite_id"] = fav_id
            info_id = info + str(i)
            teams[i]["team_info_id"] = info_id
        return render_template("search.html", teams = teams, username = name[0]['first_name'])

@app.route("/filter_varsity")
@login_required
def filter_varsity():
    if request.method == "POST":
        # get name of the team from the post request
        team = request.form['team']
        # run SQL query to get information about the team
        teams = db.execute("SELECT * FROM teams WHERE name LIKE ?", "%" + team + "%")
        #run SQL query to get a name of the current user
        name = db.execute("SELECT first_name FROM users WHERE id = ?", session["user_id"])
        # error checking - if the user provided a valid name of the team
        if len(teams) == 0:
            return render_template("error.html", message = "Please, provide a valid team name")
        fav = "favorites"
        info ="team_info"
        # adding unique ids for the forms in html file
        for i in range(len(teams)):
            fav_id = fav + str(i)
            teams[i]["favorite_id"] = fav_id
            info_id = info + str(i)
            teams[i]["team_info_id"] = info_id
        return render_template("results.html", teams = teams, username = name[0]['first_name'])
    else:
        # run SQL query to get a name of the current user
        name = db.execute("SELECT first_name FROM users WHERE id = ?", session["user_id"])
        # run SQL query to get info about teams that are Varsity
        teams = db.execute("SELECT * FROM teams WHERE varsity_club = 'Varsity'")
        fav = "favorites"
        info ="team_info"
        for i in range(len(teams)):
            fav_id = fav + str(i)
            teams[i]["favorite_id"] = fav_id
            info_id = info + str(i)
            teams[i]["team_info_id"] = info_id
        return render_template("search.html", teams = teams, username = name[0]['first_name'])

@app.route("/filter_club")
@login_required
def filter_club():
    if request.method == "POST":
        # get name of the team from the post request
        team = request.form['team']
        # run SQL query to get information about the team
        teams = db.execute("SELECT * FROM teams WHERE name LIKE ?", "%" + team + "%")
        #run SQL query to get a name of the current user
        name = db.execute("SELECT first_name FROM users WHERE id = ?", session["user_id"])
        # error checking - if the user provided a valid name of the team
        if len(teams) == 0:
            return render_template("error.html", message = "Please, provide a valid team name")
        fav = "favorites"
        info ="team_info"
        # adding unique ids for the forms in html file
        for i in range(len(teams)):
            fav_id = fav + str(i)
            teams[i]["favorite_id"] = fav_id
            info_id = info + str(i)
            teams[i]["team_info_id"] = info_id
        return render_template("results.html", teams = teams, username = name[0]['first_name'])
    else:
        # run SQL query to get a name of the current user
        name = db.execute("SELECT first_name FROM users WHERE id = ?", session["user_id"])
        # run SQL query to get info about all the teams that are Clun
        teams = db.execute("SELECT * FROM teams WHERE varsity_club = 'Club'")
        fav = "favorites"
        info ="team_info"
        # generating unique ids for the forms in the html file
        for i in range(len(teams)):
            fav_id = fav + str(i)
            teams[i]["favorite_id"] = fav_id
            info_id = info + str(i)
            teams[i]["team_info_id"] = info_id
        return render_template("search.html", teams = teams, username = name[0]['first_name'])

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template("error.html", message = "Internal Error")


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)