from flask import Flask, url_for
app = Flask(__name__, instance_relative_config=True)

class DefaultConfiguration():
	APPLICATION_ROOT = "/"

app.config.from_object(DefaultConfiguration)
app.config.from_pyfile("app.cfg", silent=True)

@app.route("/")
def index():
	return repr(app.config["APPLICATION_ROOT"])
