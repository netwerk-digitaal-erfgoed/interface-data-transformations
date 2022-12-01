# Change SHACL SHAPE
The python script is for data validation using SHACL Core.

Requirements
Install required libraries using following command before running script. pip install -r requirements.txt

##### one folder is required as inputs:
1- Add your folder contains datasets
2- keep shape folder. It contains SHACL core for validation

## Usage
### 1- Run script
Find your python path on your system :
python = "C:\Program Files\Python37\python.exe"
`python validation-report.py`

### 3- Folders after running script:

One folder contains validation reports

## report on cardinality: check for maxcount

There is more than one object in the below paths:

###### Rijskacademie for schema:temporal and artist object.

###### maurithuis for schema:temporal and schema:createdDate and artist object
temoral and data created maurithuis (http://data.collectienederland.nl/resource/document/mauritshuis/198) and  (http://data.collectienederland.nl/resource/document/mauritshuis/621)
 artist maurithuis: the https://data.rkd.nl/artists/18572 has more than one Artist name.
###### Belvedere for schema:title 

example: http://data.collectienederland.nl/resource/document/museum-belvedere/0042 2 titles

###### de fundatie for schema:title, schema:description , and artist object
same like above examples


You can also test with the below SPARQL.

PREFIX schema: <http://schema.org/>

PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT * WHERE {
  
  ?sub <https://schema.org/name> ?obj .

   ?sub1 <https://schema.org/name> ?obj1 .
  
  filter (?sub = ?sub1 )

  filter (?obj != ?obj1 )

} 











