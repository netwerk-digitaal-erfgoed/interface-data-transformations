## RCE pipeline

Under development

https://github.com/netwerk-digitaal-erfgoed/interface-usable-visible/blob/main/heritageflix/frontend/v2/datamodel.md

https://github.com/netwerk-digitaal-erfgoed/interface-usable-visible/blob/main/heritageflix/backend/v2/transformations.md

Last version of dataset:
https://data.netwerkdigitaalerfgoed.nl/MaryamSajjadian/checkedCardinalityRCE/graphs

duplications have been deleted except Bnodes.

Todo:

1- Invalid URIs

2- Create store for all steps

3- Add identifier ---> add to enrichment phase

BIND(STRAFTER(STR(?heritageObject), "http://data.collectienederland.nl/resource/document/rce-beeldbank/") AS ?id)

4- Repeat enrichment step 3(start with new datastore)
Start point: https://github.com/netwerk-digitaal-erfgoed/interface-data-transformations/tree/main/3-Third-Heritageflix-V2-RCE/3-merge-csv

5- Shape validation
