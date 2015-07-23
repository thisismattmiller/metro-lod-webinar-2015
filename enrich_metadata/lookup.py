
#we are going to use the csv module which is built in
import csv
#the requests module, which needs to be installed (http://docs.python-requests.org/)
import requests
#the rdflib module that needs to be installed (https://rdflib.readthedocs.org/en/latest/)
import rdflib


#Open up the data.csv and loop through it
with open('data.csv', 'r') as csvfile:

	#parse the file
	lines = csv.reader(csvfile)
	for a_line in lines:

		#each row has two columns which are now an array, lets store the name and the NAF id into variables
		person_name = a_line[0]
		person_naf_id = a_line[1]

		print ('Looking up: ' + person_name)

		#we know if we have the NAF id we can ask VIAF to translate to the viaf URI
		#it will be in the format http://www.viaf.org/viaf/lccn/n79058586
		#viaf will tell us the viaf address but we don't want to follow it, that is why allow_redirects = False
		naf_to_viaf_url = 'http://www.viaf.org/viaf/lccn/' + person_naf_id		

		r = requests.get(naf_to_viaf_url, allow_redirects=False)

		#all the headers for the request are sent back, so it said "you should look here instead" and that is in the location value
		print ('The VIAF URI for this person is ' +  r.headers['location'])

		#we can now ask VIAF for the wikidata URI for this person.
		just_links_url = r.headers['location'] + "/justlinks.json"

		#so it looks something like http://viaf.org/viaf/34461945/justlinks.json

		r = requests.get(just_links_url)

		# { 
		#	"viafID":"34461945",
		#	"LC":["n79058586"],
		#	"WKP":["Q290536"],
		# }

		#this is a JSON response, so we can ask request to turn it into a python dictonary
		links = r.json()


		#does it have WKP link?
		if ('WKP' in links):
			#if so it is the first link (since they are stored as an list)
			wkidata_id = links['WKP'][0] 

			wiki_data_uri = 'http://www.wikidata.org/entity/' + wkidata_id

			print ("The wikidata uri is: " + wiki_data_uri)

			#lets use RDF lib to loop through this RDF data

			g = rdflib.Graph()
			result = g.parse(wiki_data_uri)

			for subj, pred, obj in g:


				#if this predicate is talking about the description of this person lets print it out
				if (pred == rdflib.term.URIRef('http://schema.org/description')):

					#and we are talking about our person (there is other data about other entites in the response too)
					if (subj == rdflib.term.URIRef(wiki_data_uri)):

						# and we only want engligh descriptions right now
						if (obj.language == 'en'):
							print (obj)




		#some new lines to space it out on the screen for each loop
		print ("\n\n\n\n")








