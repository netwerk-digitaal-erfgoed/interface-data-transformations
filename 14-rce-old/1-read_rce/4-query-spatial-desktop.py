import csv
import re
import pandas as pd
from rdflib import Graph, URIRef, Literal, BNode, XSD
from rdflib.namespace import Namespace
import os
import shutil
import traceback

result_enrichment = './csvforspatial/'

edm = Namespace("http://www.europeana.eu/schemas/edm/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
dcterms = Namespace("http://purl.org/dc/terms/")
aat = Namespace("http://vocab.getty.edu/aat/")
dc = Namespace("http://purl.org/dc/elements/1.1/")


def startProcessing(_path="./enrichment-step-1/"):
    try:
        _entities = []
        for fName in os.listdir(_path):
            if not fName.endswith('ttl'):
                continue
            _entities.append(fName.split(".")[0])
            print(_entities)
        query_spatial(_entities, _path)
    except Exception as e:
        print(str(e), traceback.format_exc())

def query_spatial(_entities, _path):

    for filename in _entities:
        print(filename, _path)
        path = f'{_path}{filename}.ttl'
        g =Graph()
        g.parse(path, format('ttl'))
        print(f'{filename} parsed successfully')  ## [A-z][\u00F0-\u02AF ]{2,} #FILTER(REGEX(str(?b), "[A-z]{3,}", "i"))
        res = g.query("""
        
                    SELECT DISTINCT ?a ?b 
                    WHERE {
                        ?a  <http://purl.org/dc/terms/spatial> ?b .
                
                        
     
                    }""")

        result = []
        for r in res:
            result.append([str(_) for _ in r])
        columns = [ "URI", "Name"]
        res_df = pd.DataFrame(data=result, columns=columns)
        res_df.to_csv('spatial_in_obj.csv')


startProcessing()