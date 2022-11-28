import csv
import os
import shutil
import traceback
from rdflib import Graph
import os.path

result_enrichment = './report-final/'

shutil.rmtree(result_enrichment, ignore_errors=True)
os.makedirs(result_enrichment, exist_ok=True)


def startProcessing(_path="."):
    try:

        for dirPath, dirNames, files in os.walk("."):
            _entities = []
            hasFile = False
            for fileName in [f for f in files if f.endswith(".ttl")]:
                hasFile = True
                _entities.append(fileName.split(".")[0])
            if hasFile:
                startEnrichment(_entities, dirPath, result_enrichment)

    except Exception as e:
        print(str(e), traceback.format_exc())


def startEnrichment(_entities, _dirName, _result_enrichment):
    try:
        gPathName = _dirName.replace(".\\","").replace("\\","//")
        dirName = gPathName.replace("//","-")

        resultFilePath = f'{_result_enrichment}/{dirName}-report.csv'
        with open(resultFilePath, 'a', encoding='utf-8', newline='') as csvResultValue:
            resultWriter = csv.writer(csvResultValue)
            resultWriter.writerow(["entity", "count"])

        for url in _entities:
            gPath = f'./{gPathName}/{url}.ttl'
            g = Graph()
            g.parse(gPath, format("ttl"))
            print(url + " Parsed successfully")
            getByIdentifiers = """  
            SELECT distinct  (count( DISTINCT  ?s) as ?scount)
            WHERE {
                ?s ?p ?o .
                FILTER (!isBlank(?s))

            }"""

            qres = g.query(getByIdentifiers)
            for index, row in enumerate(qres):
                print(row.scount)

            with open(resultFilePath, 'a', encoding='utf-8', newline='') as csvResultValue:
                resultWriter = csv.writer(csvResultValue)
                resultWriter.writerow([f'{url}-records', row.scount])

    except Exception as e:
        print(str(e), traceback.format_exc())


startProcessing()