from rdflib import Graph
import os
import shutil
from timeit import default_timer as timer
from datetime import timedelta
import traceback
import urllib.request
import csv

import imageio.v2 as imageio

start = timer()
print(start)

result_process = './report-imags/'

shutil.rmtree(result_process, ignore_errors=True)
os.makedirs(result_process, exist_ok=True)

def startAPIProcessing(_path="./inputs/"):
    try:
        _entities = []
        for fName in os.listdir(_path):
            if not fName.endswith('.ttl'):
                continue
            _entities.append(fName.split(".")[0])
            startImageGathering(_entities)
    except Exception as e:
        print(str(e), traceback.format_exc())


def startImageGathering(_entities):
    try:
        for filename in _entities:
            result = f'./upload-pic/{filename}/'
            shutil.rmtree(result, ignore_errors=True)
            os.makedirs(result, exist_ok=True)
            path = f'./upload/{filename}.ttl'
            print(path)
            g = Graph()
            g.parse(path, format("ttl"))
            print(filename + " Parsed successfully")
            getByIdentifiers = """
            SELECT ?o ?ss
            WHERE {
                ?ss  ?p  ?s.
                ?s schema:contentUrl ?o .

            }"""
            qres = g.query(getByIdentifiers)
            for index, row in enumerate(qres):
                im = imageio.imread(row.o)
                width, height, channel = im.shape
                print('width:  ', width, row.o)
                print('height: ', height, row.o)
                if height > width:
                    orientation  = "Portrait"
                elif width > height:
                    orientation  = "landscape"
                elif height == width:
                    orientation = "square"

                print(orientation, row.o)

            with open(result + f'{filename}.csv', 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, quoting=csv.QUOTE_ALL, delimiter=',', quotechar='"')
                f.write(",".join(["uri-records","width","height","orientation", "uri-img"]))
                f.write("\n")
                for row in qres:
                    sub = row.ss.split("/n")[0]
                    obj = row.o.split("/n")[0]
                    writer.writerow([sub,width,height,orientation, obj])
            print(f'{filename} saved in this path: {result}')

    except Exception as e:
      print(str(e), traceback.format_exc())

startAPIProcessing()

end = timer()
print(timedelta(seconds=end-start))