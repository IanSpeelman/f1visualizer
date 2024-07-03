import pdfplumber
from random import random

def saveDocument(file):
    filename = f"files/{random()}.pdf"
    file.save(filename)
    return filename

def getResults(file):
    with pdfplumber.open(file) as pdf:
        page = pdf.pages[1];
        results = page.extract_tables(table_settings={"snap_x_tolerance": 1})
        return results
    
def getFastestLap(results):
    fastest_index = 0
    i = 0
    for result in results[0]:
        if result[11] < results[0][fastest_index][11]:
            fastest_index = i
        i += 1
    return fastest_index