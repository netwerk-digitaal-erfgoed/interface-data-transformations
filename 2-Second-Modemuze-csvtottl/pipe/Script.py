# import 1-csv-triple-final as step1

import csvTtl as step1
import enrich
import model
import cardinality
import validation


step1.startProcessing()
enrich.startProcessing()
model.startProcessing()
cardinality.startProcessingDataGraph()
validation.startProcessingDataGraph()



