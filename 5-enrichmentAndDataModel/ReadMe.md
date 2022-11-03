# File outputs:

#### https://github.com/netwerk-digitaal-erfgoed/interface-usable-visible/blob/main/heritageflix/backend/publishers.ttl

#### mauritshuis   and van-abbe-museum

Following the data model:

PREFIX ore: <http://www.openarchives.org/ore/terms/>

PREFIX edm: <http://www.europeana.eu/schemas/edm/>

PREFIX schema: <http://schema.org/>

PREFIX cd: <http://citydata.wu.ac.at/ns#>

PREFIX dc: <http://purl.org/dc/elements/1.1/>

PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

PREFIX dcterms: <http://purl.org/dc/terms/>

PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>


CONSTRUCT {

  ?heritageObject

        rdf:type schema:VisualArtwork ;

		schema:artform ?artform;

		schema:name ?titleNL ;

		schema:description ?discription ;

		schema:publisher <https://www.mauritshuis.nl/> ;

		schema:creator ?creator;

  		schema:temporal ?created ;

		schema:dateCreated ?yearCreated;

		schema:mainEntityOfPage ?isShownAt;

		schema:isBasedOn ?heritageObject ;

		schema:temporalCoverage ?temporalCoverage ;

    	schema:image ?image.

  ?image rdf:type schema:ImageObject ;

  		schema:isShownBy ?isShownBy;

  	    schema:encodingFormat ?img ;

		schema:license ?rights.
}

WHERE {

    ?heritageObject a edm:ProvidedCHO ;

		dcterms:artform ?artform;

		dc:title ?title ;

		dc:description ?discription ;

		dcterms:creators ?creator ;

  		dcterms:created ?created ;

		dcterms:dateCreated ?yearCreated ;

		edm:temporalCoverage ?temporalCoverage ;

		edm:image ?image.

		bind(strlang(str(?title), "nl") as ?titleNL)

		FILTER(LANG(?discription) = "nl")

	?aggregation a ore:Aggregation ;

		edm:aggregatedCHO ?heritageObject ;#setting 1 for mauritshuis

		edm:isShownBy ?isShownBy ; #setting 1 for mauritshuis

		edm:rights ?rights .#setting 1

		OPTIONAL { ?aggregation edm:isShownAt ?isShownAt }#setting 2 for mauritshuis

		OPTIONAL { ?aggregation dcterms:format ?img }#setting 2 for mauritshuis


}

PREFIX ore: <http://www.openarchives.org/ore/terms/>

PREFIX edm: <http://www.europeana.eu/schemas/edm/>

PREFIX schema: <http://schema.org/>

PREFIX cd: <http://citydata.wu.ac.at/ns#>

PREFIX dc: <http://purl.org/dc/elements/1.1/>

PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

PREFIX dcterms: <http://purl.org/dc/terms/>

CONSTRUCT {

  ?creator

	rdf:type schema:Person;

	schema:creator ?creator;

	schema:name ?personNL .

}

WHERE {

    ?heritageObject a edm:ProvidedCHO ;

		dcterms:creators ?creator ;

		dc:description ?discription ;

		dc:creator ?person .

		BIND(STRLANG(str(?person), "nl") as ?personNL)

		FILTER(LANG(?discription) = "nl")
}

PREFIX ore: <http://www.openarchives.org/ore/terms/>

PREFIX edm: <http://www.europeana.eu/schemas/edm/>

PREFIX schema: <http://schema.org/>

PREFIX cd: <http://citydata.wu.ac.at/ns#>

PREFIX dc: <http://purl.org/dc/elements/1.1/>

PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

PREFIX dcterms: <http://purl.org/dc/terms/>

CONSTRUCT {

?temporalCoverage

  a schema:DefinedTerm ;

  schema:name ?name;

  schema:startDate ?startDate;

  schema:endDate ?endDate.

}

WHERE {

?temporalCoverage

	dcterms:startDate ?startDate ;

	dcterms:name ?name .

    OPTIONAL { ?temporalCoverage dcterms:endDate ?endDate }

}


#### stedelijk-museum-schiedam:????
isShowby must be optional

descriptions is not with @nl 

person has a problem

no description with NL

CONSTRUCT {

  ?heritageObject

        rdf:type schema:VisualArtwork ;

		schema:artform ?artform;

		schema:name ?titleNL ;

		schema:publisher <https://www.stedelijkmuseumschiedam.nl/> ;

		schema:creator ?creator;

  		schema:temporal ?created ;

		schema:dateCreated ?yearCreated;

		schema:mainEntityOfPage ?isShownAt;

		schema:isBasedOn ?heritageObject ;

		schema:temporalCoverage ?temporalCoverage ;

    	schema:image ?image.

  ?image rdf:type schema:ImageObject ;

  		schema:isShownBy ?isShownBy;

  	    schema:encodingFormat ?img ;

		schema:license ?rights.
}

WHERE {

    ?heritageObject a edm:ProvidedCHO ;

		dcterms:artform ?artform;

		dc:title ?title ;

		dcterms:creators ?creator ;

  		dcterms:created ?created ;

		dcterms:dateCreated ?yearCreated ;

		edm:temporalCoverage ?temporalCoverage ;

		edm:image ?image.

		bind(strlang(str(?title), "nl") as ?titleNL)

	?aggregation a ore:Aggregation ;

		edm:aggregatedCHO ?heritageObject ;#setting 1 for mauritshuis

		edm:rights ?rights .#setting 1

		OPTIONAL { ?aggregation edm:isShownAt ?isShownAt }#setting 2 for mauritshuis

		OPTIONAL { ?aggregation dcterms:format ?img }#setting 2 for mauritshuis

		OPTIONAL { ?aggregation edm:isShownBy ?isShownBy }#setting 2 for mauritshuis


}


