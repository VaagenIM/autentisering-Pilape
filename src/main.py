from flask import Flask, render_template, request, redirect, session, url_for
from user import User, get_user
from quote import quote, get_quote_list, delete_quote, get_quote_username, get_quote_content, update_quote_content
from decorators import login_required
import os

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"] if "FLASK_SECRET_KEY" in os.environ else "3hfdsajfhskruk"

@app.route("/")
def index() -> str:
    return render_template("index.html")

def session_login(user: User) -> None:
    session["user"] = user
    session["logged_in"] = True



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



@app.route("/log-out")
def log_out():
    session.clear()
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



@app.route("/profile", methods=["GET"])
def get_profile():
    return render_template("profile.html")



@app.route("/quotes")
@login_required
def get_quotes() -> str:
    return render_template("quotes.html", quotes=get_quote_list(), username=session["user"]["username"])

@app.route("/quotes", methods=["POST"])
@login_required
def post_quotes():
    content: str = request.form["content"]
    quote(content, session["user"].get("username"))

    return redirect(url_for("get_quotes"))

@app.route("/quotes/delete/<int:id>", methods=["POST"])
@login_required
def delete_quotes(id: int):
    if get_quote_username(id) != session["user"]["username"]:
        return "403 Forbidden", 403

    delete_quote(id)
    return redirect(url_for("get_quotes"))

@app.route("/quotes/edit/<int:id>", methods=["GET"])
@login_required
def get_quote_editor(id: int):
    if get_quote_username(id) != session["user"]["username"]:
        return "403 Forbidden", 403

    return render_template("edit.html", id=id, old_content=get_quote_content(id))

@app.route("/quotes/update/<int:id>", methods=["POST"])
@login_required
def update_quotes(id: int):
    if get_quote_username(id) != session["user"]["username"]:
        return "403 Forbidden", 403

    update_quote_content(request.form["new_content"], id)

    return redirect(url_for("get_quotes"))



def run(debug: bool = False) -> None:
    app.run(debug=debug)

# Dev mode:
if __name__ == "__main__":
    run(debug=True)
