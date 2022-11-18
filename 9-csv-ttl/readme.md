# csv-ttl (test version)

This script allows you to transform CSV dataset from open refine to turtle.
Creator is optional in this code, you can ignore warning message in the first step.

##### Requirements

Install required libraries using following command before running script. pip install -r requirements.txt

##### a folder is required as inputs:
1- Add all files in a csv folder.
`Please Note that the name of files must be stable and consistent.`

## Usage

### 1- Run script

Find your python path on your system :

python = "C:\Program Files\Python37\python.exe"

`python csv-triple_final.py`

### 2- Folders after running script:

1- clean-csv

2- enrich-step1

Folders number 2 will be used for the next steps (step 4 need new file???).

The rest of folder/folders are only for control.