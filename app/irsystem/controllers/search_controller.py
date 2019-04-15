from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import os
from app.irsystem import ranked_results as rr

from googleplaces import types
import googlemaps

import pickle

project_name = "De-Tour Guide"
net_id = "Josh Even (jre83), Josh Sones (js2572), Adomas Hassan (ah667), Jesse Salazar (js2928), Luis Verdi (lev27)"
API_KEY = os.environ["GOOGLE_KEY"]
client = googlemaps.Client(API_KEY)

def getLatLong(origin, destination):
	origin_gc = client.geocode(origin)[0]['geometry']['location']
	origin_coords = (origin_gc['lat'], origin_gc['lng'])
	dest_gc = client.geocode(destination)[0]['geometry']['location']
	dest_coords = (dest_gc['lat'], dest_gc['lng'])
	return [origin_coords, dest_coords]

@irsystem.route('/', methods=['GET'])
def search():
	origin = request.args.get('origin')
	destination = request.args.get('dest')
	print(origin, destination)
	
	# TODO:
	# queries = request.arges.get('queries')
	queries = ["family friendly museum"]
	
	if not (origin and destination):
		print("HERE")
		data = []
		output_message = ''
		results = []
	else:
		output_message = "Your search: " + origin + " to " + destination
		data = getLatLong(origin, destination)
		# this is where the results get populated in
		print("getting results")
		with open("./app/irsystem/pickled_data","rb") as f:
			inv_idx_reviews,idf_reviews,doc_norms_reviews,inv_idx_types,idf_types,doc_norms_types, review_to_places, places_to_details = pickle.load(f)
		
		waypoints = rr.generateWaypoints(origin, destination)
		print(waypoints)
		results = []
		
		for query in queries:
			index_search_rst_reviews = rr.index_search(query, inv_idx_reviews, idf_reviews, doc_norms_reviews)
			index_search_rst_types = rr.index_search(query, inv_idx_types, idf_types, doc_norms_types)
			ranked_rst = rr.computeScores(waypoints, index_search_rst_reviews, index_search_rst_types, review_to_places, places_to_details)
			results = ranked_rst[:10]
	
	print(results)

	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data, results=results, api_key=API_KEY)



