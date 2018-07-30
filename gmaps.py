#!/usr/bin/python3
import googlemaps

# fetch distance matrix from google and returns 2D matrix
# Input: list of all locations including origin
# api_key: contains the google maps api key
class DistanceMatrix():

	def __init__(self, origin_locations, destination_locations):

		self.api_key = 'AIzaSyC02c5shSIY_kVIdXfCVZAZN6MJm5BJ2Ck'
		self.origin_locations = origin_locations
		self.destination_locations = destination_locations

	# returns: 2D matrix in json format
	def get_json_response(self):

		gmaps = googlemaps.Client(key=self.api_key)
		print("fetching matrix...")

		distance_matrix = gmaps.distance_matrix(
			mode='driving',
			units='metric',
			origins=self.origin_locations, 
			destinations=self.destination_locations
			)
		print("done.")

		return distance_matrix

	# takes the json response
	# returns: 2D matrix in the form of 2D array
	def get_matrix(self):

		json_data = self.get_json_response()
		rows = json_data['rows']
		num_rows = len(rows)
		num_cols = len(rows[0]['elements'])
		distance_matrix = [[0 for x in range(num_cols)] for y in range(num_rows)]

		for i in range(num_rows):
			for j in range(num_cols):
				distance_matrix[i][j] = json_data['rows'][i]['elements'][j]['distance']['value']

		return distance_matrix
