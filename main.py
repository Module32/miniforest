import random, string
from replit import db
from flask import Flask, render_template, request, redirect, request, make_response, url_for

def clear():
  for i in db.keys():
    del db[i]

app = Flask(
	__name__,
	template_folder='templates',
	static_folder='static'
)

ok_chars = string.ascii_letters + string.digits

@app.route('/')
def base_page():
  loggedIn = request.cookies.get("loggedIn")
  username = request.cookies.get("username")
  if loggedIn == "true":
    if username != None and username in db.keys():
      return render_template("home.html", username=username)
    else:
      return redirect("/logout")
  else:
    return render_template("home.html")

@app.route('/account')
def account():
  loggedIn = request.cookies.get("loggedIn")
  username = request.cookies.get("username")
  if loggedIn == "true":
    if username != None and username in db.keys():
      return render_template("account.html", username=username)
    else:
      return redirect("/logout")
  else:
    return render_template('noaccount.html')

@app.route('/testing')
def testing():
  return render_template("testing.html")

@app.route("/login")
def login():
  return render_template("login.html")

@app.route("/signup")
def signup():
  loggedIn = request.cookies.get("loggedIn")
  if loggedIn == "true":
    return redirect("/account")
  else:
    return render_template("signup.html")

@app.route("/loginsubmit", methods=["GET", "POST"])
def loginsubmit():
  if request.method == "POST":
    username = request.form.get("username");
    password = request.form.get("password");
    if username in db.keys():
      if password == db[username]:
        resp = make_response(render_template('readcookie.html'))
        resp.set_cookie("loggedIn", "true")
        resp.set_cookie("username", username)
        return resp
      else:
        return render_template("wrongpass.html")
    else:
      return render_template("accountnotfound.html")

@app.route("/createaccount", methods=["GET", "POST"])
def createaccount():
  if request.method == "POST":
    newusername = request.form.get("newusername")
    newpassword = request.form.get("newpassword")
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    cap_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    allchars = letters + cap_letters + numbers + ['_']
    print(newusername)
    for i in newusername:
      if i not in allchars:
        return "Username can only contain alphanumeric characters and underscores."
    if newusername in db.keys():
      return "Username taken."
    if newusername == "":
      return "Please enter a username."
    if newpassword == "":
      return "Please enter a password."
    db[newusername] = newpassword
    resp = make_response(render_template('readcookie.html'))
    resp.set_cookie("loggedIn", "true")
    resp.set_cookie("username", newusername)
    return resp

@app.route("/logout")
def logout():
  resp = make_response(render_template('readcookie.html'))
  resp.set_cookie("loggedIn", "false")
  resp.set_cookie("username", "None")
  return resp

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
  return render_template('500.html'), 500

if __name__ == "__main__":
	app.run(
		host='0.0.0.0',
		port=random.randint(2000, 9000)
	)