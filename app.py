from flask import Flask, request, render_template, redirect
from helpers import getResults, saveDocument, getFastestLap


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")



@app.route("/upload", methods=["POST"])
def upload():
    document = saveDocument(request.files["file"])
    results = getResults(document)
    fastest_lap = getFastestLap(results)
    
    return render_template("table.html", results=results, fastest_lap=results[0][fastest_lap])