CONSTRUCT {

  ?creator

	rdf:type schema:Person;

	schema:creator ?creator;

	schema:name ?personNL .

}

WHERE {

    ?heritageObject a edm:ProvidedCHO ;

		dcterms:creators ?creator ;

		dc:creator ?person .

		BIND(STRLANG(str(?person), "nl") as ?personNL)

}



#### belvedere:

description has problem  and art period from previous step must be checked

CONSTRUCT {

  ?heritageObject

        rdf:type schema:VisualArtwork ;

		schema:artform ?artform;

		schema:name ?titleNL ;

		schema:description ?discribeNL ;

		schema:publisher <https://www.museumbelvedere.nl/> ;

		schema:creator ?creator;

  		schema:temporal ?created ;

		schema:dateCreated ?yearCreated;

		schema:mainEntityOfPage ?isShownAt;

		schema:isBasedOn ?heritageObject ;

		schema:temporalCoverage ?temporalCoverage ;

    	schema:image ?image.

  ?image rdf:type schema:ImageObject ;

  		schema:isShownBy ?isShownBy;

  	    schema:encodingFormat ?img ;

		schema:license ?rights.

}

WHERE {

    ?heritageObject a edm:ProvidedCHO ;

		dcterms:artform ?artform;

		dc:title ?title ;

		dc:description ?discription ;

		dcterms:creators ?creator ;

  		dcterms:created ?created ;

		dcterms:dateCreated ?yearCreated ;

		edm:temporalCoverage ?temporalCoverage ;

		edm:image ?image.

		bind(strlang(str(?title), "nl") as ?titleNL)

		BIND(STRLANG(?discription, "nl") as ?discribeNL)

		FILTER(LANG(?discribeNL) = "nl")## not rijksakademie and stedelijkmuseumschiedam

	?aggregation a ore:Aggregation ;

		edm:aggregatedCHO ?heritageObject ;#setting 1 for mauritshuis

		edm:isShownBy ?isShownBy ; #setting 1 for mauritshuis

		edm:rights ?rights .#setting 1

		OPTIONAL { ?aggregation edm:isShownAt ?isShownAt }#setting 2 for mauritshuis

		OPTIONAL { ?aggregation dcterms:format ?img }#setting 2 for mauritshuis


}



CONSTRUCT {

  ?creator

	rdf:type schema:Person;

	schema:creator ?creator;

	schema:name ?personNL .
}

WHERE {

    ?heritageObject a edm:ProvidedCHO ;

		dcterms:creators ?creator ;

		dc:description ?discription ;

		dc:creator ?person .

		BIND(STRLANG(str(?person), "nl") as ?personNL)

		BIND(STRLANG(?discription, "nl") as ?discribeNL)

		FILTER(LANG(?discribeNL) = "nl")


}



#### catharijneconvent:

CONSTRUCT {

  ?heritageObject

        rdf:type schema:VisualArtwork ;

		schema:artform ?artform;

		schema:name ?titleNL ;

		schema:publisher <https://www.catharijneconvent.nl/> ;

		schema:creator ?creator;

  		schema:temporal ?created ;

		schema:dateCreated ?yearCreated;

		schema:mainEntityOfPage ?isShownAt;

		schema:isBasedOn ?heritageObject ;

		schema:temporalCoverage ?temporalCoverage ;

    	schema:image ?image.

  ?image rdf:type schema:ImageObject ;

  		schema:isShownBy ?isShownBy;

  	    schema:encodingFormat ?img ;

		schema:license ?rights.

}

WHERE {

    ?heritageObject a edm:ProvidedCHO ;

		dcterms:artform ?artform;

		dc:title ?title ;

		dcterms:creators ?creator ;

  		dcterms:created ?created ;

		dcterms:dateCreated ?yearCreated ;

		edm:temporalCoverage ?temporalCoverage ;

		edm:image ?image.

		bind(strlang(str(?title), "nl") as ?titleNL)

	?aggregation a ore:Aggregation ;

		edm:aggregatedCHO ?heritageObject .#setting 1 for mauritshuis

		OPTIONAL { ?aggregation edm:isShownAt ?isShownAt }#setting 2 for mauritshuis

		OPTIONAL { ?aggregation dcterms:format ?img }#setting 2 for mauritshuis

		OPTIONAL { ?aggregation edm:rights ?rights }#setting 2 for mauritshuis

		OPTIONAL { ?aggregation edm:isShownBy ?isShownBy }#setting 2 for mauritshuis
}


CONSTRUCT {

  ?creator

	rdf:type schema:Person;

	schema:creator ?creator;

	schema:name ?personNL .

}

WHERE {

    ?heritageObject a edm:ProvidedCHO ;

		dcterms:creators ?creator ;

		dc:creator ?person .

		BIND(STRLANG(str(?person), "nl") as ?personNL)

}

rights and issShowBy is not avaliable in the all records.

right is optional

description is optional

#### `Title is description?`

#### moderne-kunst-museum-deventer:
<http://www.geertgrootehuis.nl/museum-deventer>
No date and artperiod 

#### museumdefundatie
This dateset is restricted based on requirements.

we used Date instead of created:

`changed dcterms:created to dc:date ?created;`

#### rijksakademie:

It has different format for date:

I am working on this









