# submissions-biostudies-api
This is a small Python web app to retrieve flat file information from the BioStudies API. 
It replaces the ArrayExpress "peach API" to deliver the status of all array designs (ADFs) in the ArrayExpress collection. 

The endpoint `/arrays` shows a list of all array designs in the ArrayExpress collection retrieved via the BioStudies API. 

Call to the endpoint `/update_arrays` refreshes the list to the latest status. This can be set up as a cronjob to update nightly. 
