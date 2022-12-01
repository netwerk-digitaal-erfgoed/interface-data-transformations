import csv
import re
from rdflib import Graph, URIRef, Literal, BNode, XSD
from rdflib.namespace import Namespace
import os
import shutil
import traceback



edm = Namespace("http://www.europeana.eu/schemas/edm/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
dcterms = Namespace("http://purl.org/dc/terms/")
aat = Namespace("http://vocab.getty.edu/aat/")
dc = Namespace("http://purl.org/dc/elements/1.1/")

def startProcessing(_path="./enrichment-step-1/"):
    try:
        _entities = []
        for fName in os.listdir(_path):
            if not fName.endswith('.ttl'):
                continue
            _entities.append(fName.split(".")[0])
        startEnrichment(_entities,edm,rdf,dcterms,dc,aat)
    except Exception as e:
        print(str(e), traceback.format_exc())

def startEnrichment(_entities,_edm,_rdf,_dcterms,_dc,_aat, result_enrichment = './enrich-data-for-datamodel/'):
    try:
        shutil.rmtree(result_enrichment, ignore_errors=True)
        os.makedirs(result_enrichment, exist_ok=True)
        for url in _entities:
            gPath = f'./enrichment-step-1/{url}.ttl'
            g = Graph()
            g.parse(gPath, format("ttl"))
            print(url + " Parsed successfully")
            getByIdentifiers = """  
            SELECT DISTINCT ?s ?p ?o 
            WHERE {
                ?s ?p ?o .
            }"""
            qres = g.query(getByIdentifiers)
            for index, row in enumerate(qres):
                if (str(row.p) == 'http://purl.org/dc/elements/1.1/date'):
                    g.add((row.s, _edm['image'], BNode(index)))
                    g.add((BNode(index), _rdf['type'], _edm['ImageObject']))
                if (str(row.p) == 'http://purl.org/dc/elements/1.1/creator'):
                    g.add((row.s, _edm['creator'], BNode(index)))
                    g.add((BNode(index), _rdf['type'], _edm['Person']))

                if (str(row.p) == 'http://www.europeana.eu/schemas/edm/isShownBy'):
                    formatIMG = str(row.o).split(".")[-1]
                    if formatIMG == "JPG" or formatIMG == "jpg" :
                        formatIMG = f'image/{formatIMG}'
                        g.add((row.s, _dcterms['format'], Literal(formatIMG, datatype=XSD.string)))
                if (str(row.p) == "http://purl.org/dc/terms/created") or (str(row.p) == "http://purl.org/dc/terms/dateCreated")  :  ###or (str(row.p) == "http://purl.org/dc/elements/1.1/date")
                    dateOfCreation = str(row.o)

                    match = re.search(r'\d{4}', dateOfCreation)
                    if match and match.group(0) is not None:
                        dateOfCreation_forComparison = int(match.group(0))
                        # print("isiiiiiiii: ",dateOfCreation_forComparison)
                        Date = str(match.group(0))
                    else:
                        continue
                    g.add((row.s, _dcterms.dateCreated, Literal(Date, datatype=XSD.gYear)))
                    g.add((row.s, _dcterms.temporal, Literal(dateOfCreation, lang="nl")))
            g.serialize(destination=f'{result_enrichment}{url}.ttl', format='turtle', encoding='utf-8')
            print(f" Done! successfully, check {result_enrichment}{url}.ttl, the next step is datamodel change- step 5- showby is imgae not object")
    except Exception as e:
      print(str(e), traceback.format_exc())

startProcessing()
# openCsvToTriple()