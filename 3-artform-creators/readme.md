# Enrich step one and extract creators
This script allows you to enrich converted data in step one (1-data-gathering)
and extract creators who have painting artwork. Indeed, exclude painting visual work from other art work.

Requirements

Install required libraries using following command before running script. pip install -r requirements.txt

##### Two folders are required as inputs:
1- Add converted folder from first step(1-data-gathering).

2- Add the results of artType from openRefine inside of `type` folder.


`Please Note that the name of files inside of two folders must be the same.
Indeed, the name of file in the type folder must be the same as converted folder `

## Usage

### 1- Run script

Find your python path on your system :

python = "C:\Program Files\Python37\python.exe"

`python art-form-creators.py`

### 2- required Folders

1- type: result of open refine and the name of file = the name of file in converted. NO additional prefixes.

2-converted




### 3- Folders after running script:

1- csvartform

2- csv-final

3-artformtriple

4- enrich-step1

5- creators

Folders 4 and 5 will be used for the next steps.

The rest of folders are only for control and creating folders for the next steps.



