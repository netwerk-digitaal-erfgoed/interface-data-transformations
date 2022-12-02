import os
import shutil
import traceback
import rdflib


def startProcessingDataGraph(_path="./upload/"):
    try:
        _entities = []

        for dirPath, dirNames, files in os.walk(_path):
            for fileName in [f for f in files if f.endswith(".ttl")]:
                _entities.append(fileName.split(".")[0])
                dirname = dirPath.split("/")[2]
                processCardinality(_entities, dirPath, dirname)

    except Exception as e:
        print(str(e), traceback.format_exc())

def processCardinality(_entities, _dirPath, dirname, upload = "./upload-correction/"):
    try:
        correction = upload + dirname
        shutil.rmtree(correction, ignore_errors=True)
        os.makedirs(correction, exist_ok=True)
        folderName = _dirPath.split('/')[-1]

        for filename in _entities:
            path = f'{_dirPath + "/" + filename}.ttl'
            g_data = rdflib.Graph()
            g_data.parse(path, format='ttl')
            print(f'{_dirPath} parsed successfully, number of triples: {len(g_data)}')
            predicates = ['<https://schema.org/name>', '<https://schema.org/description>',
                          '<https://schema.org/temporal>','<https://schema.org/dateCreated>',
                          '<https://schema.org/publisher>', '<https://schema.org/isBasedOn>',
                          '<https://schema.org/mainEntityOfPage>']
            for predicate in predicates:
                getByIdentifiers = """
                    DELETE { ?s """+ predicate +""" ?o2 .}
                    WHERE {
                      ?s """+ predicate +""" ?o1, ?o2 .
                      FILTER(?o1 != ?o2)
                      FILTER(str(?o1) > str(?o2))
                    }"""

                g_data.update(getByIdentifiers)


            g_data.serialize(destination=f'{upload}{folderName}/{filename}.ttl', format="ttl")

    except Exception as e:
        print(str(e), traceback.format_exc())

startProcessingDataGraph()
