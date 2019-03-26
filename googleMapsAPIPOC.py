#!/usr/bin/env python

import googlemaps 
import gmaps
import csv
import pickle 


from datetime import datetime
from googleplaces import GooglePlaces, types, lang
from math import sin, cos, sqrt, atan2, radians


result_count = 0

def computeDistanceLatLong(lat1, lon1, lat2, lon2):
	"""
	Computes distance between two locations using lat long 

	"""
	# approximate radius of earth in km
	R = 6373.0

	lat1 = radians(lat1)
	lon1 = radians(lon1)
	lat2 = radians(lat2)
	lon2 = radians(lon2)

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	distance = R * c

	return distance

######## 1 BEGINNING GENERATING NEARBY LOCATIONS ##############
def getNearbySearchDetails(location, waypoint, radius, types=None, keyword=None, rankby='prominence'):
	"""
	Generates details of places nearby your location


	Args:
        location -- A human readable location, e.g 'London, England' (default None)
        waypoing -- tuple containing lat long of the waypoint used for nearby search
		keyword  -- A term to be matched against all available fields, including
	                   but not limited to name, type, and address (default None)
	    radius   -- The radius (in meters) around the location/lat_lng to restrict
                    the search to. The maximum is 50000 meters (default 3200)
        types     -- An optional type(s) used for restricting the results to Places (default None)
        			can be a list (check 'import types' for information on types)
        rankby   -- Specifies the order in which results are listed:
                    'prominence' (default) or 'distance' (imply no radius argument)


	"""
	global result_count


	API_KEY = "AIzaSyB4UtBsSLm1kkkmYh7zONJ3iv6_4a2j0Og"

	google_places = GooglePlaces(API_KEY)

	# Radius is in meters
	
	# rankby   -- Specifies the order in which results are listed:
	#                    'prominence' (default) or 'distance' (imply no radius argument)
	query_result = google_places.nearby_search(
		    location=location, keyword=keyword,
		    radius=radius, types=types)

	# If types param contains only 1 item the request to Google Places API
	# will be send as type param to fullfil:
	# http://googlegeodevelopers.blogspot.com.au/2016/02/changes-and-quality-improvements-in_16.html

	if query_result.has_attributions:
		print(query_result.html_attributions)
	
	# Array of dictionaries for writing to csv
	rst = []

	for place in query_result.places:
		d = {}
		result_count+=1
	# 	# Returned places from a query are place summaries.
		print("**************")
		print("Place name: ", place.name)
		
		d["name"] = place.name

		geo_loc = place.geo_location

		# Computes distance to waypoints
		d["distance"] = computeDistanceLatLong(waypoint[0], waypoint[1], 
												float(geo_loc['lat']), float(geo_loc['lng']))
	# 	print(place.geo_location)
	# 	print(place.place_id)

	# 	# The following method has to make a further API call.
		place.get_details()
	# 	# Referencing any of the attributes below, prior to making a call to
	# 	# get_details() will raise a googleplaces.GooglePlacesAttributeError.
		#print("Place details: ", place.details) # A dict matching the JSON response from Google.
		
		curr_reviews = []
		print("Place types: " , place.types)
		d["types"] = place.types
		try: 
			print("Place rating: ", place.rating)
			d["rating"] = float(place.rating)
		except: 
			print("No ratings found for: ", place.name)
			d["rating"] = None

		try:
			print("Place reviews: ", place.details["reviews"])
			for review in place.details["reviews"]:
				print("Author name: ", review["author_name"])
				print("Relative Time Description: ", review["relative_time_description"])
				print("Text: ", review["text"])
				print("Reviewer Rating: ", review["rating"])
				print("--------")
				curr_reviews.append({"author_name" : review["author_name"], 
									"relative_time_description" : review["relative_time_description"],
									"rating" : review["rating"], "text" : review["text"]})
			d["reviews"] = curr_reviews

		except:
			print("No reviews found for: ", place.name)	
			d["reviews"] = []

		rst.append(d)


	#  Most of the time twenty is plenty, but for restaurants, for example it may not be
	# # Are there any additional pages of results?
	# if query_result.has_next_page_token:
	#     query_result = google_places.nearby_search(
	#             pagetoken=query_result.next_page_token)

	# else:
	# 	print("Breaking")
	# 	break

	# 	print(place.local_phone_number)
	# 	print(place.international_phone_number)
	# 	print(place.website)
	# 	print(place.url)

	# 	# Getting place photos -- We can embed these values into our HTML page if we use our 
		# Template!

		# for photo in place.photos: 
		#     # 'maxheight' or 'maxwidth' is required
		#     photo.get(maxheight=500, maxwidth=500)
		#     # MIME-type, e.g. 'image/jpeg'
		#     photo.mimetype
		#     # Image URL
		#     photo.url
		#     # Original filename (optional)
		#     photo.filename
		#     # Raw image data
		#     photo.data


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

	return rst


