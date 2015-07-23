# !/usr/local/bin/python2.7

#the rdflib module that needs to be installed (https://rdflib.readthedocs.org/en/latest/)
import rdflib

#we make a new graph to put our data into
g = rdflib.Graph()

#ask the library to parse the URI and its data
result = g.parse('http://www.dbpedia.org/resource/Ella_Fitzgerald')

#lets loop through it
for subj, pred, obj in g:

	#check if this is the right predicate
	if (pred == rdflib.term.URIRef('http://www.dbpedia.org/property/placeOfBirth')):
		
		print ("Was born in: " + obj)

