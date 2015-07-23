#we are going to use the csv module which is built in
import csv
#the rdflib module that needs to be installed (https://rdflib.readthedocs.org/en/latest/)
import rdflib


#we are going to make a new graph to hold our data
g = rdflib.Graph()

#Open up the data.csv and loop through it
with open('names.csv', 'r') as csvfile:

	#parse the file
	lines = csv.reader(csvfile)
	for a_line in lines:

		#each row has 4 columns the database id, the person's name, their name tag and their image
		db_id = a_line[0]
		name = a_line[1]
		name_tag = a_line[2]
		image = a_line[3]

		#lets build the URI that we want to represent for each person, somthing like "http://linkedjazz.org/resource/Winnie_Brown"
		uri = "http://linkedjazz.org/resource/" + name_tag

		#and the complete url to the image
		image_url = "https://linkedjazz.org/image/square/" + image

		#everything needs to be a URI datatype or a Literal datatype to add it to our "graph", so lets convert everything
		uri = rdflib.URIRef(uri) 
		#using RDF Type predicate here
		rdf_type_predicate = rdflib.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
		
		#using FOAF person entity class
		foaf_person_class = rdflib.URIRef("http://xmlns.com/foaf/0.1/Person")
		
		#the FOAF name predicate
		foaf_name_predicate = rdflib.URIRef("http://xmlns.com/foaf/0.1/name")

		#the FOAF depection predicate
		foaf_depection_predicate = rdflib.URIRef("http://xmlns.com/foaf/0.1/depiction")

		#and the image, which is not a URI but a literal, because it is a document,
		image_url = rdflib.Literal(image_url)

		#and their name, which is another literal
		name = rdflib.Literal(name)
		

		#Now lets build each triple and add it to the graph 
		#this is a FOAF person
		g.add( ( uri , rdf_type_predicate , foaf_person_class  )  )

		#this is their name
		g.add( ( uri , foaf_name_predicate , name  )  )

		#and this is their image
		g.add( ( uri , foaf_depection_predicate , image_url  )  )



#lets write it all out
#format it into n-triple sieralization 
g = g.serialize(format='nt')

outfile = open('jazz_people.nt', 'w')
outfile.write(g)
outfile.close()




