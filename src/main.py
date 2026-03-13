# Algoritme som bruker salt & pepper X
# Krypteringsfunksjon X

# TODO: Lagring av brukerdata - Ser på det imorgen

from flask import Flask, render_template, request, redirect, session
from user import User, get_user
from decorators import login_required

app = Flask(__name__)
app.secret_key = "3hfdsajfhskruk"

@app.route("/")
def index() -> str:
    return render_template("index.html")

def session_login(user: User) -> None:
    session["user"] = user
    session["logged_in"] = True

@app.route("/log-out")
def log_out():
    session.clear()
    return redirect("/")

@app.route("/register")
def get_register() -> str:
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def post_register():

    # If username or password is empty
    if request.form["username"] == "" or request.form["password"] == "":
        return render_template("register.html", error_msg="Du må oppgi brukernavn og passord")
    
    # If username exists
    if get_user(request.form["username"]) != None:
        return render_template("register.html", error_msg="Brukernavn er tatt")

    user = User(**request.form)


    session_login(user)
    return redirect("/")

@app.route("/log-in")
def get_login() -> str:
    return render_template("login.html")

@app.route("/log-in", methods=["POST"])
def post_login():
    user = get_user(request.form.get("username").lower())
    if not user or not user.check_password(request.form.get("password")):
        return render_template("login.html", error_msg="Feil brukernavn eller passord.", form=request.form)

    session_login(user)
    return redirect("/")

@app.route("/quotes")
@login_required
def get_quotes() -> str:
    return render_template("quotes.html")

def run(debug: bool = False) -> None:
    app.run(debug=debug)

# Dev mode:
if __name__ == "__main__":
    run(debug=True)
