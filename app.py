from flask import Flask, url_for, request, session, render_template
import hashlib
app = Flask(__name__)

class DefaultConfiguration():
	APPLICATION_ROOT = "/"

app.config.from_object(DefaultConfiguration)
app.config.from_pyfile("app.cfg", silent=True)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "GET":
		md5 = hashlib.md5()
		md5.update(os.urandom(32))
		secret = md5.hexdigest()
		return render_template("login.html", secret=secret)
	return "would validate here, but..."

@app.route("/logout")
def logout():
	session["logged_in"] = False
	session.pop("secret", None)
	return redirect(url_for(index))