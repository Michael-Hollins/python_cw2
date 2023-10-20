# Script containing all the helper functions for the data import to construct TubeMap
import sys
sys.path.insert(0, 'C:/Users/micha/OneDrive/Documents/AI_MSc/coursework/python_cw2_mdh323')

import json
import pprint
from tube.components import *
import math

def read_raw_json(filename):
	""" Loads in the raw json data to a dict, defaults to the london.json file."""
	with open(filename) as jsonfile:
		data = json.load(jsonfile)
	return data

def zone_set(zone_string):
	""" Takes a number and returns a set of zones it rounds to.
	
	We convert the string input to a float. If it's an integer we 
	simply return a singleton set of the integer. If it's a float,
	we return the set of integers that bound the float. For example,
	2.5 will return {2, 3}. 
	
	Arguments:
		number_string (str): Must be able to be converted to a floor
	Output:
		(set): A set of integers that bound the zone we input.
	
	"""
	# Check our input is valid so we only have a single number to consider.
	if not isinstance(zone_string, str):
		return TypeError("Argument must be a string.")
	
	# Check we can convert from string to float.
	try:
		zone_float = float(zone_string)
	except:
		return TypeError("Please use an appropriate input, e.g. '2.5'")
	
	# Return a set of integers, either just a singleton or two. 
	if zone_float.is_integer():
		zone_set = {int(zone_float)}
		return zone_set	 
	elif isinstance(zone_float, float):
		lower_zone = int(math.floor(zone_float))
		upper_zone = int(math.ceil(zone_float))
		zone_set = {lower_zone, upper_zone}
		return zone_set
	else:
		return None


def get_stations(data):
	""" Returns a dictionary that indexes Station instances by their id, (key=id (str), value=Station) 

	Note that we have to parse the zones correctly into a set of ints using our zone_set() function.
	
	Arguments:
		data (dict): A dictionary containing a "stations" key from our json file.
	Output:
		(dict) : a dictionary that indexes Station instances by their id(key=id (str), value=Station).
		This will help form an attribute of TubeMap. 
	"""
	stations = dict()

	for sub_dictionary in data["stations"]:
		# Coerce our inputs into the correct data types for the Station class
		id_string = str(sub_dictionary["id"])
		name_string = str(sub_dictionary["name"])
		zone = zone_set(sub_dictionary["zone"])
		
		# Add each station instance to a stations dictionary
		stations[id_string] = Station(id_string, name_string, zone)
	
	return stations
	
	
def get_trainlines(data):
	""" A dictionary that indexes Line instances by their id (key=id (str), value=Station) 
	
	Arguments:
		data (dict): A dictionary containing a "lines" key from our json file.
	Output:
		(dict): indexes lines by their ID. Will be used to form an attribute of TubeMap.
	"""
	lines = dict()

	for sub_dictionary in data["lines"]:
		# Coerce our inputs into the correct data types
		id_string = str(sub_dictionary["line"])
		name_string = str(sub_dictionary["name"])
	
		# Add each line instance to a lines dictionary
		lines[id_string] = Line(id_string, name_string)
	
	return lines


def get_connections(data, stations, lines):
	""" Returns a list of Connection instances from a dictionary.
	
	Note each item in the connections list of dictionaries will return station and line IDs.
	To get the values, we will need to load in the corresponding stations and lines dictionaries.
	We define these functions above.
	
	Arguments:
		data (dict): A dictionary containing a "connections" key from our json file.
	Output:
		(list): A list of Connection instances.
	"""
	# Load stations and lines dictionaries so we can get values from keys.
	
	# Initalise the list
	connections = list()
	
	# Create a list of Connection objects
	for item in data["connections"]:
		station1 = item['station1']
		station2 = item['station2']
		station_connection = {stations[station1], stations[station2]}
		
		line_id = item['line']
		line_connection = lines[line_id]
		
		time_connection = int(item['time'])
		
		connection = Connection(station_connection, line_connection, time_connection)
		connections.append(connection)
		
	return connections
