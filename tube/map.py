import sys
sys.path.insert(0, 'C:/Users/micha/OneDrive/Documents/AI_MSc/coursework/python_cw2_mdh323')

from tube.import_helper_functions import *

class TubeMap:
	"""
    The TubeMap class must contain these three member attributes:
	- stations: a dictionary that indexes Station instances by their id 
	  (key=id (str), value=Station)
	- lines: a dictionary that indexes Line instances by their id 
	  (key=id, value=Line)
	- connections: a list of Connection instances for the TubeMap 
	  (list of Connections)
	"""

	def __init__(self):
		self.stations = {}	# key: id (str), value: Station instance
		self.lines = {}	 # key: id (str), value: Line instance
		self.connections = []  # list of Connection instances
	

	def import_from_json(self, filepath):
		""" Import tube map information from a JSON file

		Args:
			filepath (str) : relative or absolute path to the JSON file 
				containing all the information about the tube map graph to 
				import. If filepath is invalid, no attribute should be updated, 
				and no error should be raised.

		Returns:
			None
		"""
		try:
			data = read_raw_json(filepath)
			self.stations = get_stations(data)
			self.lines = get_trainlines(data)
			self.connections = get_connections(data, self.stations, self.lines)
		except:
			pass