import os
import shutil
import traceback
from rdflib import Graph, URIRef
from timeit import default_timer as timer
from datetime import timedelta

start = timer()
print(start)

print("start")

def startChangePrefixes(_path="./invalidperfixes/"):
    
    try:
        _entities = []

        for dirPath, dirNames, files in os.walk(_path):
            for fileName in [f for f in files if f.endswith(".n3")]:
                _entities.append(fileName.split(".")[0])
                dirname = dirPath.split("/")[2]
        processPrefixes(_entities, dirPath, dirname)

    except Exception as e:
        print(str(e), traceback.format_exc())

def processPrefixes(_entities, _dirPath, dirname, upload = "./corrected-prefixes/"):
    try:
        correction = upload
        shutil.rmtree(correction, ignore_errors=True)
        os.makedirs(correction, exist_ok=True)
        folderName = _dirPath.split('/')[-1]

        for filename in _entities:
            path = f'{_dirPath + "/" + filename}.n3'
            
            g = Graph()
            g.parse(path, format='ntriples')                       
            g.namespace_manager.bind('edm', URIRef("http://www.europeana.eu/schemas/edm/" ), replace=True)
            g.namespace_manager.bind('dcterms', URIRef("http://purl.org/dc/terms/"), replace=True)
            g.namespace_manager.bind('dc', URIRef("http://purl.org/dc/elements/1.1/"), replace=True)
            g.namespace_manager.bind('ore', URIRef("http://www.openarchives.org/ore/terms/"), replace=True)
        g.serialize(destination=f'{correction}{filename}.ttl', format='turtle', encoding='utf-8')
        print(f'{filename} is serialize')


    except Exception as e:
        print(str(e), traceback.format_exc())      
     

startChangePrefixes()

end = timer()
print(timedelta(seconds=end-start))