######## 1 END GENERATING NEARBY LOCATIONS ##############

######## 4 BEGINNING GENERATING DIRECTIONS ##############
def generateSearchResults(start_addr, end_addr, filename ,
						  keyword=None, radius=10000, 
						  types=None, rankby='prominence'):
	"""
	Generates nearby search results every 30 miles along a given route
	
	Returns an array of dictionaries and writes them to a csv
	Args:
		start_addr -- start address of trip
		end_addr   -- end address of trip
		filename   -- Name of the file to write to
		keyword  -- A term to be matched against all available fields, including
	                   but not limited to name, type, and address (default None)
	    radius   -- The radius (in meters) around the location/lat_lng to restrict
                    the search to. The maximum is 50000 meters (default 3200)
        types     -- An optional type(s) used for restricting the results to Places (default None)
        			can be a list (check 'import types' for information on types)
        rankby   -- Specifies the order in which results are listed:
                    'prominence' (default) or 'distance' (imply no radius argument)
	

	"""
	global result_count


	rst = []
	
	gmap = googlemaps.Client(key="AIzaSyB4UtBsSLm1kkkmYh7zONJ3iv6_4a2j0Og")

	# Request directions via public transit
	now = datetime.now()

	# The locations can be written out or geocoded
	# mode = "driving", "walking", "bicycling", "transit"
	# departure_time -- int or date.datetime
	directions_result = gmap.directions(start_addr,
	                                     end_addr,
	                                     mode="driving",
	                                     departure_time=now)
	
	# Way to lookup waypoints for later usage
	waypoint_dict = directions_result[0]["legs"][0]["steps"]

	total_distance = 0 # total distance in meters
	total_duration = 0 # total duration in seconds

	prev_distance = 0

	waypoints = [] # tuples of (lat, lng)
	polylines = [] # Array of polylines -- can be used for display if we like

	# TODO: Should try to include the start and end locations every time we perform a nearby_search
	#		So while checking total_distance - prev_distance we also should just automatically add the first 
	# 		and last waypoint
	for entry in waypoint_dict:
		total_distance += entry["distance"]["value"]
		total_duration += entry["duration"]["value"]

		# Only include waypoints every 20-30 miles
		# TODO: the number of waypoints should be constant and should be based on overall
		#		trip distance
		if total_distance - prev_distance > 10000: 
			lat = entry["start_location"]["lat"]
			lng = entry["start_location"]["lng"]
			waypoints.append((lat, lng))
			prev_distance = total_distance
			reverse_geocode_result = gmap.reverse_geocode((lat, lng))
			location = reverse_geocode_result[0]["formatted_address"]


			# TODO: INCLUDE ARGUMENT THAT TAKES WAYPOINT LAT LNG AND COMPUTES DISTANCE FROM
			# 		THAT WAYPOINT TO THE PATH
			rst = rst + getNearbySearchDetails(location, (lat,lng), radius, types, keyword, rankby)
		
		polylines.append(entry["polyline"]["points"])

	print("Number of waypoints: ", waypoints)	
	print("There are {} results".format(result_count))


	# If you wanna save results dump em in a pickle
	# with open('gapiPathPickle', 'wb') as f:
	# 	pickle.dump(rst, f )

	# with open(filename,'w') as f:
	# 	dw = csv.DictWriter(f,rst[0].keys())
	# 	dw.writeheader()
	# 	dw.writerows(rst)
	# return rst


if __name__ == '__main__':
	
	start_addr = "Jackson, NJ"
	end_addr   = "17 Wakefield Court, Shrewsbury NJ"

	# Uncomment this to run the file
	# generateSearchResults(start_addr, end_addr, "pathData.csv", keyword="adventure")