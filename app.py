from flask import Flask, request, render_template, redirect
from helpers import getData, checkDriver, getEvents, createEvent, getTracks


app = Flask(__name__)

@app.route("/")
def index():
    events = getEvents()
    return render_template("index.html", events=events)

@app.route("/createevent", methods=["GET", "POST"])
def makeevent():
    if request.method == "POST":
        createEvent(request.form)
        return redirect("/createevent")
    else: 
        tracks = getTracks()
        return render_template("createevent.html", tracks=tracks)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        results = getData(request.files["results"],"1,2")
        drivers = getData(request.files["drivers"],"2")
        data = {}
        data["meta"] = results[1]
        data["results"] = []
        data["drivers"] = drivers[0]
        for result in results[0]:
            try:
                if int(result[4]):
                    data["results"].append(result)
            except:
                continue

        for i in range(len(data["drivers"])):
            if data["drivers"][i][0] != "" and data["drivers"][i][0] != "No.":
                checkDriver(data["drivers"][i])
        return render_template("confirm.html", results=data["results"])
    else:
        events = getEvents()
        return render_template("index.html", events=events)

