def get_connection_ID_pairs(tubemap):
    """ Returns a list of ID pairs for each connection instance in tubemap.connections"""
    connection_ids = list()
    for i in range(len(tubemap.connections)):
        connection_ids.append([station.id for station in tubemap.connections[i].stations])
    
    return connection_ids

def find_connections(connection_ID_list, ID):
    """For a given ID, return all the connection ID pairs where ID is in the list """
    matches = list()
    for i in range(len(connection_ID_list)):
        if ID in connection_ID_list[i]:
            matches.append(connection_ID_list[i])
    
    return matches
    

def get_neighbour_IDs(match_list, station_id):
    """ Strip the matches just down to a list of unqiue station IDs excluding the station ID itself """
    for item in match_list:
        item.remove(station_id)
    flat_list = [item for sublist in match_list for item in sublist]
    neighbours = list(set(flat_list))
    
    return neighbours

def get_neighbours(station_id, tubemap):
    """ For each station, get a list of station IDs of its neighbours via connections."""
    
    connection_ids = get_connection_ID_pairs(tubemap)
    matches = find_connections(connection_ids, station_id)
    neighbours = get_neighbour_IDs(matches, station_id)
    
    return neighbours


def return_neighbour_connections(station_neighbours, tube_obj, station_id):
    """ Build the inner dictionary so each station ID has a dict of all its connections."""
    inner_dict = dict()
    
    # for each neighbour, get a list of connections
    for neighbour_id in station_neighbours:
        neighbour_connections = list()
        
        for i in range(len(tube_obj.connections)):
            stations = [station.id for station in tube_obj.connections[i].stations]
            if station_id in stations and neighbour_id in stations:
                neighbour_connections.append(tube_obj.connections[i])
            
        inner_dict.update({neighbour_id: neighbour_connections})
     
    return inner_dict