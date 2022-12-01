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


    # predicates = ['<https://schema.org/image>',
    #               '<https://schema.org/creator>']
    # for predicate in predicates:
    query_txt = """
         DELETE { ?s schema:image ?o1 .
           ?image rdf:type schema:ImageObject ;
 		    schema:contentUrl ?isShownBy2 ;
  	        schema:encodingFormat ?img ;
		    schema:license ?rights.}
         WHERE {       
    ?s
        rdf:type schema:CreativeWork ;
		schema:description ?discribeNL ;
		schema:about ?about ;
		schema:publisher <https://beeldbank.cultureelerfgoed.nl/> ;
		schema:creator ?creators ; 
  		schema:temporal ?temporal ; 
		schema:dateCreated ?yearCreated;
        schema:contentLocation ?contentLocation ;
    	schema:mainEntityOfPage ?isShownAt ; 
		schema:isBasedOn ?heritageObject ; 
    	schema:image ?o1, ?o2 .
    	FILTER(?o1 != ?o2)
        FILTER(str(?o1) > str(?o2))
    ?image rdf:type schema:ImageObject ;
 		schema:contentUrl ?isShownBy2 ;
  	    schema:encodingFormat ?img ;
		schema:license ?rights.
    ?creators rdf:type schema:Person ;
			schema:name ?creator .

         }"""

    print(query_txt)
    store.update(query_txt)
    store.dump(f'{result}RCE-cardinality-img.ttl', "text/turtle")


processCardinality()
