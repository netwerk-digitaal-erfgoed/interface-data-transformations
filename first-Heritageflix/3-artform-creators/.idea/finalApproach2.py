import csv
import os
import shutil
import traceback
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Literal, XSD

sparqlEndpoint = 'http://vocab.getty.edu/sparql'


def startProcessing(_path="./type/"):
    try:
        _entities = []
        for fName in os.listdir(_path):
            if not fName.endswith('.csv'):
                continue
            _entities.append(fName.split(".")[0])
        RemoveCSVDuplications(_path, _entities)
    except Exception as e:
        print(str(e), traceback.format_exc())


def RemoveCSVDuplications(_path, _entities):
    for entityName in _entities:
        shutil.rmtree("./csvartform-final/", ignore_errors=True)
        os.makedirs("./csvartform-final/", exist_ok=True)
        with open(f'{_path}{entityName}.csv', 'r', newline='') as inputfile:
            with open("./csvartform-final/" + f'{entityName}.csv', 'w', newline='') as outputfile:
                duplicateReader = csv.DictReader(inputfile, delimiter=',')
                uniqueWrite = csv.DictWriter(outputfile, fieldnames=["uri", "type", "aat_label", "aat_uri"],
                                             delimiter=',')
                uniqueWrite.writeheader()
                keysRead = []
                for row in duplicateReader:
                    key = (row['aat_uri'])
                    if key not in keysRead:
                        keysRead.append(key)
                        uniqueWrite.writerow(row)


def openArtFormWithOutDuplication(_path="./csvartform-final/"):
    try:
        _entities = []
        for fName in os.listdir(_path):
            if not fName.endswith('.csv'):
                continue
            _entities.append(fName.split(".")[0])
            processArtFormCsv(_entities)
    except Exception as e:
        print(str(e), traceback.format_exc())


def processArtFormCsv(_entities):
    try:
        for csvFile in _entities:
            choosen = []
            print(csvFile + "Parsed successfully")
            with open(f'./csvartform-final/{csvFile}.csv') as fileHanler:
                csvreader = csv.reader(fileHanler)
                for rowData in csvreader:
                    if rowData[3].startswith("http://vocab.getty.edu/aat"):
                        term = (rowData[3])
                        aatUris = Literal(f'<{term}>', datatype=XSD.anyURI)
                        subFile = rowData[0]
                        query = ("""SELECT  ?term ?o
                        WHERE {
                          BIND((""" + aatUris + """)AS ?term)
                          ?term <http://www.w3.org/2004/02/skos/core#broaderTransitive> ?o
                          filter(?o = <http://vocab.getty.edu/aat/300033618>)
                        }""")
                        sparql = SPARQLWrapper(sparqlEndpoint)
                        sparql.setQuery(query)
                        # time.sleep(1)  # imported from time
                        sparql.setReturnFormat(JSON)
                        results = sparql.query().convert()
                        for result in results["results"]["bindings"]:
                            obj = result['o']
                            artClass = obj['value']
                            term = result['term']
                            subClassPainting = term['value']
                            if artClass == 'http://vocab.getty.edu/aat/300033618':
                                choosen.append(subClassPainting)
                                # print(choosen)

            choosen.append('http://vocab.getty.edu/aat/300033618')
            # print(choosen)
            tempList = []
            for uri in choosen:
                with open(f'./type/{csvFile}.csv', 'r', newline='') as inputfile:
                    recordReader = csv.DictReader(inputfile, delimiter=',')
                    for row in recordReader:
                        key = row['aat_uri']
                        if key == uri:
                            tempList.append({'uri': row['uri'], 'item': key})##here is list of sparql output


            resultFilePath = "./csv-final/"
            shutil.rmtree(resultFilePath, ignore_errors=True)
            os.makedirs(resultFilePath, exist_ok=True)
            resultFilePath += f'{csvFile}_result.csv'
            finalList = []
            for d in tempList: ## here compare orginal file with sparql output
                if d not in finalList:
                    finalList.append(d)

                    with open(resultFilePath, 'a', encoding='utf-8', newline='') as csvResultValue:
                        resultWriter = csv.writer(csvResultValue)
                        resultWriter.writerow([d['uri'], d['item']])

    except Exception as e:
        print("The error is :::", str(e))


startProcessing()
openArtFormWithOutDuplication()
