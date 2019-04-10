from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

import googlemaps 

project_name = "De-Tour Guide"
net_id = "Josh Even (jre83), Josh Sones (js2572), Adomas Hassan (ah667), Jesse Salazar (js2928), Luis Verdi (lev27)"
API_KEY = "AIzaSyB4UtBsSLm1kkkmYh7zONJ3iv6_4a2j0Og"
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
	if not (origin and destination):
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + origin + " to " + destination
		data = getLatLong(origin, destination)

	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)



