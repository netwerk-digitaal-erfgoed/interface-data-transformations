# Change data model

The python script and SPARQL queries allow you to change perfixes and namespaces match with your data model.


Requirements

Install required libraries using following command before running script. pip install -r requirements.txt

##### one folder is required as inputs:

1- Add enrich-data-for-datamodel

## Usage

### 1- Run script

Find your python path on your system :

python = "C:\Program Files\Python37\python.exe"

`python 12-datamodel.py`
or 
`python 13-datamodel-V1.py`

### 3- Folders after running script:

if you want to have final outputs in different folders run 12-mauritshuis-datamodel:

1- Organizations
2- artwork
3- artists
4- art-period

Please Note that we have 3 queries for five datasets for artists and artworks:
1- mauritshuis and vanabbemuseum (different dc:createddate) 
2- museumdefundatie and rijksakademie (different dc:date)
3- museumbelvedere (different dc:description)

if you want to have all objects in one file run 13-mauritshuis-datamodel-V1.py

1- outputs-for-uploads