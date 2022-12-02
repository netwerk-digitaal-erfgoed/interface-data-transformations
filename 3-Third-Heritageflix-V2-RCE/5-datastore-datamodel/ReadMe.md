# Change data model

The python script and SPARQL queries allow you to change perfixes and namespaces match with the new data model.

## Requirements

Install required libraries using following command before running script. pip install -r requirements.txt

##### One folder is required as inputs:

enrich-data-for-datamodel

## Usage

### Run script

Find your python path on your system :

python = "C:\Program Files\Python37\python.exe"

`python datamodel.py`

### Folders after running script:

One folder(outputs-for-uploads) consists of Organizations file and datastore

Please note that the data store is created in this phase again and we use for cardinality check.

## github data model

https://github.com/netwerk-digitaal-erfgoed/interface-usable-visible/blob/main/heritageflix/backend/v2/transformations.md

https://github.com/netwerk-digitaal-erfgoed/interface-usable-visible/blob/main/heritageflix/frontend/v2/datamodel.md