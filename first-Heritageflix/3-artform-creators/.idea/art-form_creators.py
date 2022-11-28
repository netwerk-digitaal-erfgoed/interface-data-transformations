import shutil
import traceback
import csv
from rdflib import Graph, URIRef, Literal, BNode, XSD
from rdflib.namespace import FOAF, NamespaceManager, Namespace, RDFS
import os

edm = Namespace("http://www.europeana.eu/schemas/edm/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
dcterms = Namespace("http://purl.org/dc/terms/")
aat = Namespace("http://vocab.getty.edu/aat/")
dc = Namespace("http://purl.org/dc/elements/1.1/")

def openCsvToTriple(_path="./testfile/"):
    try:
        _entities = []
        for fName in os.listdir(_path):
            if not fName.endswith('.csv'):
                continue
            _entities.append(fName.split(".")[0])
        csvToTripleProcess(_path, _entities)
    except Exception as e:
        print(str(e), traceback.format_exc())

def csvToTripleProcess(_path, _entities, artformPath = './artformtriple/'):
    shutil.rmtree(artformPath, ignore_errors=True)
    os.makedirs(artformPath, exist_ok=True)
    try:
        g = Graph()
        for csvFile in _entities:
            print(csvFile)
            with open (f'{_path}{csvFile}.csv') as fileHanler:
                csvreader = csv.reader(fileHanler)
                for row in csvreader:
                    g.add((URIRef(row[0]), dcterms.artform, URIRef(row[1])))

            g.serialize(destination=f'{artformPath}artforms_test.n3', format='ntriples', encoding='utf-8')
            g2 = Graph()
            g2.parse(f'{artformPath}artforms_test.n3', format='ntriples')
            g2.namespace_manager.bind('dcterms', URIRef('http://purl.org/dc/terms/'), replace=True)
            g2.namespace_manager.bind('aat', URIRef('http://vocab.getty.edu/aat/'), replace=True)
            g2.serialize(destination=f'{artformPath}artforms_test_final.ttl', format='turtle', encoding='utf-8')

    except Exception as e:
       print(str(e), traceback.format_exc())



def enrichWithArtForm( enrichfile = './enrich-step1/', artformPath = './artformtriple/artforms_test_final.ttl', pathorginalfile="./converted/mauritshuis.ttl"):
    shutil.rmtree(enrichfile, ignore_errors=True)
    os.makedirs(enrichfile, exist_ok=True)
    gArtFrom = Graph()
    gArtFrom.parse(f'{artformPath}', format='turtle')
    gOrginFile = Graph()
    gOrginFile.parse(f'{pathorginalfile}', format='turtle')
    integrateFile = gArtFrom + gOrginFile
    integrateFile.serialize(destination=f'{enrichfile}mauritshuis_Graph.ttl', format='turtle', encoding='utf-8')

def extract_csv_creators(enrichfile='./enrich-step1/', _resultCreatorsCsv='./creators/'):
    shutil.rmtree(_resultCreatorsCsv, ignore_errors=True)
    os.makedirs(_resultCreatorsCsv, exist_ok=True)
    # for entityName in _entities:
    gPath = f'{enrichfile}mauritshuis_Graph.ttl'
    g = Graph()
    g.parse(gPath, format("ttl"))
    print( " file Parsed successfully")

    getByIdentifiers = """
    SELECT DISTINCT ?a ?b 
    WHERE {
        ?a <http://purl.org/dc/elements/1.1/creator> ?b .
        ?a <http://purl.org/dc/terms/artform> ?c.    
    }"""

    qres = g.query(getByIdentifiers)
    with open(_resultCreatorsCsv+ f'creators.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL, delimiter=',', quotechar='"')  # quotechar='',
        f.write(",".join(["uri", "creators"]))
        f.write("\n")
        for row in qres:
            sub = row.a.split("/n")[0]
            obj = row.b.split("/n")[0]
            writer.writerow([sub, obj])


openCsvToTriple()
enrichWithArtForm()
extract_csv_creators()