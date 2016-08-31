from flask import Flask, url_for, session, render_template
app = Flask(__name__)

class DefaultConfiguration():
	APPLICATION_ROOT = "/"

app.config.from_object(DefaultConfiguration)
app.config.from_pyfile("app.cfg", silent=True)

@app.route("/")
def index():
	return render_template("index.html", app=app)
