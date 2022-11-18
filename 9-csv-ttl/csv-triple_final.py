import os
import shutil
import traceback
from rdflib import Graph, URIRef, RDF, OWL, Namespace, Literal
import pandas as pd
import urllib.parse


def startProcessing(_path="./csv/"):
    try:
        _entities = []
        for fName in os.listdir(_path):

            if not fName.endswith('.csv'):
                continue
            _entities.append(fName.split(".")[0])
            # print(_entities)

        parse_csv(_entities)
    except Exception as e:
        print(str(e), traceback.format_exc())

def parse_csv(_entities, cleanCSV = "./clean-csv/" ,result = "./enrich-step1/" ):

    shutil.rmtree(result, ignore_errors=True)
    os.makedirs(result , exist_ok=True)
    shutil.rmtree(cleanCSV, ignore_errors=True)
    os.makedirs(cleanCSV , exist_ok=True)
    for fileName in _entities:
        path = f'./csv/'

        zm = pd.read_csv(f'{path}{fileName}.csv', delimiter=',')
        zm.to_excel(f'{cleanCSV}{fileName}.xlsx')
        eerste_regels = zm[pd.notna(zm['rdf:RDF - edm:ProvidedCHO - rdf:about'])].index
        zm['rdf:RDF - edm:ProvidedCHO - rdf:about'] = zm['rdf:RDF - edm:ProvidedCHO - rdf:about'].fillna(
            method="pad")
        zm["rdf:RDF - ore:Aggregation - rdf:about"] = zm["rdf:RDF - ore:Aggregation - rdf:about"].fillna(
            method="pad")
        zm.to_excel(f'{cleanCSV}{fileName}-work.xlsx')
        
        g = Graph()
        EDM = Namespace("http://www.europeana.eu/schemas/edm/")
        EDMFP = Namespace("http://www.europeanafashion.eu/edmfp/technique/")
        ORE = Namespace("http://www.openarchives.org/ore/terms/")
        DCTERMS = Namespace("http://purl.org/dc/terms/")
        DC = Namespace("http://purl.org/dc/elements/1.1/")
        SKOS = Namespace('http://www.w3.org/2004/02/skos/core#')
        RDF = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
        g.bind('skos', SKOS)
        g.bind('edm', EDM)
        g.bind('ore', ORE)
        g.bind('edmfp', EDMFP)
        g.bind('dc', DC)
        g.bind('dcterms', DCTERMS)
        g.bind('rdf', RDF)
        for index in eerste_regels:
            subject_providedCHO_aggregation = URIRef(urllib.parse.quote(zm["rdf:RDF - ore:Aggregation - rdf:about"][index]).replace('%3A', ':'))
            g.add((subject_providedCHO_aggregation, RDF.type, ORE.Aggregation))
            g.add((URIRef(urllib.parse.quote(zm["rdf:RDF - edm:ProvidedCHO - rdf:about"][index]).replace('%3A', ':')), RDF.type, EDM.ProvidedCHO))
          

            g.add((subject_providedCHO_aggregation, EDM.aggregatedCHO, URIRef(urllib.parse.quote(zm["rdf:RDF - edm:ProvidedCHO - rdf:about"][index]).replace('%3A', ':'))))
            try:
                g.add((subject_providedCHO_aggregation, DC.creator,
                       Literal(zm["rdf:RDF - dc:creator - rdf:about"][index])))
            except:
                #print("Warning: No creator in dataset.")
                pass

            g.add((subject_providedCHO_aggregation, EDM.providers,
                   Literal(zm["rdf:RDF - ore:Aggregation - edm:provider - edm:Agent - skos:prefLabel"][
                               index])))
            
            g.add((subject_providedCHO_aggregation, EDM.isShownBy,
                   URIRef(zm["rdf:RDF - ore:Aggregation - edm:isShownBy - edm:WebResource - rdf:about"][index])))
            
            g.add((subject_providedCHO_aggregation, EDM.isShownAt,
                   URIRef(zm["rdf:RDF - ore:Aggregation - edm:isShownAt - edm:WebResource - rdf:about"][index])))
            
            g.add((subject_providedCHO_aggregation, EDM.provider,
                   URIRef(zm["rdf:RDF - ore:Aggregation - edm:provider - edm:Agent - rdf:about"][index])))
            
            g.add((subject_providedCHO_aggregation, EDM.dataProvider,
                   Literal(zm["rdf:RDF - ore:Aggregation - edm:dataProvider - edm:Agent - skos:prefLabel"][index],
                           lang=zm[
                               "rdf:RDF - ore:Aggregation - edm:dataProvider - edm:Agent - skos:prefLabel - xml:lang"][
                               index])))

            g.add((subject_providedCHO_aggregation, EDM.rights,
                   URIRef(zm["rdf:RDF - ore:Aggregation - edm:rights - rdf:resource"][index])))
        for index in zm.index:
            for col in zm.columns:
                subject_providedCHO = URIRef(urllib.parse.quote(zm["rdf:RDF - edm:ProvidedCHO - rdf:about"][index]).replace('%3A', ':'))
                if col == "rdf:RDF - edm:ProvidedCHO - dc:title" and pd.notna(zm[col][index]):
                    g.add((subject_providedCHO, DC.title,
                           Literal(zm[col][index],
                                   lang=zm["rdf:RDF - edm:ProvidedCHO - dc:title - xml:lang"][index])))

                if col == "rdf:RDF - edm:ProvidedCHO - edm:type" and pd.notna(zm[col][index]):
                    g.add((subject_providedCHO, EDM.type,
                           Literal(zm[col][index])))
                
                if col == "rdf:RDF - edm:ProvidedCHO - dcterms:medium - rdf:resource" and pd.notna(zm[col][index]):
                    g.add((subject_providedCHO, DCTERMS.medium,
                           Literal(zm[col][index])))
                
                if col == "rdf:RDF - edm:ProvidedCHO - dc:identifier" and pd.notna(zm[col][index]):
                    g.add((subject_providedCHO, DC.identifier,
                           Literal(zm[col][index])))
                
                if col == "rdf:RDF - edm:ProvidedCHO - dc:type - skos:Concept - rdf:about" and pd.notna(
                        zm[col][index]):
                    g.add((subject_providedCHO, DC.additionalType,
                           URIRef(zm["rdf:RDF - edm:ProvidedCHO - dc:type - skos:Concept - rdf:about"][index])))
                if col == "dc:type_URI" and pd.notna(zm[col][index]):
                    g.add((subject_providedCHO, DC.type,
                           URIRef(zm["dc:type_URI"][index])))
                if col == "dcterms:medium_URI" and pd.notna(zm[col][index]):
                    g.add((subject_providedCHO, DCTERMS.medium_URI,
                           URIRef(zm["dcterms:medium_URI"][index])))
                if col == "rdf:RDF - edm:ProvidedCHO - dcterms:medium" and pd.notna(zm[col][index]):
                    g.add((subject_providedCHO, DCTERMS.martial,
                           Literal(zm[col][index])))
                
                if col == "edmfp:technique_URI" and pd.notna(zm[col][index]):
                    g.add((subject_providedCHO, EDMFP.technique_URI,
                           URIRef(zm["edmfp:technique_URI"][index])))
                
                if col == "rdf:RDF - edm:ProvidedCHO - edmfp:technique" and pd.notna(zm[col][index]):
                    g.add((subject_providedCHO, EDMFP.techniques,
                           Literal(zm[col][index])))
                
                if col == "rdf:RDF - edm:ProvidedCHO - dc:description" and pd.notna(zm[col][index]):
                    g.add((subject_providedCHO, DC.description,
                           Literal(zm[col][index],
                                   lang=zm["rdf:RDF - edm:ProvidedCHO - dc:description - xml:lang"][index])))
                
                if col == "rdf:RDF - edm:ProvidedCHO - dcterms:created" and pd.notna(zm[col][index]):
                    g.add((subject_providedCHO, DCTERMS.created,
                           Literal(zm[col][index],
                                   lang=zm["rdf:RDF - edm:ProvidedCHO - dcterms:created - xml:lang"][index])))
                
                if col == "rdf:RDF - ore:Aggregation - edm:dataProvider - edm:Agent - skos:prefLabel" and pd.notna(
                        zm[col][index]):
                    g.add((subject_providedCHO, EDM.Agent,
                           Literal(zm[col][index],
                                   lang=zm[
                                       "rdf:RDF - ore:Aggregation - edm:dataProvider - edm:Agent - skos:prefLabel - xml:lang"][
                                       index])))

        g.serialize(f'{result}{fileName}.ttl')

        print(f'{path}{fileName}.csv Done!')




startProcessing()

