# Merge chunk.ttl files

from pyoxigraph import Store, NamedNode, Quad, Literal, parse
import datetime as dt
import pandas as pd

print('Start: ', dt.datetime.now())

def query_store():
    store = Store('rceStore')

    res = store.query("""
    select ?s ?val
    where {
        ?s  <http://purl.org/dc/elements/1.1/subject> ?val .
        filter contains(?val,'kerk') 
    }
    """)
    result = []
    for r in res:
        result.append([str(_) for _ in r])
    columns = result[0]
    res_df = pd.DataFrame(data=result, columns=columns)
    res_df.to_excel('kerk_in_obj.xlsx')

query_store()