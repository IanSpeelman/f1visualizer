from random import random
import camelot
import json
import sqlite3
import os.path
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "f1visualizer.db")

# saves the document to the files folder
def saveDocument(file):
    filename = f"files/tmp/{random()}.pdf"
    file.save(filename)
    return filename

# get information from the pdf, and sort/store it in a array
def getData(file, page):
    filename = saveDocument(file)
    results = camelot.read_pdf(filename, flavor='stream', pages=page)
    try:
        meta = results[0].df.to_json()
        results = results[1].df.to_json()
        meta = json.loads(meta)
    except:
        meta = []
        results = results[0].df.to_json()
    results = json.loads(results)
    fixed_results = []
    for i in range(len(results["0"])):
        tmp = []
        for j in range(len(results)):
            tmp.append(results[str(j)][str(i)])
        fixed_results.append(tmp)
    return [fixed_results, meta]

# check if the driver exists in the database, if not add the driver to the database
def checkDriver(driver):
    connection = sqlite3.connect(db_path)
    cur = connection.cursor()   
    result = cur.execute("SELECT * FROM drivers").fetchall()
    driver_name = driver[1].split(" ")
    for i in range(len(result)):
        if driver_name[0] == result[i][3] and driver_name[1] == result[i][4]:
            return
    cur.execute("INSERT INTO drivers (driver_number, first_name, last_name, nationality, team_id) VALUES (?,?,?,?,?)", (driver[0], driver_name[0], driver_name[1], driver[2], checkTeam(driver)))
    connection.commit()
    connectDriver(checkTeam(driver), cur.lastrowid)
    connection.close()
    
# check if the team is in the database, if not, add the team to the database, regardles of existence before running, return team id
def checkTeam(team):
    connection = sqlite3.connect(db_path)
    cur = connection.cursor()   
    result = cur.execute("SELECT * FROM teams WHERE team_name = ?", [team[3]]).fetchall()
    if not len(result):
        cur.execute("INSERT INTO teams (team_name, car_name, engine, driver_1, driver_2) VALUES (?,?,?,?,?)", (team[3], 0, 0, 0, 0))
        connection.commit()
    else:
        return result[0][0]
    connection.close()
    return cur.lastrowid

def connectDriver(team_id, driver_id):
    connection = sqlite3.connect(db_path)
    cur = connection.cursor()
    result = cur.execute("SELECT * FROM teams WHERE id = ?", [team_id]).fetchone()
    if result[4] == 0:
        cur.execute("UPDATE teams SET driver_1 = ? WHERE id = ?", (driver_id, team_id))
    elif result[5] == 0:
        cur.execute("UPDATE teams SET driver_2 = ? WHERE id = ?", (driver_id, team_id))
    connection.commit()
    connection.close()
    return None

def getEvents():
    connection = sqlite3.connect(db_path)
    cur = connection.cursor()
    year = datetime.date.today().year
    events = cur.execute("SELECT * FROM events WHERE year = ?", [year]).fetchall()
    return events

def createEvent(form):
    form = form.to_dict()
    connection = sqlite3.connect(db_path)
    cur = connection.cursor()
    id = 0
    try:
        year = form["Race"].split("-")[0]
        id = cur.execute("INSERT INTO events (name, year, track_id) VALUES (?, ?, ?)", (form["name"], year, form["track"])).lastrowid
        connection.commit()
        connection.close()
    except Exception as error:
        return
    for key in form:
        try:
            if form[key].split("T")[1] != None:
                createSession(key, form[key], id)
        except Exception as error:
            pass

def createSession(type, datetime, eventid):

    connection = sqlite3.connect(db_path)
    cur = connection.cursor()
    date = datetime.split("T")[0]
    time = datetime.split("T")[1]
    try:
        cur.execute("INSERT INTO sessions (type, time, date, event_id) VALUES (?, ?, ?, ?)", 
                   (type, time, date, eventid))
        connection.commit()
        connection.close()
    except:
        pass

