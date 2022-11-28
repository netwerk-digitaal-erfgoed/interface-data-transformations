import csv
import os
from rdflib import Graph
import shutil
import traceback
from timeit import default_timer as timer
from datetime import timedelta

start = timer()
print(start)

def startProcessing(_path="./converted/"):
    try:
        _entities = []
        for fName in os.listdir(_path):
            if not fName.endswith('.ttl'):
                continue
            _entities.append(fName.split(".")[0])
        extractArtForm(_entities)
    except Exception as e:
        print(str(e), traceback.format_exc())

def extractArtForm(_entities,result ='./art_type_All/'):
    shutil.rmtree(result, ignore_errors=True)
    os.makedirs(result, exist_ok=True)
    for url in _entities:
        gPath = f'./converted/{url}.ttl'
        g = Graph()
        g.parse(gPath, format("ttl"))
        print(url + " Parsed successfully")

        getByIdentifiers = """
        SELECT DISTINCT ?a ?b
        WHERE {
            ?a <http://purl.org/dc/elements/1.1/type> ?b .
    
        }"""

        qres = g.query(getByIdentifiers)

        with open(result + f'{url}.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL, delimiter=',', quotechar='"')#quotechar='',
            f.write(",".join(["uri", "type"]))
            f.write("\n")
            for row in qres:
                sub = row.a.split("/n")[0]
                obj = row.b.split("/n")[0]
                writer.writerow([sub, obj])


end = timer()
print(timedelta(seconds=end-start))
startProcessing()
