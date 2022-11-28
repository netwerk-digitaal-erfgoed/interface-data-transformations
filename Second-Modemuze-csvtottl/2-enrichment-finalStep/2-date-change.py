import os
import shutil
from timeit import default_timer as timer
from datetime import timedelta
import traceback
from rdflib import Graph, URIRef, Literal, BNode, XSD
from rdflib.namespace import FOAF, NamespaceManager, Namespace

start = timer()
print(start)

edm = Namespace("http://www.europeana.eu/schemas/edm/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
dcterms = Namespace("http://purl.org/dc/terms/")
aat = Namespace("http://vocab.getty.edu/aat/")
dc = Namespace("http://purl.org/dc/elements/1.1/")

def startProcessingDate(_path="./enrich-step1/"):
    try:
        _entities = []
        for fName in os.listdir(_path):
            if not fName.endswith('.ttl'):
                continue
            _entities.append(fName.split(".")[0])
        startEnrichment(_entities)

    except Exception as e:
        print(str(e), traceback.format_exc())

def startEnrichment(_entities, _pathdate="./date-change-enrichment/", _finalPath='./enrichstep-1Date/' ):
    try:
        shutil.rmtree(_finalPath, ignore_errors=True)
        os.makedirs(_finalPath, exist_ok=True)

        for filename in _entities:
            result = f'./date-change-enrichment/'
            shutil.rmtree(result, ignore_errors=True)
            os.makedirs(result, exist_ok=True)
            path = f'./enrich-step1/{filename}.ttl'
            ####### artworks Graph
            g_data = Graph().parse(path)

            with open('dateSparql.rq') as file:
                query_txt = file.read()
                res = g_data.query(query_txt)

            res.serialize(f'{result}/{filename}.n3', format='ntriples')
            g = Graph()
            g.parse(f'{result}/{filename}.n3', format='ntriples')
            g.namespace_manager.bind('dcterms', URIRef('http://purl.org/dc/terms/'), replace=True)
            g.serialize(destination=f'{result}/{filename}.ttl', format='turtle', encoding='utf-8')
            print(f'{filename} for Artwork graph has been serialized, successfully! check {result}')
            print("date integration start")

            gdate = Graph().parse(f'{_pathdate}/{filename}.ttl', format='turtle')
            gOrginalFile = Graph().parse(f'{path}', format='turtle')
            integrateFile = gdate + gOrginalFile
            integrateFile.serialize(destination=f'{_finalPath}{filename}.ttl', format='turtle', encoding='utf-8')
            print(f'final dataset: {_finalPath}{filename}.ttl, pase the file enrich-step 1 and run 3-enrich-step2')

    except Exception as e:
      print(str(e), traceback.format_exc())

startProcessingDate()

end = timer()
print(timedelta(seconds=end-start))