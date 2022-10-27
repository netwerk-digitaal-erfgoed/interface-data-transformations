import csv
import rdflib
import re
from rdflib import Graph, URIRef, Literal, BNode, XSD
from rdflib.namespace import FOAF, NamespaceManager, Namespace, RDFS
import os
import shutil
import traceback

result_enrichment = './enrichment-step-2/'

edm = Namespace("http://www.europeana.eu/schemas/edm/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
dcterms = Namespace("http://purl.org/dc/terms/")
aat = Namespace("http://vocab.getty.edu/aat/")
dc = Namespace("http://purl.org/dc/elements/1.1/")

def startProcessing(_path="./enrich-step1/"):
    try:
        _entities = []
        for fName in os.listdir(_path):
            if not fName.endswith('.ttl'):
                continue
            _entities.append(fName.split(".")[0])
        startEnrichment(_entities, result_enrichment,edm,rdf,dcterms,dc,aat)
    except Exception as e:
        print(str(e), traceback.format_exc())

def startEnrichment(_entities, _result_enrichment,_edm,_rdf,_dcterms,_dc,_aat):
    try:
        shutil.rmtree(result_enrichment, ignore_errors=True)
        os.makedirs(result_enrichment, exist_ok=True)
        for url in _entities:
            gPath = f'./enrich-step1/{url}.ttl'
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
                if (str(row.p) == 'http://www.europeana.eu/schemas/edm/type'):
                    g.add((row.s, _edm['image'], BNode(index)))
                    g.add((BNode(index), _rdf['type'], _edm['ImageObject']))
                if (str(row.p) == "http://purl.org/dc/terms/created"):
                    dateOfCreation = str(row.o)
                    match = re.search(r'\d{4}', dateOfCreation)
                    if match and match.group(0) is not None:
                        dateOfCreation_forComparison = int(match.group(0))
                        Date = str(match.group(0))
                    else:
                        continue
                    g.add((row.s, _dcterms.dateCreated, Literal(Date)))
                    g.add((row.s, _dcterms.temporal, Literal(dateOfCreation)))

                if (str(row.p) == "http://purl.org/dc/elements/1.1/date"):
                    dateOfCreation = str(row.o)
                    match = re.search(r'\d{4}', dateOfCreation)
                    if match and match.group(0) is not None:
                        dateOfCreation_forComparison = int(match.group(0))
                        Date = str(match.group(0))
                    else:
                        continue
                    g.add((row.s, _dcterms.dateCreated, Literal(Date)))
                    g.add((row.s, _dcterms.temporal, Literal(dateOfCreation)))

                #### it is for moderne-kunst-museum-deventer inwhich date is in the creator
                # if (str(row.p) == "http://purl.org/dc/elements/1.1/creator"):
                #     dateOfCreation = str(row.o)
                #     match = re.search(r'\d{4}', dateOfCreation)
                #     if match and match.group(0) is not None:
                #         dateOfCreation_forComparison = int(match.group(0))
                #         Date = str(match.group(0))
                #     else:
                #         continue
                #     g.add((row.s, dcterms.dateCreated, Literal(Date)))
                #     g.add((row.s, dcterms.temporal, Literal(dateOfCreation)))

                    if dateOfCreation_forComparison >= 1000 and dateOfCreation_forComparison < 1450:
                        g.add((row.s, _edm.temporalCoverage, _aat['300020756']))
                        g.add((_aat['300020756'], _dcterms.startDate, Literal("1000", datatype=XSD.string)))
                        g.add((_aat['300020756'], _dcterms.endDate, Literal("1450", datatype=XSD.string)))
                        g.add((_aat['300020756'], _dcterms.name, Literal("Medieval", datatype=XSD.string)))
                        continue
                    elif dateOfCreation_forComparison >= 1450 and dateOfCreation_forComparison < 1600:
                        g.add((row.s, _edm.temporalCoverage, _aat['300021140']))
                        g.add((_aat['300021140'], _dcterms.startDate, Literal("1450", datatype=XSD.string)))
                        g.add((_aat['300021140'], _dcterms.endDate, Literal("1600", datatype=XSD.string)))
                        g.add((_aat['300021140'], _dcterms.name, Literal("Renaissance", datatype=XSD.string)))
                        continue
                    elif dateOfCreation_forComparison >= 1600 and dateOfCreation_forComparison < 1750:
                        g.add((row.s, _edm.temporalCoverage,  _aat['300021147']))
                        g.add((_aat['300021147'], _dcterms.startDate, Literal("1600", datatype=XSD.string)))
                        g.add((_aat['300021147'], _dcterms.endDate, Literal("1750", datatype=XSD.string)))
                        g.add((_aat['300021147'], _dcterms.name, Literal("Baroque", datatype=XSD.string)))
                        continue
                    elif dateOfCreation_forComparison >= 1750 and dateOfCreation_forComparison < 1850:
                        g.add((row.s, _edm.temporalCoverage, _aat['300172863000']))
                        g.add((_aat['300172863000'], _dcterms.startDate, Literal("1750", datatype=XSD.string)))
                        g.add((_aat['300172863000'], _dcterms.endDate, Literal("1850", datatype=XSD.string)))
                        g.add((_aat['300172863000'], _dcterms.name, Literal("Classicism ", datatype=XSD.string)))
                        continue
                    elif dateOfCreation_forComparison >= 1830 and dateOfCreation_forComparison < 1870:
                        g.add((row.s, _edm.temporalCoverage, _aat['300172861']))
                        g.add((_aat['300172861'], _dcterms.startDate, Literal("1830", datatype=XSD.string)))
                        g.add((_aat['300172861'], _dcterms.endDate, Literal("1870", datatype=XSD.string)))
                        g.add((_aat['300172861'], _dcterms.name, Literal("Realist", datatype=XSD.string)))
                        continue
                    elif dateOfCreation_forComparison >= 1860 and dateOfCreation_forComparison < 1890:
                        g.add((row.s, _edm.temporalCoverage, _aat['300021503']))
                        g.add((_aat['300021503'], _dcterms.startDate, Literal("1860", datatype=XSD.string)))
                        g.add((_aat['300021503'], _dcterms.endDate, Literal("1890", datatype=XSD.string)))
                        g.add((_aat['300021503'], _dcterms.name, Literal("Impressionist", datatype=XSD.string)))
                        continue
                    elif dateOfCreation_forComparison >= 1890 and dateOfCreation_forComparison < 1970:
                        g.add((row.s, _edm.temporalCoverage, _aat['300021474']))
                        g.add((_aat['300021474'], _dcterms.startDate, Literal("1890", datatype=XSD.string)))
                        g.add((_aat['300021474'], _dcterms.endDate, Literal("1970", datatype=XSD.string)))
                        g.add((_aat['300021474'], _dcterms.name, Literal("Modernist", datatype=XSD.string)))
                        continue
                    elif dateOfCreation_forComparison >= 1970:
                        g.add((row.s, _edm.temporalCoverage, _aat['300022208']))
                        g.add((_aat['300022208'], _dcterms.startDate, Literal("1970", datatype=XSD.string)))
                        g.add((_aat['300022208'], _dcterms.endDate, Literal("Now", datatype=XSD.string)))
                        g.add((_aat['300022208'], _dcterms.name, Literal("Postmodern", datatype=XSD.string)))
                        continue
            g.serialize(destination=f'{result_enrichment}{url}.ttl', format='turtle', encoding='utf-8')
            print(" Done! successfully")
    except Exception as e:
      print(str(e), traceback.format_exc())

###### This is for creators
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

def openCsvToTriple(_path="./creators/"):
    try:
        entities = discoverSources(_path)
        csvToTripleProcess(_path, entities)
    except Exception as e:
        print(str(e), traceback.format_exc())


def csvToTripleProcess(_path, _entities, finalPath='./final-creator-triples/', enrichfile='./enrich-data-for-datamodel/'):
    shutil.rmtree(finalPath, ignore_errors=True)
    os.makedirs(finalPath, exist_ok=True)
    shutil.rmtree(enrichfile, ignore_errors=True)
    os.makedirs(enrichfile, exist_ok=True)

    try:
        g = Graph()
        for csvFile in _entities:
            entity = csvFile.split("_")[0]
            with open(f'{_path}{csvFile}.csv') as fileHanler:
                csvreader = csv.reader(fileHanler)
                next(csvreader, None)
                for row in csvreader:
                    if (len(row[3])) > 25 :
                        g.add((URIRef(row[0]), dcterms.creators, URIRef(row[3])))

            g.serialize(destination=f'{finalPath}{csvFile}.n3', format='ntriples', encoding='utf-8')
            g2 = Graph()
            g2.parse(f'{finalPath}{csvFile}.n3', format='ntriples')
            g2.namespace_manager.bind('dcterms', URIRef('http://purl.org/dc/terms/'), replace=True)
            g2.namespace_manager.bind('aat', URIRef('http://vocab.getty.edu/aat/'), replace=True)
            g2.serialize(destination=f'{finalPath}{csvFile}.ttl', format='turtle', encoding='utf-8')

            gcreators = Graph()
            gcreators.parse(f'{finalPath}{csvFile}.ttl', format='turtle')
            gOrginFile = Graph()
            gOrginFile.parse(f"./enrichment-step-2/{entity}.ttl", format='turtle')
            integrateFile = gcreators + gOrginFile
            integrateFile.serialize(destination=f'{enrichfile}{entity}.ttl', format='turtle', encoding='utf-8')
            integrateFile.serialize(destination=f'{enrichfile}{entity}.ttl', format='turtle', encoding='utf-8')

    except Exception as e:
        print(str(e), traceback.format_exc())




startProcessing()
openCsvToTriple()