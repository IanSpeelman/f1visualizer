from flask import Flask, request, render_template, redirect
from helpers import getData, checkDriver, getEvents, createEvent, getTracks, uploadResults, getSessions, getDriver, getResult, listSessions, eventList, getSessionResults


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
        event["session"] = request.form.get("session")
        return render_template("confirm.html", results=data["results"], event=event)
    else:
        events = getEvents()
        return render_template("uploadresults.html", events=events)

@app.route("/confirmed", methods=["POST"])
def confirmed():
    uploadResults(request.form)
    return redirect("/upload")

@app.route("/sessions")
def sessions():
    session_id = request.args.get("event")
    return getSessions(session_id)
@app.route("/driver")
def driver():
    return render_template("driver.html")

@app.route("/getdriver")
def fetchDriver():
    return getDriver()

@app.route("/getresult")
def fetchResult():
    return getResult(request.args.get("driver_id"))

@app.route("/events")
def events():
    year = request.args.get("year")
    return render_template("events.html", events=eventList(year))

@app.route("/events/<id>")
def Event(id):
    return render_template("sessions.html", sessions=listSessions(id), event_id=id)

@app.route("/events/<event_id>/<session_id>")
def sessionResults(session_id, event_id):
    return getSessionResults(int(session_id))