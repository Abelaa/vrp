from flask import Flask, request, jsonify
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
from vrp import DataProblem, JSONConverter, CreateDistanceEvaluator
from gmaps import DistanceMatrix
import json

app = Flask(__name__)

@app.route('/api', methods=['POST'])
def api():

	input = request.json
	
	if input:

		ordered_locations = []
		ordered_locations.append(input['origin'])
		for location in input["locations"]:
			ordered_locations.append(location)

		return jsonify(json_response(
			ordered_locations,
			input["maximum_distance"],
			input["number_of_vehicles"],
			len(ordered_locations)
		))

	else:

		return jsonify({
			"status" : "INCORRECT_INPUT",
			"message" : "The input parameters are invalid"	
		})

def json_response(locations, max_distance, n_vehicles, n_locations):
	# Instantiate DistanceMatrix
	try:
		distance_matrix = DistanceMatrix(
			locations, 
			locations.copy()
		).get_matrix()
	# Exception thrown if googlemaps api is unable to fetch from google
	except:
		return {
			"status" : "CRITICAL_ERROR",
			"message" : "failed to get critical data" 
		}

    # Instantiate the data problem.
	data = DataProblem(distance_matrix, max_distance, n_vehicles, n_locations)

	# Create Routing Model
	routing = pywrapcp.RoutingModel(data.num_locations, data.num_vehicles, data.depot)

	# Define weight of each edge
	created_distance_evaluator = CreateDistanceEvaluator(data)
	distance_evaluator = created_distance_evaluator.distance_evaluator

	routing.SetArcCostEvaluatorOfAllVehicles(distance_evaluator)
	created_distance_evaluator.add_distance_dimension(routing, distance_evaluator, data)

	# Setting first solution heuristic (cheapest addition).
	search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
	search_parameters.first_solution_strategy = (
	    routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

	# Solve the problem.
	print("solving...")
	assignment = routing.SolveWithParameters(search_parameters)
	print("Done.")
	converter = JSONConverter(data, routing, assignment)
	json = converter.convert(distance_evaluator)

	return json

if __name__ == "__main__":

	# start the flask server
	app.run(debug=False)
