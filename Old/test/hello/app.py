from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cake")
def boobs():
    enterprise = request.args.get("picard", "moron who forgot to enter a name in the last page")
    return render_template("greet.html", tiefighter=enterprise)
