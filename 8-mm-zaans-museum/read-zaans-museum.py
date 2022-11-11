from rdflib import Graph, URIRef, RDF, OWL, Namespace, Literal
from rdflib import DCTERMS, SKOS, DC

import numpy as np
import pandas as pd

# Lees mm-zaans-museum.csv en creeer RDF data conform aanwezig.
# Vervolgstap is het aanpassen van het datamodel en zm = df

zm = pd.read_csv('mm-zaans-museum.csv')
zm.to_excel('mm-zaans-museum.xlsx')
eerste_regels = zm[pd.notna(zm['rdf:RDF - edm:ProvidedCHO - rdf:about'])].index

# Vul lege uri's verder in
zm['rdf:RDF - edm:ProvidedCHO - rdf:about'] = zm['rdf:RDF - edm:ProvidedCHO - rdf:about'].fillna(method="pad")
zm["rdf:RDF - ore:Aggregation - rdf:about"] = zm["rdf:RDF - ore:Aggregation - rdf:about"].fillna(method="pad")
zm.to_excel('zaansm-test.xlsx')

g = Graph()
EDM = Namespace("http://www.europeana.eu/schemas/edm/")
EDMFP = Namespace("http://www.europeanafashion.eu/edmfp/technique/")
ORE = Namespace("http://www.openarchives.org/ore/terms/Aggregation/")
DCTERMS = Namespace("http://purl.org/dc/terms/")
DC = Namespace("http://purl.org/dc/elements/1.1/")
SKOS = Namespace ('http://www.w3.org/2004/02/skos/core#')
RDF = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
g.bind('skos', SKOS)
g.bind('edm', EDM)
g.bind('ore', ORE)
g.bind('edmfp', EDMFP)
g.bind('dc', DC)
g.bind('dcterms', DCTERMS)
g.bind('rdf', RDF)

for index in eerste_regels:
    g.add((URIRef(zm["rdf:RDF - ore:Aggregation - rdf:about"][index]) , RDF.type , ORE.aggregation))
    g.add((URIRef(zm["rdf:RDF - edm:ProvidedCHO - rdf:about"][index]) , RDF.type , EDM.ProvidedCHO))
    g.add((URIRef(zm["rdf:RDF - ore:Aggregation - rdf:about"][index]) , EDM.aggregatedCHO , 
                                            URIRef(zm["rdf:RDF - edm:ProvidedCHO - rdf:about"][index])))

    g.add((URIRef(zm["rdf:RDF - ore:Aggregation - rdf:about"][index]) , EDM.providers ,
                                            Literal(zm["rdf:RDF - ore:Aggregation - edm:provider - edm:Agent - skos:prefLabel"][index]))) ###checks

    g.add((URIRef(zm["rdf:RDF - ore:Aggregation - rdf:about"][index]) , EDM.isShownBy ,
                                            Literal(zm["rdf:RDF - ore:Aggregation - edm:isShownBy - edm:WebResource - rdf:about"][index])))

    g.add((URIRef(zm["rdf:RDF - ore:Aggregation - rdf:about"][index]) , EDM.isShownAt ,
                                            Literal(zm["rdf:RDF - ore:Aggregation - edm:isShownAt - edm:WebResource - rdf:about"][index])))

    g.add((URIRef(zm["rdf:RDF - ore:Aggregation - rdf:about"][index]) , EDM.provider , 
                                            Literal(zm["rdf:RDF - ore:Aggregation - edm:provider - edm:Agent - rdf:about"][index])))
    # g.add((URIRef(zm["rdf:RDF - ore:Aggregation - edm:provider - edm:Agent - rdf:about"][index]), SKOS.prefLabel,
    #        Literal(zm["rdf:RDF - ore:Aggregation - edm:provider - edm:Agent - skos:prefLabel"][index]))) ###check

    g.add((URIRef(zm["rdf:RDF - ore:Aggregation - rdf:about"][index]) , EDM.dataProvider ,
                                            Literal(zm["rdf:RDF - ore:Aggregation - edm:dataProvider - edm:Agent - skos:prefLabel"][index],
                                               lang=zm["rdf:RDF - ore:Aggregation - edm:dataProvider - edm:Agent - skos:prefLabel - xml:lang"][index])))

    g.add((URIRef(zm["rdf:RDF - ore:Aggregation - rdf:about"][index]) , EDM.rights ,
                                            Literal(zm["rdf:RDF - ore:Aggregation - edm:rights - rdf:resource"][index])))

