import csv
from rdflib import Graph, URIRef, Literal, BNode, XSD
from rdflib.namespace import Namespace
import os
import shutil
import traceback

def main ():
    startProcessing()
    strartProcessCorrectedPrefixes()


edm = Namespace("http://www.europeana.eu/schemas/edm/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
dcterms = Namespace("http://purl.org/dc/terms/")
aat = Namespace("http://vocab.getty.edu/aat/")
dc = Namespace("http://purl.org/dc/elements/1.1/")

def startProcessing(_path="./reconciled/"):
    try:
        _entities = []
        for fName in os.listdir(_path):
            if not fName.endswith('.csv'):
                continue
            _entities.append(fName.split(".")[0])
        csvToTripleProcess(_path, _entities)
    except Exception as e:
        print(str(e), traceback.format_exc())

def csvToTripleProcess(_path, _entities, finalPath='./final-triples/', enrichfile='./integrationstep1/'):
    shutil.rmtree(finalPath, ignore_errors=True)
    os.makedirs(finalPath, exist_ok=True)

    shutil.rmtree(enrichfile, ignore_errors=True)
    os.makedirs(enrichfile, exist_ok=True)
    try:
        g = Graph()
        for index, csvFile in enumerate(_entities):
        # for index, csvFile in _entities:
            entity = csvFile.split("-")[0]
            print(entity)
            with open(f'{_path}{csvFile}.csv') as fileHanler:
                csvreader = csv.reader(fileHanler) 
                next(csvreader, None)
                for row in csvreader:
                    if (len(row[3])) > 25 and entity == "kerk":
                        removesigns = row[1].replace('<', "").replace('>', "")
                        g.add((URIRef(removesigns), dc.subjectURL, URIRef(row[3])))
                    elif (len(row[3])) > 25 and entity == "spatial":
                        removesigns = row[1].replace('<', "").replace('>', "")
                        g.add((URIRef(removesigns), dc.spatialURI, URIRef(row[3])))


            g.serialize(destination=f'{finalPath}{entity}{index}.n3', format='ntriples', encoding='utf-8')
            g2 = Graph()
            g2.parse(f'{finalPath}{entity}{index}.n3', format='ntriples')
            g2.namespace_manager.bind('dc', URIRef('http://purl.org/dc/elements/1.1/'), replace=True)
            g2.serialize(destination=f'{finalPath}{entity}{index}.ttl', format='turtle', encoding='utf-8')
        integration(finalPath, enrichfile)

    except Exception as e:
        print(str(e), traceback.format_exc())

def integration(finalPath, enrichfile):
    gkerk= Graph()
    gkerk.parse(f'{finalPath}kerk0.ttl', format='turtle')
    path = f"./enrichment-step-2/kerkenEnSpatial.ttl"
    print(path)
    gspatial = Graph()
    gspatial.parse(f'{finalPath}spatial1.ttl', format='turtle')
    integrateFile = gkerk + gspatial
    integrateFile.serialize(destination=f'{enrichfile}kerkenspatial.ttl', format='turtle', encoding='utf-8')
    print(f' final enrichment has been done! your final datasets are in {enrichfile} folder')



def strartProcessCorrectedPrefixes(_path="./corrected-prefixes/"):
    try:
        _entities = []
        for fName in os.listdir(_path):
            if not fName.endswith('.ttl'):
                continue
            _entities.append(fName.split(".")[0])
        ProcessCorrectedPrefixes(_path, _entities)
    except Exception as e:
        print(str(e), traceback.format_exc())


def ProcessCorrectedPrefixes(_path, _entities,finalPath='./mergeForenrichtment/'):
    shutil.rmtree(finalPath, ignore_errors=True)
    os.makedirs(finalPath, exist_ok=True)

    try:

        gcsv = Graph()
        enrichfile = './integrationstep1/kerkenspatial.ttl'
        gcsv.parse(enrichfile, format='ttl')
        g = Graph()
        for ttlFile in _entities:

            path = f'{_path}{ttlFile}.ttl'
            print(path)
            g.parse(path, format='ttl')

            integrationGraph = g + gcsv

            integrationGraph.serialize(destination=f'{finalPath}{ttlFile}.ttl')

            print(f' final enrichment has been done! your final datasets are in {finalPath} path')


    except Exception as e:
        print(str(e), traceback.format_exc())

main()
