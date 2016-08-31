from flask import Flask, url_for
app = Flask(__name__, instance_relative_config=True)

@app.route("/")
def index():
	return repr(app.config["APPLICATION_ROOT"])
