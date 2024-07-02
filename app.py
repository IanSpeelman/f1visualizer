from flask import Flask, request, render_template, redirect
from random import random
import pdfplumber


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")



@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    filename = f"files/{random()}.pdf"
    file.save(filename)

    with pdfplumber.open(filename) as pdf:
        page = pdf.pages[1];
        results = page.extract_tables(table_settings={"snap_x_tolerance": 1})
    fastest_index = 0
    i = 0
    for result in results[0]:
        if result[11] < results[0][fastest_index][11]:
            fastest_index = i
        i += 1
    
    # return results
    fastest_lap = results[0][fastest_index]
    return render_template("table.html", results=results, fastest_lap=fastest_lap)