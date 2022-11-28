import pyshacl
import rdflib
import os
import shutil
import traceback

def startProcessingDataGraph(_path="./upload/"):
    try:
        _entities = []

        for dirPath, dirNames, files in os.walk(_path):
            _entities = []
            for fileName in [f for f in files if f.endswith(".ttl")]:
                _entities.append(fileName.split(".")[0])
                dirname = dirPath.split("/")[2]
                validationReport(_entities, dirPath, dirname)

    except Exception as e:
        print(str(e), traceback.format_exc())

def validationReport(_entities, _dirPath, dirname, shaclepath="./shape/shapes.ttl", validationReport = "./validationReport/"):
    try:
        validationReport = validationReport + dirname
        shutil.rmtree(validationReport, ignore_errors=True)
        os.makedirs(validationReport, exist_ok=True)
        for filename in _entities:

            pathgraph = f'{_dirPath + "/" + filename}.ttl'
            data_graph = rdflib.Graph().parse(pathgraph)
            shape_graph = rdflib.Graph().parse(shaclepath)

            r = pyshacl.validate(data_graph,
                                 shacl_graph=shape_graph,
                                 ont_graph=None,
                                 inference=None,  # 'rdfs',
                                 abort_on_first=False,
                                 allow_infos=False,
                                 allow_warnings=False,
                                 meta_shacl=False,
                                 advanced=True,
                                 js=False,
                                 debug=False)

            conforms, results_graph, results_text = r
            results_graph.serialize(f'{validationReport}/{filename}.ttl')
            print(f'find the validation report in this path: {validationReport}/{filename}')

    except Exception as e:
        print(str(e), traceback.format_exc())

startProcessingDataGraph()

