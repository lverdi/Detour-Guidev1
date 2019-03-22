from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

from googleplaces import GooglePlaces, types, lang

API_KEY = "AIzaSyB4UtBsSLm1kkkmYh7zONJ3iv6_4a2j0Og"

google_places = GooglePlaces(API_KEY)


project_name = "DeTour Guide"
net_id = "Josh Even (jre83), Josh Sones (js2572), Adomas Hassan (ah667), Jesse Salazar (js2928), Luis Verde (lev27)"

@irsystem.route('/', methods=['GET'])
def search():
	# query = request.args.get('search')
	# if not query:
	# 	data = []
	# 	output_message = ''
	# else:
	# 	output_message = "Your search: " + query
	# 	data = range(5)
	query_result = google_places.nearby_search(
    location='London', keyword='Restaurants',
    radius=1000, types=[types.TYPE_RESTAURANT])
	# If types param contains only 1 item the request to Google Places API
	# will be send as type param to fullfil:
	# http://googlegeodevelopers.blogspot.com.au/2016/02/changes-and-quality-improvements-in_16.html

	if query_result.has_attributions:
		print(query_result.html_attributions)

	output_message = "Result of query"
	data = [query_result.html_attributions]
	# for place in query_result.places:
	# 	# Returned places from a query are place summaries.
	# 	print(place.name)
	# 	print(place.geo_location)
	# 	print(place.place_id)

	# 	# The following method has to make a further API call.
	# 	place.get_details()
	# 	# Referencing any of the attributes below, prior to making a call to
	# 	# get_details() will raise a googleplaces.GooglePlacesAttributeError.
	# 	print(place.details) # A dict matching the JSON response from Google.
	# 	print(place.local_phone_number)
	# 	print(place.international_phone_number)
	# 	print(place.website)
	# 	print(place.url)

	# 	# Getting place photos

	# 	for photo in place.photos:
	# 	    # 'maxheight' or 'maxwidth' is required
	# 	    photo.get(maxheight=500, maxwidth=500)
	# 	    # MIME-type, e.g. 'image/jpeg'
	# 	    photo.mimetype
	# 	    # Image URL
	# 	    photo.url
	# 	    # Original filename (optional)
	# 	    photo.filename
	# 	    # Raw image data
	# 	    photo.data


	# # Are there any additional pages of results?
	# if query_result.has_next_page_token:
	#     query_result_next_page = google_places.nearby_search(
	#             pagetoken=query_result.next_page_token)


	# # Adding and deleting a place
	# try:
	#     added_place = google_places.add_place(name='Mom and Pop local store',
	#             lat_lng={'lat': 51.501984, 'lng': -0.141792},
	#             accuracy=100,
	#             types=types.TYPE_HOME_GOODS_STORE,
	#             language=lang.ENGLISH_GREAT_BRITAIN)
	#     print added_place.place_id # The Google Places identifier - Important!
	#     print added_place.id

	#     # Delete the place that you've just added.
	#     google_places.delete_place(added_place.place_id)
	# except GooglePlacesError as error_detail:
	#     # You've passed in parameter values that the Places API doesn't like..
	#     print error_detail
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)



