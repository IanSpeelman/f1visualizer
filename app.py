from flask import Flask, request, render_template, redirect
from random import random
from pypdf import PdfReader

app = Flask(__name__)

@app.route("/")
def index():
    reader = PdfReader("files/0.6736087870438566.pdf")
    page = reader.pages[1]
    data = page.extract_text()
    words = []
    # print(len(data))
    # page = reader.pages[1]
    # data = page.extract_text()
    # print(len(data))

    for letter in data:
        if letter == "\n":
            print("  <-nl->  ")
        else:
            print(letter, end = "")
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    file.save(f"files/{random()}.pdf")
    return redirect("/")