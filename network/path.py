import sys
sys.path.insert(0, 'C:/Users/micha/OneDrive/Documents/AI_MSc/coursework/python_cw2_mdh323')
import pprint
from network.graph import NeighbourGraphBuilder
from tube.map import TubeMap

# Functions to help with the Djikstra algorithm

def get_unvisited_neighbours(neighbour_dict, id_to_check, unvisited_nodes):
    """ Return a list of neighbour station IDs not yet fully visited. """
    neighbours = neighbour_dict[id_to_check].copy()
    for key in list(neighbours.keys()):
        if key not in unvisited_nodes:
            del neighbours[key]
    return neighbours


def get_quickest_connection(connections):
    """ Return the quickest connection from a list of connection objects."""
    return min(connections, key = lambda connection:connection.time)


def first_common_elements(list1, list2):
    """ For each item in list 1, return its first instance in list 2."""
    return [element for element in list1 if element in list2][0]
  

class PathFinder:
    def __init__(self, tubemap):
        """
        Args:
            tubemap (TubeMap) : The TubeMap to use.
        """
        self.tubemap = tubemap

        graph_builder = NeighbourGraphBuilder()
        self.graph = graph_builder.build(self.tubemap)

        
    def get_shortest_path(self, start_station_name, end_station_name):
        """ Find ONE shortest path from start_station_name to end_station_name.
        
        The shortest path is the path that takes the least amount of time.

        Args:
            start_station_name (str): name of the starting station
            end_station_name (str): name of the ending station

        Returns:
            list[Station] : list of Station objects corresponding to ONE 
                shortest path from start_station_name to end_station_name.
                Returns None if start_station_name or end_station_name does not 
                exist.
                Returns a list with one Station object (the station itself) if 
                start_station_name and end_station_name are the same.
        """
        
        # Catch unwanted cases first
        station_name_list = [station.name for station in self.tubemap.stations.values()]
        if start_station_name not in station_name_list:
            return None
        elif end_station_name not in station_name_list:
            return None
            
            
        # Initialise objects for Djikstra's search algorithm
        
        ## A dictionary to retrieve a station's ID from its name
        station_name_to_id = {station.name:station.id for station in self.tubemap.stations.values()}
        start_station_id = station_name_to_id[start_station_name]
        end_station_id = station_name_to_id[end_station_name]
        
        ## A dictionary of all unvisited stations
        unvisited_stations = {station.id:station.name for station in self.tubemap.stations.values()}
        
        ## A dictionary of estimated times for all stations, initalising at infinity
        estimated_times = {station.id:float('inf') for station in self.tubemap.stations.values()}
        
        ## A list to store the nodes that Djikstra's algorithm works through
        route_so_far = list()
        
        ## Set the time to the start to be zero and remove start from univisited nodes
        estimated_times[start_station_id] = 0
        current_node = start_station_id
        route_so_far.append(start_station_id)
        
        # Run the algorithm until we reach the end node
        # This follows the pseudocode outlined here: 
        # https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Algorithm
        while current_node != end_station_id: 
            neighbours = get_unvisited_neighbours(self.graph, current_node, unvisited_stations)

            for neighbour_key in list(neighbours.keys()):
                quickest_connection = get_quickest_connection(neighbours[neighbour_key])
                time_to_check = quickest_connection.time + estimated_times[current_node]
                if time_to_check < estimated_times[neighbour_key]:
                    estimated_times[neighbour_key] = time_to_check

            del unvisited_stations[current_node]

            destination_not_reached = end_station_id in unvisited_stations

            if destination_not_reached:
                remaining_node_times = {key: estimated_times[key] for key in unvisited_stations}
                new_node = min(remaining_node_times, key = remaining_node_times.get)
                route_so_far.append(new_node)
                current_node = new_node
        
        # Trace back our route
        route_taken = list()

        while route_so_far[-1] != start_station_id:
            last_node = route_so_far[-1]
            route_taken.append(last_node)
            neighbours = list(self.graph[last_node].keys())
            previous_station_id = first_common_elements(route_so_far, neighbours)
            previous_station_index = route_so_far.index(previous_station_id)
            route_so_far = route_so_far[:previous_station_index + 1]

        route_taken.append(start_station_id)
        route_taken = route_taken[::-1]

        route_taken = [self.tubemap.stations[station_id] for station_id in route_taken]
        
        return route_taken


def test_shortest_path():
    from tube.map import TubeMap
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")
    
    path_finder = PathFinder(tubemap)
    stations = path_finder.get_shortest_path("Covent Garden", "Green Park")
    print(stations)
    
    station_names = [station.name for station in stations]
    expected = ["Covent Garden", "Leicester Square", "Piccadilly Circus", 
                "Green Park"]
    assert station_names == expected


if __name__ == "__main__":
    test_shortest_path()
