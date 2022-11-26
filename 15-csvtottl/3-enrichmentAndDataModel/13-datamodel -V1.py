from rdflib import Graph, URIRef
import os
import shutil
from timeit import default_timer as timer
from datetime import timedelta
import traceback

start = timer()
print(start)

def startProcessing(_path="./enrich-data-for-datamodel/"):
    try:
        _entities = []
        for fName in os.listdir(_path):
            if not fName.endswith('.ttl'):
                continue
            _entities.append(fName.split(".")[0])
        startEnrichment(_entities)
    except Exception as e:
        print(str(e), traceback.format_exc())

def startEnrichment(_entities):
    try:

        for filename in _entities:
            result = f'./outputs-for-uploads/{filename}'
            shutil.rmtree(result, ignore_errors=True)
            os.makedirs(result, exist_ok=True)
            path = f'./enrich-data-for-datamodel/{filename}.ttl'
            ####### artworks Graph
            g_data = Graph().parse(path)

            with open('Enrich-heritage-object.rq') as file:
                query_txt = file.read()
                res = g_data.query(query_txt)

            res.serialize(f'{result}/artworks.n3', format='ntriples')
            g = Graph()
            g.parse(f'{result}/artworks.n3', format='ntriples')
            g.namespace_manager.bind('schema', URIRef('https://schema.org/'), replace=True)
            g.serialize(destination=f'{result}/artworks.ttl', format='turtle', encoding='utf-8')
            print(f'{filename} for Artwork graph has been serialized, successfully!')

            # ####### art-periods Graph
            g_data_period = Graph().parse(path)
            with open('Art-period-style.rq') as file:
                query_txt = file.read()
                res = g_data_period.query(query_txt)

            res.serialize(f'{result}/art-periods.n3', format='ntriples') #N3 fine
            g = Graph()
            g.parse(f'{result}/art-periods.n3', format='ntriples')
            g.namespace_manager.bind('schema', URIRef('https://schema.org/'), replace=True)
            g.serialize(destination=f'{result}/art-periods.ttl', format='turtle', encoding='utf-8')
            print(f'{filename} for art-period graph has been serialized, successfully!')

            ######artists Graph
            g_data_period = Graph().parse(path)
            with open('person.rq') as file:
                query_txt = file.read()
                res = g_data_period.query(query_txt)

            res.serialize(f'{result}/artists.n3', format='ntriples')
            g = Graph()
            g.parse(f'{result}/artists.n3', format='ntriples')
            g.namespace_manager.bind('schema', URIRef('https://schema.org/'), replace=True)
            g.serialize(destination=f'{result}/artists.ttl', format='turtle', encoding='utf-8')
            print(f'{filename} for person graph has been serialized, successfully!')

            #####Organization Graph
            g_data_org = Graph()
            with open('Organization.rq') as file:
                query_txt = file.read()
                res = g_data_org.query(query_txt)

            res.serialize(f'{result}/organization.n3', format='ntriples')
            g = Graph()
            g.parse(f'{result}/organization.n3', format='ntriples')
            g.namespace_manager.bind('schema', URIRef('https://schema.org/'), replace=True)
            g.serialize(destination=f'{result}/organization.ttl', format='turtle', encoding='utf-8')
            print(f'organization graph has been serialized, successfully!')

    except Exception as e:
      print(str(e), traceback.format_exc())

startProcessing()

end = timer()
print(timedelta(seconds=end-start))