def getTracks():
    connection = sqlite3.connect(db_path)
    cur = connection.cursor()
    tracks = cur.execute("SELECT id, name FROM tracks").fetchall()
    connection.close()
    return tracks

def uploadResults(data):
    connection = sqlite3.connect(db_path)
    cur = connection.cursor()
    query = """INSERT INTO results (
    driver_id,
    team_id,
    session_id,
    position,
    laps_completed,
    total_race_time,
    fastest_lap,
    fastest_lap_number,
    gap,
    interval,
    top_speed,
    points,
    endstatus
    ) VALUES"""
    try:
        for i in range(26):
            position = data[f"result[{i}][position]"]
            driver_number= data[f"result[{i}][driver_number]"]
            completed_laps = data[f"result[{i}][completed_laps]"]
            time = data[f"result[{i}][time]"]
            gap = data[f"result[{i}][gap]"]
            interval = data[f"result[{i}][interval]"]
            top_speed = data[f"result[{i}][top_speed]"]
            fl_time = data[f"result[{i}][fl_time]"]
            fl_number = data[f"result[{i}][fl_number]"]
            points = data[f"result[{i}][points]"]
            driver = data[f"result[{i}][driver]"].split(" ")
            status = "finished" if data[f"result[{i}][gap]"] != "DNF" else "dnf"
            event = data["event"]
            session = data["session"]
            result = cur.execute("SELECT id, team_id FROM drivers WHERE first_name = ? AND last_name = ? AND driver_number = ?",
                                    (driver[0].capitalize(), driver[1].capitalize(), driver_number)).fetchone()
            driver_id = result[0]
            team_id = result[1]
            session_id = data["session"]
            query += f"""{",\n" if i > 0 else ""} ({driver_id},{team_id},{session_id},'{position}','{completed_laps}','{time}','{fl_time}','{fl_number}','{gap}','{interval}','{top_speed}','{points}','{status}')"""

    except:
        pass
    cur.execute(query)
    connection.commit()
    connection.close()
    return data

def getSessions(event_id):
    connection = sqlite3.connect(db_path)
    cur = connection.cursor()
    try:
        sessions = cur.execute("""SELECT id, type FROM sessions WHERE event_id = ? AND id NOT IN (
                               SELECT session_id FROM results)""", [event_id]).fetchall()
    except:
        return None
    return sessions

def getDrivers():
    connection = sqlite3.connect(db_path)
    cur = connection.cursor()
    results = cur.execute("""SELECT * FROM drivers WHERE id IN (
                   SELECT driver_id FROM results WHERE session_id IN (
                   SELECT id FROM sessions WHERE event_id IN (
                   SELECT id FROM events WHERE year = 2024)))""").fetchall()
    return results

def getResult(driver_id):
    connection = sqlite3.connect(db_path)
    cur = connection.cursor()
    results = cur.execute("SELECT * FROM results WHERE driver_id = ?", [driver_id]).fetchall()
    # results = cur.execute("""SELECT * FROM results WHERE driver_id = ? AND IN (
    #            SELECT id FROM sessions WHERE event_id IN (
    #            SELECT id FROM events WHERE year = 2024))""", [driver_id]).fetchall()
    return results

def listSessions(event_id):
    connection = sqlite3.connect(db_path)
    cur = connection.cursor()
    result = cur.execute("SELECT * FROM sessions WHERE event_id = ?", [event_id]).fetchall()
    return [result]

def eventList(year):
    connection = sqlite3.connect(db_path)
    cur = connection.cursor()
    if year == "" or year == None:
        result = cur.execute("SELECT * FROM events").fetchall()
    else:
        result = cur.execute("SELECT * FROM events WHERE year = ?", [year]).fetchall()
    return [result]

def getSessionResults(session_id):
    connection = sqlite3.connect(db_path)
    cur = connection.cursor()
    results = cur.execute("SELECT * FROM results INNER JOIN drivers ON results.driver_id=drivers.id INNER JOIN teams ON teams.id = drivers.team_id WHERE results.session_id = ?", [session_id]).fetchall()
    return results
