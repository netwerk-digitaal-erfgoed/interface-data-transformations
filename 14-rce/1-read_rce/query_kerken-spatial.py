# Merge chunk.ttl files

from pyoxigraph import Store
import datetime as dt
import pandas as pd
import csv

print('Start: ', dt.datetime.now())

def query_store():
    store = Store('rceStore')

    res = store.query("""
    select ?s ?val
    where {
        ?s  <http://purl.org/dc/terms/spatial> ?val .   
        ?s  <http://purl.org/dc/elements/1.1/subject> ?val2 .
        
        filter contains(?val2,'kerk') 
    }
    """)
    result = []
    for r in res:
        result.append([str(_) for _ in r])
    columns = [ "URI", "Name"]
    res_df = pd.DataFrame(data=result, columns=columns)
    res_df.to_csv('spatial_in_obj.csv', quoting=csv.QUOTE_NONE , quotechar='"', escapechar = " ")

query_store()