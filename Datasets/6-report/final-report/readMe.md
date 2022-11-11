# Report

These files consist of four reports files:

### 1- Converted

Results of conversion RDF/XML to triples. Indeed, it reports on the number of untouched triples after conversion.

catharijneconvent-records,148630

mauritshuis-records,1712

museum-belvedere-records,3016

museum-de-fundatie-records,3450

van-abbe-museum-records,6314

rijksakademie-records,8232

stedelijk-museum-schiedam-records,6158

moderne-kunst-museum-deventer-records,2776

### 2- creators with painting work

catharijneconvent-records,968

mauritshuis-records,1643

moderne-kunst-museum-deventer-records,1674

museum-belvedere-records,2560

museum-de-fundatie-records,3126

rijksakademie-records,3225

stedelijk-museum-schiedam-records,3448

van-abbe-museum-records,3832

### 3- enrich-data-for-datamodel

After enrichment of dataset:

catharijneconvent,148638

mauritshuis,1720

museum-belvedere,3018

museum-de-fundatie,3458

van-abbe-museum,6317

rijksakademie,8240

stedelijk-museum-schiedam,6197

moderne-kunst-museum-deventer,2776


### 4- heritage-object files = artwork

after adding data model and executing cardinalities

5 datasets fullfilled cardinalities:

mauritshuis-records,126

museum-belvedere-records,572

museum-de-fundatie-records,35

van-abbe-museum-records,92

rijksakademie-records,95

##### catharijneconvent

rights and issShowBy is not avaliable in the all records.

##### stedelijk-museum-schiedam

description contains tags and not real words.

##### moderne-kunst-museum-deventer

No date and art period 


## rce-beeldbank dataset

It seems this dataset has 2 problems:

1-	The first problem happens during serializations to turtle. Here, you see the messages after serializations. We can have them only in N3 format.
https://monumentenregister.cultureelerfgoed.nl/monumenten/510882%20|%20510883%20|%20510884 does not look like a valid URI, I cannot serialize this as N3/Turtle. Perhaps you wanted to urlencode it?
https://monumentenregister.cultureelerfgoed.nl/monumenten/510882%20|%20510883%20|%20510884 does not look like a valid URI, trying to serialize this will break.
https://monumentenregister.cultureelerfgoed.nl/monumenten/5380%20|%205381 does not look like a valid URI, trying to serialize this will break.

2-	This dataset does not have dc:type and dc:title.However, I attached some part of it(please check your email),  I could not attach the complete xml file because zip file is enough large, and I also could not push it on Github.
It is also very large dataset. I can not uploaded.

## nationaal-archief-beeldbank

It  does not have dc:title. It is also very large dataset. I can not uploaded.








