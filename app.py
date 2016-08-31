from flask import Flask, url_for, request, session, render_template, redirect,
	flash, get_flashed_messages
import hashlib
import os
import gnupg
import tempfile
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
	if "signature" not in request.form:
		return redirect(url_for(login))
	try:
		secret = get_flashed_messages()[0]
	except IndexError:
		return redirect(url_for(index))

	signature_filename = tempfile.mkstemp()[1]
	try:
		with open(signature_filename, "w") as signature:
			signature.write(request.form["signature"].encode("ascii"))
		gpg = gnupg.GPG()
		verified = gpg.verify_data(signature_filename, secret)
		if not verified:
			flash("Could not verify signature", "error")
			return redirect(url_for(login))
		session["logged_in"] = True
		return redirect(url_for(index))

	except UnicodeDecodeError:
		flash("Invalid signature", "error")
		return redirect(url_for(login))
	finally:
		os.unlink(signature_filename)
	


@app.route("/logout")
def logout():
	session["logged_in"] = False
	session.pop("secret", None)
	return redirect(url_for(index))