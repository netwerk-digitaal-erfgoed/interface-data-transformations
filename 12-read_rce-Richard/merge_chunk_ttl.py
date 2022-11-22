# Merge chunk.ttl files

from pyoxigraph import Store, NamedNode, Quad, Literal, parse
import datetime as dt

print('Start: ', dt.datetime.now())

def store_chunk_files():
    store = Store('rceStore')
    for i in range(1,152):
        path = f"./rce3_{i}.ttl"
        print(path)
        try:
            store.bulk_load(path,  "text/turtle")
        except:
            print(f"File {path} does not exist")
        if i%10==0:
            print(i)

def query_store():
    store = Store('rceStore')

    res = store.query("""
    select (count(?cho) as ?aantal_cho) 
    where {
        ?cho  <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.europeana.eu/schemas/edm/ProvidedCHO> .
    }
    """)
    print(list(res))

    res = store.query("""
    select (count(?agg) as ?aantal_agg)
    where {
        ?agg  <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.openarchives.org/ore/terms/Aggregation> .
    }
    """)
    print(list(res))

    res = store.query("""
    select distinct ?clss
    where {
        ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?clss.
    } 
    """)
    print(list(res))

    #[<QuerySolution clss=<NamedNode value=http://www.europeana.eu/schemas/edm/ProvidedCHO>>, 
    #<QuerySolution clss=<NamedNode value=http://www.openarchives.org/ore/terms/Aggregation>>]

store_chunk_files()

query_store()