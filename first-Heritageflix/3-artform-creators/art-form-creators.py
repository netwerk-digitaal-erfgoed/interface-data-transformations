import csv
import os
import shutil
import traceback
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, URIRef
from rdflib.namespace import Namespace
from rdflib import Literal, XSD

edm = Namespace("http://www.europeana.eu/schemas/edm/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
dcterms = Namespace("http://purl.org/dc/terms/")
aat = Namespace("http://vocab.getty.edu/aat/")
dc = Namespace("http://purl.org/dc/elements/1.1/")

sparqlEndpoint = 'http://vocab.getty.edu/sparql'

def discoverSources(_path, postfix='csv'):
    try:
        _entities = []
        for fName in os.listdir(_path):
            if not fName.endswith(postfix):
                continue
            _entities.append(fName.split(".")[0])
        return _entities
    except Exception as e:
        print(str(e), traceback.format_exc())


def startProcessing(_path="./type/"):
    try:
        entities = discoverSources(_path)
        RemoveCSVDuplications(_path, entities)
    except Exception as e:
        print(str(e), traceback.format_exc())

def RemoveCSVDuplications(_path, _entities):
    try:
        csvArtFormPath = "./csvartform/"
        shutil.rmtree(csvArtFormPath, ignore_errors=True)
        os.makedirs(csvArtFormPath, exist_ok=True)
        for entityName in _entities:

            with open(f'{_path}{entityName}.csv', 'r', newline='') as inputfile:
                with open(csvArtFormPath + f'{entityName}.csv', 'w', newline='') as outputfile:
                    duplicateReader = csv.DictReader(inputfile, delimiter=',')
                    uniqueWrite = csv.DictWriter(outputfile, fieldnames=["uri", "type", "aat_label", "aat_uri"], delimiter=',')
                    uniqueWrite.writeheader()
                    keysRead = []
                    for row in duplicateReader:
                        key = (row['aat_uri'])
                        if key not in keysRead:
                            keysRead.append(key)
                            uniqueWrite.writerow(row)
        entities = discoverSources(csvArtFormPath)
        processArtFormCsv(entities)
    except Exception as e:
        print(str(e), traceback.format_exc())

def processArtFormCsv(_entities):
    try:
        resultFilePath = "./csv-final/"
        shutil.rmtree(resultFilePath, ignore_errors=True)
        os.makedirs(resultFilePath, exist_ok=True)
        for csvFile in _entities:
            choosen = []
            print(csvFile + "Parsed successfully")
            with open(f'./csvartform/{csvFile}.csv') as fileHanler:
                csvreader = csv.reader(fileHanler)
                for rowData in csvreader:
                    if rowData[3].startswith("http://vocab.getty.edu/aat"):
                        term = (rowData[3])
                        aatUris = Literal(f'<{term}>', datatype=XSD.anyURI)
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


            finalPath = resultFilePath + f'{csvFile}_result.csv'
            finalList = []
            for d in tempList:
                if d not in finalList:
                    finalList.append(d)
                    with open(finalPath, 'a', encoding='utf-8', newline='') as csvResultValue:
                        resultWriter = csv.writer(csvResultValue)
                        resultWriter.writerow([d['uri'], d['item']])

    except Exception as e:
        print("The error is :::", str(e))

def openCsvToTriple(_path="./csv-final/"):
    try:
        entities = discoverSources(_path)
        csvToTripleProcess(_path, entities)
    except Exception as e:
        print(str(e), traceback.format_exc())

def csvToTripleProcess(_path, _entities, artformPath='./artformtriple/', enrichfile='./enrich-step1/'):
    shutil.rmtree(artformPath, ignore_errors=True)
    os.makedirs(artformPath, exist_ok=True)

    shutil.rmtree(enrichfile, ignore_errors=True)
    os.makedirs(enrichfile, exist_ok=True)

    try:
        g = Graph()
        for csvFile in _entities:
            entity = csvFile.split("_")[0]
            with open(f'{_path}{csvFile}.csv') as fileHanler:
                csvreader = csv.reader(fileHanler)
                for row in csvreader:
                    if (len(row[1])) > 25 :
                     g.add((URIRef(row[0]), dcterms.artform, URIRef(row[1])))
            g.serialize(destination=f'{artformPath}{csvFile}.n3', format='ntriples', encoding='utf-8')
            g2 = Graph()
            g2.parse(f'{artformPath}{csvFile}.n3', format='ntriples')
            g2.namespace_manager.bind('dcterms', URIRef('http://purl.org/dc/terms/'), replace=True)
            g2.namespace_manager.bind('aat', URIRef('http://vocab.getty.edu/aat/'), replace=True)
            g2.serialize(destination=f'{artformPath}{csvFile}.ttl', format='turtle', encoding='utf-8')
            gArtFrom = Graph()
            gArtFrom.parse(f'{artformPath}{csvFile}.ttl', format='turtle')
            gOrginFile = Graph()
            gOrginFile.parse(f"./converted/{entity}.ttl", format='turtle')
            try:
                if entity == csvFile:
                    integrateFile = gArtFrom + gOrginFile
                    integrateFile.serialize(destination=f'{enrichfile}{entity}.ttl', format='turtle', encoding='utf-8')
                    print('final enrichment step 1 has been done! your final datasets are in "enrich-step1 and creators" folders for the next step')
            except Exception as e:
                print("integration Error: ", str(e), traceback.format_exc())
    except Exception as e:
        print(str(e), traceback.format_exc())


def extract_csv_creators(enrichfile='./enrich-step1/', _resultCreatorsCsv='./creators/'):
    try:
        shutil.rmtree(_resultCreatorsCsv, ignore_errors=True)
        os.makedirs(_resultCreatorsCsv, exist_ok=True)

        entities = discoverSources(enrichfile, 'ttl')
        for entityName in entities:
            gPath = f'{enrichfile}{entityName}.ttl'
            g = Graph()
            g.parse(gPath, format("ttl"))
            print(f'{entityName} parsed successfully')

            getByIdentifiers = """
            SELECT DISTINCT ?a ?b 
            WHERE {
                ?a <http://purl.org/dc/elements/1.1/creator> ?b .
                ?a <http://purl.org/dc/terms/artform> ?c.    
            }"""

            qres = g.query(getByIdentifiers)
            with open(_resultCreatorsCsv + f'{entityName}.csv', 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, quoting=csv.QUOTE_ALL, delimiter=',', quotechar='"')  # quotechar='',
                f.write(",".join(["uri", "creators"]))
                f.write("\n")
                for row in qres:
                    sub = row.a.split("/n")[0]
                    obj = row.b.split("/n")[0]
                    writer.writerow([sub, obj])
        print("Creators file created successfully")
    except Exception as e:
        print(str(e), traceback.format_exc())

startProcessing()
openCsvToTriple()
extract_csv_creators()
