from flask import Flask, request, render_template, redirect
from helpers import getData



app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")



@app.route("/upload", methods=["POST"])
def upload():
    results = getData(request.files["results"])
    drivers = getData(request.files["drivers"])
    # fastest_lap = getFastestLap(results)
    data = {}
    data["results"] = results
    data["drivers"] = drivers
    return data
    return render_template("table.html", results=results, fastest_lap=results[0][fastest_lap])