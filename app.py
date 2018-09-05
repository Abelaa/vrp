from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
from vrp import DataProblem, JSONConverter, CreateDistanceEvaluator
from gmaps import DistanceMatrix

class VRPService:

	def __init__(self, input):

		if input and 'origin' in input and 'locations' in input and 'maximum_distance' in input and 'number_of_vehicles' in input:

			ordered_locations = []
			ordered_locations.append(input['origin'])
			for location in input["locations"]:
				ordered_locations.append(location)

			self.response = self.json_response(
				ordered_locations,
				input["maximum_distance"],
				input["number_of_vehicles"],
				len(ordered_locations)
			)

		else:

			self.response = {
				"status" : "INCORRECT_INPUT",
				"message" : "The input parameters are invalid"	
			}

	def get_response(self):

		return self.response

	def json_response(self, locations, max_distance, n_vehicles, n_locations):

		# Instantiate DistanceMatrix
		raw_json_data = {}

		status, result = DistanceMatrix(
			locations, 
			locations.copy()
		).get_matrix()

		if status != 'OK':
			return result

		distance_matrix = result

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