for index in zm.index:
    for col in zm.columns:
        if col == "rdf:RDF - edm:ProvidedCHO - dc:title" and pd.notna(zm[col][index]):
            g.add((URIRef(zm["rdf:RDF - edm:ProvidedCHO - rdf:about"][index])  , DC.title , Literal(zm[col][index], 
                                                lang=zm["rdf:RDF - edm:ProvidedCHO - dc:title - xml:lang"][index])))  

        if col == "rdf:RDF - edm:ProvidedCHO - edm:type" and pd.notna(zm[col][index]):
            g.add((URIRef(zm["rdf:RDF - edm:ProvidedCHO - rdf:about"][index])  , EDM.type , Literal(zm[col][index])))

        if col == "rdf:RDF - edm:ProvidedCHO - dcterms:medium - rdf:resource" and pd.notna(zm[col][index]):
            g.add((URIRef(zm["rdf:RDF - edm:ProvidedCHO - rdf:about"][index])  , DCTERMS.medium , Literal(zm[col][index])))

        if col == "rdf:RDF - edm:ProvidedCHO - dc:identifier" and pd.notna(zm[col][index]):
            g.add((URIRef(zm["rdf:RDF - edm:ProvidedCHO - rdf:about"][index])  , DC.identifier, Literal(zm[col][index])))

        if col == "rdf:RDF - edm:ProvidedCHO - dc:type - skos:Concept - rdf:about" and pd.notna(zm[col][index]):
            g.add((URIRef(zm["rdf:RDF - edm:ProvidedCHO - rdf:about"][index])  , DC.additionalType, URIRef(zm["rdf:RDF - edm:ProvidedCHO - dc:type - skos:Concept - rdf:about"][index])))
        if col == "dc:type_URI" and pd.notna(zm[col][index]):
            g.add((URIRef(zm["rdf:RDF - edm:ProvidedCHO - rdf:about"][index])  , DC.type, URIRef(zm["dc:type_URI"][index])))
        if col == "dcterms:medium_URI" and pd.notna(zm[col][index]):
            g.add((URIRef(zm["rdf:RDF - edm:ProvidedCHO - rdf:about"][index])  , DCTERMS.medium_URI, URIRef(zm["dcterms:medium_URI"][index])))
        if col == "rdf:RDF - edm:ProvidedCHO - dcterms:medium" and pd.notna(zm[col][index]):
            g.add((URIRef(zm["rdf:RDF - edm:ProvidedCHO - rdf:about"][index]), DCTERMS.martial, Literal(zm[col][index])))

        if col == "edmfp:technique_URI" and pd.notna(zm[col][index]):
            g.add((URIRef(zm["rdf:RDF - edm:ProvidedCHO - rdf:about"][index]), EDMFP.technique_URI, URIRef(zm["edmfp:technique_URI"][index])))

        if col == "rdf:RDF - edm:ProvidedCHO - edmfp:technique" and pd.notna(zm[col][index]):
            g.add((URIRef(zm["rdf:RDF - edm:ProvidedCHO - rdf:about"][index]), EDMFP.techniques , Literal(zm[col][index])))

        if col == "rdf:RDF - edm:ProvidedCHO - dc:description" and pd.notna(zm[col][index]):
            g.add((URIRef(zm["rdf:RDF - edm:ProvidedCHO - rdf:about"][index]), DC.description, Literal(zm[col][index],
                                                lang=zm["rdf:RDF - edm:ProvidedCHO - dc:description - xml:lang"][index])))

        if col == "rdf:RDF - edm:ProvidedCHO - dcterms:created" and pd.notna(zm[col][index]):
            g.add((URIRef(zm["rdf:RDF - edm:ProvidedCHO - rdf:about"][index]), DCTERMS.created, Literal(zm[col][index],
                                               lang=zm["rdf:RDF - edm:ProvidedCHO - dcterms:created - xml:lang"][index])))

        if col == "rdf:RDF - ore:Aggregation - edm:dataProvider - edm:Agent - skos:prefLabel" and pd.notna(zm[col][index]):
            g.add((URIRef(zm["rdf:RDF - edm:ProvidedCHO - rdf:about"][index]), EDM.Agent, Literal(zm[col][index],
                                               lang=zm["rdf:RDF - ore:Aggregation - edm:dataProvider - edm:Agent - skos:prefLabel - xml:lang"][index])))

g.serialize('zaams-museum.ttl')