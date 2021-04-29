"""
  This module handles all code related to modelling all data that
  is utilized by the program.
"""

class ParsedData:
  """
  A class used act as a container to handle parsed data. This is
  primarily used to reduce the number of parameters passed across
  the various classes in this script.

  ....

  Attributes
  ----------
  node_coords: dict
    A Dictionary containing information about a Node and its Coordinates
  
  coord_connections: dict.
    A Dictionary containing information about tuples of Nodes and their respective
    connection distances.
  
  existing_connections: dict
    A dictionary containing information about each Node and its possible Neighbouring
    Nodes.
  
  truck_max_units: int
    An Integer value that represents the maximum amount of data that can be stored
    on a truck.
  
  pack_types: dict
    A Dictionary that stores data relating types of packages and their respective weights.
  
  pack_data: dict
    A Dictionary that stores data regarding each individual package and its associated data.


  Methods
  -------
  get_node_data() -> dict
    Returns Node Data.
  
  get_connection_data() -> dict
    Returns connection data.
  
  get_existing_connections() -> dict
    Returns data representing the neighbours of each node.
  
  get_max_truck_weight() -> int
    Returns data representing the maximum load of a truck.
  
  get_package_type_data() -> dict
    Returns data representing package classifications.
  
  get_package_data() -> dict
    Returns data representing input packages.
  """

  # Stores the coordinates of each node
  node_coords = None
  # Stores the distance between 2 coordinates
  coord_connections = None
  # Stores the list of possible connections to each node
  existing_connections = None
  # Truck Max Units
  truck_max_units = None
  # Package Types
  pack_types = None
  # Package Data
  pack_data = None

  def __init__(self, node_coords: dict, coord_connections: dict, existing_connections: dict, truck_max_units: int, \
    pack_types: dict, pack_data: dict):
    self.node_coords = node_coords
    self.coord_connections = coord_connections
    self.existing_connections = existing_connections
    self.truck_max_units = truck_max_units
    self.pack_types = pack_types
    self.pack_data = pack_data

  def get_node_data(self) -> dict:
    """Returns Node Data.

    Returns:
        dict: Dictionary data containing Nodes and their coordinates.
    """
    return self.node_coords

  def get_connection_data(self) -> dict:
    """Returns connection data.

    Returns:
        dict: Dictionary data containing pairs of nodes and information
        about their connection.
    """
    return self.coord_connections

  def get_existing_connections(self) -> dict:
    """Returns data representing the neighbours of each node.

    Returns:
        dict: Dictionary data containing each node and all
        neighbours to that node.
    """
    return self.existing_connections

  def get_max_truck_weight(self) -> int:
    """Returns data representing the maximum load of a truck.

    Returns:
        int: Integer representing the maximum truck weight.
    """
    return self.truck_max_units

  def get_package_type_data(self) -> dict:
    """Returns data representing package classifications.

    Returns:
        dict: Dictionary data about the type of packages and
        their weights.
    """
    return self.pack_types

  def get_package_data(self) -> dict:
    """Returns data representing input packages.

    Returns:
        dict: Dictionary data containing each all input packages,
        their type and goal location.
    """
    return self.pack_data
