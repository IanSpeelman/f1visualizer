from flask import Flask, request, render_template, redirect
from random import random
import pdfplumber


app = Flask(__name__)

@app.route("/")
def index():
    with pdfplumber.open("files/result9.pdf") as pdf:
        page = pdf.pages[1];
        data = page.extract_tables(table_settings={"snap_x_tolerance": 1})
    results = []
    for driver in data[0]:
        results.append(driver)
    return results
    return render_template("index.html")



@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    file.save(f"files/{random()}.pdf")
    return redirect("/")