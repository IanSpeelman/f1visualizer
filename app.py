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
        # return results
    return render_template("table.html", results=results)