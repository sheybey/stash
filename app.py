from flask import Flask, url_for, request, session, render_template, redirect, flash, get_flashed_messages
import os
import gnupg
import hashlib
import tempfile
app = Flask(__name__)

class DefaultConfiguration():
	APPLICATION_ROOT = "/"
	SECRET_KEY = "hello"
	UPLOAD_DIR = "uploads"

app.config.from_object(DefaultConfiguration)
app.config.from_pyfile("app.cfg", silent=True)

app.secret_key = app.config["SECRET_KEY"]

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "GET":
		sha1 = hashlib.sha1()
		sha1.update(os.urandom(32))
		secret = sha1.hexdigest()
		session["secret"] = secret
		return render_template("login.html", secret=secret)

	if "signature" not in request.form:
		flash("No signature", "error")
		return redirect(url_for("login"))

	secret = session.pop("secret", None)
	if secret is None:
		return redirect(url_for("login"))

	signature_filename = tempfile.mkstemp()[1]
	try:
		with open(signature_filename, "w") as signature:
			signature.write(request.form["signature"].encode("ascii"))
		gpg = gnupg.GPG()
		if not gpg.verify_data(signature_filename, secret):
			flash("Could not verify signature", "error")
			return redirect(url_for("login"))
		session["logged_in"] = True
		return redirect(url_for("index"))

	except UnicodeDecodeError:
		flash("Invalid signature", "error")
		return redirect(url_for("login"))
	finally:
		if os.name != "nt":
			os.unlink(signature_filename)

@app.route("/logout")
def logout():
	session["logged_in"] = False
	return redirect(url_for("index"))

@app.route("/upload", methods=["GET", "POST"])
def upload():
	if "logged_in" not in session or not session["logged_in"]:
		return redirect(url_for("login"))
	if request.method == "GET":
		return render_template("upload.html")

