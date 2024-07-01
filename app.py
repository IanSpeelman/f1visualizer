from flask import Flask, request, render_template, redirect
from random import random
from pypdf import PdfReader
import pdfplumber


app = Flask(__name__)

@app.route("/")
def index():
    with pdfplumber.open("files/result3.pdf") as pdf:
        page = pdf.pages[1];
        data = page.extract_tables(table_settings={})
    
    return render_template("index.html")



@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    file.save(f"files/{random()}.pdf")
    return redirect("/")