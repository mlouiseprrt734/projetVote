from flask import render_template

def loginpage():
    return render_template("pages/loginpage.html")

def homepage():
    return render_template("pages/homepage.html")

def navigation():
    return render_template("pages/navigation.html")

def ballotpage():
    return render_template("pages/ballotpage.html")

def resultspage():
    return render_template("pages/resultspage.html")

def organisationpage():
    return render_template("pages/organisationpage.html")

def displayTOTP():
    return render_template("pages/displayTOTP.html")