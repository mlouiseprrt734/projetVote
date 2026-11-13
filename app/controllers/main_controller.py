from flask import jsonify, render_template

def loginpage():
    return render_template("pages/loginpage.html")

def registerpage():
    return render_template("pages/registerpage.html")

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

def creationscrutin():
    return render_template("pages/creationscrutin.html")

def detailscrutin():
    return render_template("pages/detailscrutin.html")

def parametrescrutin():
    return render_template("pages/parametrescrutin.html")

def RGPDpage():
    return render_template("pages/RGPDpage.html")
def presence_control():
    return render_template("pages/presence_control.html")

def displayTOTP():
    return render_template("pages/displayTOTP.html")