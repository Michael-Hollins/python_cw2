import sys
sys.path.insert(0, 'C:/Users/micha/OneDrive/Documents/AI_MSc/coursework/python_cw2_mdh323')
from tube.import_helper_functions import zone_set
from tube.map import TubeMap
from network.graph import NeighbourGraphBuilder

def test_zone_set_integers():  
	assert zone_set("4") == {4}
	assert zone_set("0") == {0}
	assert zone_set("-4") == {-4}
	
def test_zone_set_floats():
	assert zone_set("2.5") == {2, 3}
	for item in zone_set("0.3"):
		assert isinstance(item, int)
	assert isinstance(zone_set("3.5"), set)

def test_zone_invalids():
	assert isinstance(zone_set("Blah"), TypeError)
	assert isinstance(zone_set(""), TypeError)
	
test_zone_set_integers()
test_zone_set_floats()
test_zone_invalids()

def test_import():
	tubemap = TubeMap()
	tubemap.import_from_json("data/london.json")
	# view one example Station
	print(tubemap.stations[list(tubemap.stations)[0]])
	
	# view one example Line
	print(tubemap.lines[list(tubemap.lines)[0]])
	
	# view the first Connection
	print(tubemap.connections[0])
	
	# view stations for the first Connection
	print([station for station in tubemap.connections[0].stations])
	
	print("All tests passed for tubemap")
	
test_import()


def check_graph_pairs():
	# Checks that graph['110']['17'] == graph['17']['110'] etc.
	tubemap = TubeMap()
	tubemap.import_from_json("data/london.json")
	graph_builder = NeighbourGraphBuilder()
	graph = graph_builder.build(tubemap)
	
	for i in graph.keys():
		for j in graph[i].keys():
			assert graph[i][j] == graph[j][i]

check_graph_pairs()
	
def test_graph():
	from tube.map import TubeMap
	tubemap = TubeMap()
	tubemap.import_from_json("data/london.json")

	graph_builder = NeighbourGraphBuilder()
	graph = graph_builder.build(tubemap)

	print(graph)

test_graph()