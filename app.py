from flask import Flask, request, render_template, redirect
from helpers import getData, checkDriver, getEvents, createEvent, getTracks, uploadResults, getDrivers, getResult, getSessionResults, getSessions2, getEventsUpload


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
        event = {}
        event["event"] = request.form.get("event")
        print(event)
        event["session"] = request.form.get("session")
        return render_template("confirm.html", results=data["results"], event=event)
    else:
        events = getEventsUpload()
        return render_template("uploadresults.html", events=events)

@app.route("/confirmed", methods=["POST"]) 
def confirmed():
    uploadResults(request.form)
    return redirect("/upload")

@app.route("/getEvents") 
def sessions():
    session_id = request.args.get("event")
    return getEvents()

@app.route("/getdriver") 
def fetchDriver():
    return getDrivers()

@app.route("/getresult") 
def fetchResult():
    return getResult(request.args.get("driver_id"))

@app.route("/getsessionresults") 
def getsessionsresults():
    return getSessionResults(request.args.get("session_id"))


@app.route("/events") 
def sessionResults():
    return render_template("result.html", events=getEvents())

@app.route("/sessions") 
def getsessions():
    print(request.args.get("event"))
    results = getSessions2(request.args.get("event"))
    return results



@app.route("/driver") 
def drivercompare():
    return render_template("DRIVERCOMPARE.html")