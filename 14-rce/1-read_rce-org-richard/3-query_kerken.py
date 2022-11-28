

from pyoxigraph import Store, NamedNode, Quad, Literal, parse
import datetime as dt
import pandas as pd

print('Start: ', dt.datetime.now())

def query_store():
    store = Store('rceStore')

    res = store.query("""
    select ?s ?val
    where {
    
        ?s  <http://purl.org/dc/elements/1.1/subject> ?val2 .
        filter contains(?val2,'kerk') 
    }
    """)
    result = []
    for r in res:
        result.append([str(_) for _ in r])
    columns = ["URIs", "Names"]
    res_df = pd.DataFrame(data=result, columns=columns)
    res_df.to_csv('kerk_in_obj.csv')

query_store()