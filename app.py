from flask import Flask, request, render_template, redirect
from helpers import getData, checkDriver



app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")



@app.route("/upload", methods=["POST"])
def upload():
    results = getData(request.files["results"])
    drivers = getData(request.files["drivers"])
    data = {}
    data["results"] = results
    data["drivers"] = drivers

    for i in range(len(data["drivers"])):
        if data["drivers"][i][0] != "" and data["drivers"][i][0] != "No.":
            checkDriver(data["drivers"][i])
    return data
    return data["drivers"][2]
    return render_template("table.html", results=results, fastest_lap=results[0][fastest_lap])

