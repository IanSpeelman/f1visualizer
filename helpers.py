import pdfplumber
from random import random
import camelot
import json

def saveDocument(file):
    filename = f"files/{random()}.pdf"
    file.save(filename)
    return filename

def getData(file):
    filename = saveDocument(file)
    results = camelot.read_pdf(filename, flavor='stream', pages='2')
    results = results[0].df.to_json()
    results = json.loads(results)
    fixed_results = []
    for i in range(len(results["0"])):
        tmp = []
        for j in range(len(results)):
            tmp.append(results[str(j)][str(i)])
        fixed_results.append(tmp)
    return fixed_results
    
# def getFastestLap(results):
#     fastest_index = 0
#     i = 0
#     for result in results[0]:
#         if result[11] < results[0][fastest_index][11]:
#             fastest_index = i
#         i += 1
#     return fastest_index

# def getDriverInfo(file):
#     filename = saveDocument(file)
#     results = camelot.read_pdf(filename, flavor='stream', pages='2')
#     json = results[0].df.to_json()
#     return json