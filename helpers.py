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
    else:
        print("do nothing for now")
    connection.commit()
    connection.close()
    print(team_id, driver_id, result[4], result[5])
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
        print("create event", error)
        return
    for key in form:
        try:
            if form[key].split("T")[1] != None:
                createSession(key, form[key], id)
        except Exception as error:
            print("create session",error)
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