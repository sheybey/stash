from flask import Flask, url_for, request, session, render_template, \
	redirect, flash, get_flashed_messages, send_from_directory
from werkzeug.utils import secure_filename
import os
import gnupg
import hashlib
import tempfile

app = Flask(__name__)

class DefaultConfiguration(object):
	SECRET_KEY = "hello"
	UPLOAD_DIR = os.path.join(app.root_path, "uploads")
	PROTECTED_NAMES = [".htaccess"]
	GNUPG_CONF = {}

app.config.from_object(DefaultConfiguration)
app.config.from_pyfile("app.cfg", silent=True)

app.secret_key = app.config["SECRET_KEY"]
if not os.path.isdir(app.config["UPLOAD_DIR"]):
	os.makedirs(app.config["UPLOAD_DIR"], 0o755)

def human_size(size):
	k = 1024.0
	m = k * 1024
	g = m * 1024
	if size > g:
		return "{} GiB".format(round(size / g, 2))
	if size > m:
		return "{} MiB".format(round(size / m, 2))
	if size > k:
		return "{} KiB".format(round(size / k, 2))
	return "{} bytes".format(size)

@app.route("/")
def index():
	return render_template("index.html", files=[
		{
			"name": name,
			"size": human_size(os.stat(
				os.path.join(app.config["UPLOAD_DIR"], name)
			).st_size)
		}
		for name in os.listdir(app.config["UPLOAD_DIR"])
		if name not in app.config["PROTECTED_NAMES"]
	])

@app.route("/login", methods=["GET", "POST"])
def login():
	if session.get("logged_in", False):
		return redirect(url_for("index"))

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

	signature_fd, signature_filename = tempfile.mkstemp()
	try:
		with os.fdopen(signature_fd, "w") as signature:
			signature.write(request.form["signature"].encode("ascii"))
		gpg = gnupg.GPG(**app.config["GNUPG_CONF"])
		if not gpg.verify_data(signature_filename, secret):
			flash("Could not verify signature", "error")
			return redirect(url_for("login"))
		session["logged_in"] = True
		return redirect(url_for("index"))

	except UnicodeDecodeError:
		flash("Invalid signature", "error")
		return redirect(url_for("login"))
	finally:
		try: os.close(signature_fd)
		except OSError: pass
		finally: os.unlink(signature_filename)

@app.route("/logout")
def logout():
	session["logged_in"] = False
	return redirect(url_for("index"))

@app.route("/delete/<name>")
def delete(name):
	if not session.get("logged_in", False):
		return redirect(url_for("login"))
	f = os.path.join(app.config["UPLOAD_DIR"], name)
	if os.path.isfile(f):
		os.unlink(f)
	return redirect(url_for("index"))

@app.route("/download/<name>")
def download(name):
	if os.path.isfile(os.path.join(app.config['UPLOAD_DIR'], name)) and \
		name not in app.config["PROTECTED_NAMES"]:
		return send_from_directory(app.config['UPLOAD_DIR'],
			name, as_attachment=True)
	return "No such file", 404

@app.route("/upload", methods=["GET", "POST"])
def upload():
	if not session.get("logged_in", False):
		return redirect(url_for("login"))
	if request.method == "GET":
		return render_template("upload.html")

	if "file" not in request.files:
		flash("No file uploaded", "error")
		return redirect(url_for("upload"))

	f = request.files["file"]
	name = secure_filename(f.filename)

	if len(name) == 0:
		flash("No file uploaded", "error")
		return redirect(url_for("upload"))

	if name in app.config["PROTECTED_NAMES"]:
		flash("Invalid filename", "error")
		return redirect(url_for("upload"))

	f.save(os.path.join(app.config["UPLOAD_DIR"], name))
	return redirect(url_for("index"))