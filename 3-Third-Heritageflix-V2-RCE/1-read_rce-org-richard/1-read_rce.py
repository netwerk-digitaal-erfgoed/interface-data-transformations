import re
from rdflib import Graph
import shutil
import os


finalPath = './invalidperfixes/'

shutil.rmtree(finalPath, ignore_errors=True)
os.makedirs(finalPath, exist_ok=True)


i = 0
stap = 100
rce_total = Graph()
## here change the name of input xml/rdf file
with open('rce-beeldbank.xml', 'rb') as f:
    for chunk in iter(lambda: f.read(10000000), ''):
        if len(chunk)==0:
            break
        i = i + 1
        print('Chunk: ', i)
        rdfStriper = re.findall('<rdf:RDF.*?</rdf:RDF>', chunk.decode('UTF-8'), re.DOTALL)

        rce = Graph()
        j = 0
        for part in rdfStriper:
            g = Graph().parse(data=part, format='xml')
            rce += g
            j += 1
            if j%1000==0:
               print(i,j)
        try:
            rce.serialize(f'{finalPath}rce3_{i}.n3')
        except:
            print(f'Chunk {i} {j} has uri coding error.')


