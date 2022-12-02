# Merge chunk.ttl files

from pyoxigraph import Store, NamedNode, Quad, Literal, parse
import datetime as dt
from rdflib import Graph, URIRef
import os
import shutil
from timeit import default_timer as timer
from datetime import timedelta
import traceback

print('Start: ', dt.datetime.now())

def startProcessing(_path="./enrich-data-for-datamodel/"):
    try:
        _entities = []
        for fName in os.listdir(_path):
            if not fName.endswith('.ttl'):
                continue
            _entities.append(fName.split(".")[0])
        store_chunk_files(_entities, _path)
    except Exception as e:
        print(str(e), traceback.format_exc())

def store_chunk_files(_entities, _path):
    store = Store('rceStore')
    for fileName in _entities:
        inputpath = f"{_path}{fileName}.ttl"
        store.bulk_load(inputpath,  "text/turtle")
        print(f"File {inputpath} stored!")

def datamodel():
    store = Store('rceStore')
    result = f'./outputs-for-uploads/rce/'
    shutil.rmtree(result, ignore_errors=True)
    os.makedirs(result, exist_ok=True)
    enrichWorkObjectStore = Store('enrichWorkObjectStore')
    enrichWorkObjectStore.clear()
    with open('Enrich-heritage-object.rq') as file:
        query_txt = file.read()
        res = store.query(query_txt)

    for r in res:
        print(r)
        enrichWorkObjectStore.add(Quad(r.subject, r.predicate, r.object))
    enrichWorkObjectStore.dump(f'{result}RCE.ttl', "text/turtle")

startProcessing()
datamodel()