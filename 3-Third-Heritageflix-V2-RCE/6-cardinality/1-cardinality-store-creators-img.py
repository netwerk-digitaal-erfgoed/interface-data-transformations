from pyoxigraph import Store, NamedNode, Quad, Literal, parse
import datetime as dt
from rdflib import Graph, URIRef
import os
import shutil
from timeit import default_timer as timer
from datetime import timedelta
import traceback

print('Start: ', dt.datetime.now())


def processCardinality():
    store = Store('enrichWorkObjectStore')
    result = f'./outputs-for-cardinality/rce/'
    # shutil.rmtree(result, ignore_errors=True)
    # os.makedirs(result, exist_ok=True)
    enrichWorkObjectStore = Store('cardinalityOutput')
      enrichWorkObjectStore.clear()
    predicates = ['<https://schema.org/description>',
                   '<https://schema.org/temporal>',
                  '<https://schema.org/dateCreated>',
                  '<https://schema.org/name>',
                  '<https://schema.org/publisher>',
                  '<https://schema.org/isBasedOn>',
                  '<https://schema.org/mainEntityOfPage>',
                  '<https://schema.org/image>',
                  '<https://schema.org/creator>',
                  '<https://schema.org/encodingFormat>',
                  '<https://schema.org/contentUrl>',
                  '<https://schema.org/contentUrl/license>']
    for predicate in predicates:
        query_txt = """
             DELETE { ?s """ + predicate + """ ?o2 .}
             WHERE {
               ?s """ + predicate + """ ?o1, ?o2 .
               FILTER(?o1 != ?o2)
               FILTER(str(?o1) > str(?o2))
             }"""

        print(query_txt)
        store.update(query_txt)
    store.dump(f'{result}RCE-cardinality-2.ttl', "text/turtle")




processCardinality()
