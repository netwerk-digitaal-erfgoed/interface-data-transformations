import re
from rdflib import Graph

i = 0
stap = 100
rce_total = Graph()
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
            # part are valid rdf/xml strings
            g = Graph().parse(data=part, format='xml')
            rce += g
            j += 1
            if j%1000==0:
               print(i,j)
        #rce_total += rce
        try:
            rce.serialize(f'rce3_{i}.ttl')
        except:
            #TODO: Fix the uri in this chunk
            print(f'Chunk {i} {j} has uri coding error.')
        # TODO: Add storage in pyoxigraph store based on the chunk ttl's

# TODO: Mogelijke verbetering:
# Fix chunk door begin tot <RDF te verwijderen en vanaf eind tot </RDF te verwijderen.
# De gesplitse is dan dus weg !:)
