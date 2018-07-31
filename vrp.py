# Vehicle Routing Problem
from __future__ import print_function
from six.moves import xrange
from gmaps import DistanceMatrix

###########################
# Problem Data Definition #
###########################

class DataProblem():
    """Stores the data for the problem"""
    def __init__(self, dist_matrix, max_distance, n_vehicles, n_locations):
        """Initializes the data for the problem"""
        self._distance_matrix = dist_matrix
        self._maximum_distance = max_distance
        self._num_vehicles = n_vehicles
        self._num_locations = n_locations
        self._depot = 0

    @property
    def maximum_distance(self):
        """Gets maximum distance"""
        return self._maximum_distance

    @property
    def distance_matrix(self):
        """Gets distance matrix"""
        return self._distance_matrix

    @property
    def num_vehicles(self):
        """Gets number of vehicles"""
        return self._num_vehicles

    @property
    def num_locations(self):
        """Gets number of locations"""
        return self._num_locations

    @property
    def depot(self):
        """Gets depot location index"""
        return self._depot

#######################
# Problem Constraints #
#######################

class CreateDistanceEvaluator(object): # pylint: disable=too-few-public-methods
    """Creates callback to return distance between points."""
    def __init__(self, data):
        """Initializes the distance matrix."""
        self.data = data

    def distance_evaluator(self, from_node, to_node):
        """Returns the manhattan distance between the two nodes"""
        return self.data.distance_matrix[from_node][to_node]

    def add_distance_dimension(self, routing, distance_evaluator, data):
        """Add Global Span constraint"""
        maximum_distance = data.maximum_distance
        distance = "Distance"
        routing.AddDimension(
            distance_evaluator,
            0, # null slack
            maximum_distance, # maximum distance per vehicle
            True, # start cumul to zero
            distance)
        distance_dimension = routing.GetDimensionOrDie(distance)
        # Try to minimize the max distance among vehicles.
        # /!\ It doesn't mean the standard deviation is minimized
        distance_dimension.SetGlobalSpanCostCoefficient(100)

##################
# conver to JSON #
##################
class JSONConverter():
    """Print solution to console"""
    def __init__(self, data, routing, assignment):
        """Initializes the printer"""
        self._data = data
        self._routing = routing
        self._assignment = assignment

    @property
    def data(self):
        """Gets problem data"""
        return self._data

    @property
    def routing(self):
        """Gets routing model"""
        return self._routing

    @property
    def assignment(self):
        """Gets routing model"""
        return self._assignment

    def convert(self, distance_evaluator):
        """converts the assignments to json format"""
        JSON_output = {}
        JSON_output['result'] = {}
        JSON_output['result']['routes'] = []

        try:
            total_dist = 0 # summation of each route distances, begin from 0
            for vehicle_id in xrange(self.data.num_vehicles):
                index = self.routing.Start(vehicle_id)

                JSON_output['result']['routes'].append({})
                JSON_output['result']['routes'][vehicle_id]['route'] = []

                route_dist = 0 # summation of each distances in a route
                while not self.routing.IsEnd(index):
                    node_index = self.routing.IndexToNode(index)
                    next_node_index = self.routing.IndexToNode(
                        self.assignment.Value(self.routing.NextVar(index)))
                    route_dist += distance_evaluator(
                        node_index,
                        next_node_index)

                    JSON_output['result']['routes'][vehicle_id]['route'].append(node_index)

                    index = self.assignment.Value(self.routing.NextVar(index))

                node_index = self.routing.IndexToNode(index)
                total_dist += route_dist

                JSON_output['result']['routes'][vehicle_id]['route'].append(node_index)
                JSON_output['result']['routes'][vehicle_id]['route_distance'] = route_dist

            JSON_output['result']['total_distance'] = total_dist
            JSON_output['status'] = 'OK'

        # exception thrown if no solution is found
        except:
            JSON_output = {}
            JSON_output['status'] = 'NOT_SOLVED'
            JSON_output['message'] = 'Try higher number of vehicles or increase maximum distance'

        return JSON_output
