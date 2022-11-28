# read RCE 

This folder consists of 4 files that must be run in order.
1-read_rce.py allows to read the big XML/RDF files and divided them into 152 files or chunks

2-merge_chunk_ttl allows you to merge files into one file and store it in the restore and then, you can test SPARQL queries and activate query-store.

3-query_kerken allows extracting Kerken from storage in an excel file for reconciliation

4-query_spatial allows to extract of all spatial objects from storage in an excel file for reconciliation


## Requirements

Install required libraries using following command before running script. pip install -r requirements.txt

### folders or file:
a XML/RDF file

## Usage

Find your python path on your system :

python = "C:\Program Files\Python37\python.exe"

#### Run:

`python 1-read_rce.py`



### Files after running script:


1- 152 N3 files in invalidperfixes folder

2- two excel file for reconciliation (kerk en sptail)





