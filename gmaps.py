import googlemaps
import os
import urllib.request, json 

# fetches distance matrix from google and returns 2D array
# Input: list of all locations including origin
# both origin and destination locations have the same list of locations
# api_key: contains the google maps api key
class DistanceMatrix():

	def __init__(self, origin_locations, destination_locations):

		self.api_key = os.getenv('API_KEY', 'AIzaSyC02c5shSIY_kVIdXfCVZAZN6MJm5BJ2Ck')
		self.origin_locations = origin_locations
		self.destination_locations = destination_locations

	# returns: 2D matrix in json format
	def get_json_response(self):

		gmaps = googlemaps.Client(key=self.api_key)
		print("fetching matrix...")

		try:

			# fetch distance matrix for driving b/n given points in meter
			distance_matrix = gmaps.distance_matrix(
				mode='driving',
				units='metric',
				origins=self.origin_locations, 
				destinations=self.destination_locations
			)
			print(distance_matrix)
			print("done.")

		except googlemaps.exceptions.ApiError as err:

			reference_link = "http://developers.google.com/maps/documentation/distance-matrix/intro#StatusCodes"

			distance_matrix = {
				"status": '{}'.format(err),
				"error_message": 'Status Code Reference Link - {}'.format(reference_link)
			}

		return distance_matrix

	# takes the json response
	# returns: 2D matrix in the form of 2D array
	def get_matrix(self):

		json_data = self.get_json_response()

		if json_data['status'] == 'OK':

			rows = json_data['rows']
			num_rows = len(rows)
			num_cols = len(rows[0]['elements'])

			# initialize matrix with zeroes
			distance_matrix = [[0 for x in range(num_cols)] for y in range(num_rows)]

			for i in range(num_rows):
				for j in range(num_cols):
					data = json_data['rows'][i]['elements'][j]
					if data['status'] == 'NOT_FOUND':
						return ('NOT_OKAY', {
							"status": "INVALID_LOCATION_DATA",
							"message": "At least one of the locations doesn't have proper format"
						})
					distance_matrix[i][j] = data['distance']['value']
		
			return ('OK', distance_matrix)

		else:

			return ('NOT_OKAY', {
				"status": json_data['status'],
				"message": json_data['error_message']
			})
