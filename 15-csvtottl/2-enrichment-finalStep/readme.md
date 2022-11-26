# Enrich final step
This script allows you to enrich datasets by adding creators and art periods.

Requirements

Install required libraries using following command before running script. pip install -r requirements.txt

##### Two folders are required as inputs:
1- Add creators folder result of open refine (creator folder).

2- Add the results of enrichment step one (enrich-step1 folder).

`Please Note that the name of files must be stable and consistent with files in the converted folder.
Only name of files can be changed.`

## Usage

### 1- Run script

Find your python path on your system :

python = "C:\Program Files\Python37\python.exe"

`python 1-enrich-step2.py`

If date is in dc:date into two seperate lines or have only dc:date, first, run 2-date-change.py and then run  1-enrich-step2.py


### 3- Folders after running script:

1- final-creator-triple

2- enrichment-step-2

3- enrich-data-for-datamodel

Folders number 3 will be used for the next steps.

The rest of folders are only for control and creating folders for the next steps.