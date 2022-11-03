import csv
import os
import shutil
import time
import traceback
from rdflib import Graph, BNode
from rdflib.namespace import Namespace
from SPARQLWrapper import SPARQLWrapper, JSON
import rdflib
import shutil
import traceback
from rdflib import Graph, URIRef, Literal, BNode, XSD
from rdflib.namespace import FOAF, NamespaceManager, Namespace, RDFS

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
                duplicatereader = csv.DictReader(inputfile, delimiter=',')
                uniquewrite = csv.DictWriter(outputfile, fieldnames=["uri", "type", "aat_label", "aat_uri"],
                                             delimiter=',')
                uniquewrite.writeheader()
                keysread = []
                for row in duplicatereader:
                    key = (row['aat_uri'])
                    if key not in keysread:
                        keysread.append(key)
                        uniquewrite.writerow(row)

def openArtFormWithOutDuplication(_path="./csvartform-final/"):
    try:
        _entities = []
        for fName in os.listdir(_path):
            if not fName.endswith('.csv'):
                continue
            _entities.append(fName.split(".")[0])
            processArtFormCsv(_entities, sparqlEndpoint)
    except Exception as e:
        print(str(e), traceback.format_exc())

def processArtFormCsv(_entities, sparqlEndpoint):
    try:


        for csvFile in _entities:
            choosen = []
            print(csvFile + "Parsed successfully")
            # make path result
            # resultFilePath = f'./csvartform-final/{csvFile}_result.csv'

            with open(f'./csvartform-final/{csvFile}.csv') as fileHanler:
                csvreader = csv.reader(fileHanler)
                for rowdata in csvreader:
                    if rowdata[3].startswith("http://vocab.getty.edu/aat"):
                        term = (rowdata[3])
                        aatUris = Literal(f'<{term}>', datatype=XSD.anyURI)
                        subFile = rowdata[0]
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
            choosen.append('http://vocab.getty.edu/aat/300033618')
            tempList = []
            for uri in choosen:
                with open(f'./type/{csvFile}.csv', 'r', newline='') as inputfile:
                    recordReader = csv.DictReader(inputfile, delimiter=',')
                    for row in recordReader:
                        key = row['aat_uri']
                        if key == uri:
                            tempList.append({'uri': row['uri'], 'item': key})
            finalList = []
            for d in tempList:
                if d not in finalList:
                    finalList.append(d)
                    resultFilePath = f'./csv-final/{csvFile}_result.csv'
                    shutil.rmtree(resultFilePath, ignore_errors=True)
                    os.makedirs(resultFilePath, exist_ok=True)
                    with open(resultFilePath, 'a', encoding='utf-8', newline='') as csvResultValue:
                        resultWriter = csv.writer(csvResultValue)
                        resultWriter.writerow([d['uri'], d['item']])

    except Exception as e:
        print("The error is :::", str(e))


startProcessing()
openArtFormWithOutDuplication()
