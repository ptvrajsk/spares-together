"""
  This Module holds all parsing related classes, functions and code.

  ....

  Accessible Classes
  ------------------
  InputParser
    A class that handles all the parsing of data files to extract information
    and pass on for further analysis.
"""

import csv
from enum import Enum
from queue import Queue
from src.model_data import ParsedData

class _NodeHeaders(Enum):
  """Enumeration to Easily identify the index of
  variables related to Node Information.

  Args:
      Enum (int): Describes the index of node data when
      parsed from .csv
  """
  NODE = 0
  X_CO = 1
  Y_CO = 2

class _ConnectionHeaders(Enum):
  """Enumeration to Easily identify the index of
  variables related to Node Connection Information.

  Args:
      Enum (int): Describes the index of data when
      parsed from .csv
  """
  NODE_A = 0
  NODE_B = 1
  IS_AVAIL = 2
  DIST = 3

class _TruckHeaders(Enum):
  """Enumeration to Easily identify the index of
  variables related to Truck Information.

  Args:
      Enum (int): Describes the index of data when
      parsed from .csv
  """
  MAX_TRUCK_WEIGHT = 0

class _PackageUnitHeaders(Enum):
  """Enumeration to Easily identify the index of
  variables related to Package Type Information.

  Args:
      Enum (int): Describes the index of data when
      parsed from .csv
  """
  PACKAGE_TYPE = 0
  WEIGHT = 1

class _PackageHeaders(Enum):
  """Enumeration to Easily identify the index of
  variables related to Package Data Information.

  Args:
      Enum (int): Describes the index of data when
      parsed from .csv
  """
  PACKAGE_ID = 0
  PACKAGE_TYPE = 1
  PACKAGE_GOAL = 2

class InputParser:
  """
  A class that handles all the parsing of data files to extract information
  and pass on for further analysis.

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
  read_truck_data(truck_path: str)
    Reads truck data from external file.
  
  read_package_types()
    Reads package type data from external file.
  
  read_packages()
    Reads package data from external file.
  
  read_nodes()
    Reads node data from external file.
  
  read_connections()
    Reads connections data from external file.

  get_parsed_data() -> ParsedData
    Returns a ParsedData Package
  """

  # Stores the coordinates of each node
  node_coords: dict = dict()
  # Stores the distance between 2 coordinates
  coord_connections: dict = dict()
  # Stores the list of possible connections to each node
  existing_connections: dict = dict()
  # Truck Max Units
  truck_max_units: int = None
  # Package Types
  pack_types: dict = dict()
  # Package Data
  pack_data: dict = dict()

  def __init__(self, nodes_path: str, connections_path: str, \
    truck_path: str, package_type_path: str, package_data_path: str):
    self.read_nodes(nodes_path)
    self.read_connections(connections_path)
    self.read_truck_data(truck_path)
    self.read_package_types(package_type_path)
    self.read_packages(package_data_path)
    self.__validateGraphConnectedness()


  def read_truck_data(self, truck_path: str):
    """Reads Truck data from .csv file.

    Args:
        truck_path (string): String representing the
        path to the relevant .csv file.
    """
    with open(truck_path, 'r') as truck_file:
      truck_reader = csv.reader(truck_file)
      next(truck_reader)
      for row in truck_reader:
        self.truck_max_units = int(row[_TruckHeaders.MAX_TRUCK_WEIGHT.value])
      # print(f"Max Truck Weight: {self.truck_max_units}") # NOTE: For Debugging

  def read_package_types(self, package_type_path: str) -> None:
    """Read Package Type Data from .csv file.

    Args:
        package_type_path (string): String representing the
        path to the relevant .csv file.
    """
    with open(package_type_path, 'r') as package_type_file:
      package_type_reader = csv.reader(package_type_file)
      next(package_type_reader)
      for row in package_type_reader:
        # Stores a dictionary where the key is a package type and
        # the value is the weight of the package type.
        # node_coords['S'] = 1
        self.pack_types[row[_PackageUnitHeaders.PACKAGE_TYPE.value]] = int(row[_PackageUnitHeaders.WEIGHT.value])
      # print(f"Package Type Details: {self.pack_types}") # NOTE: For Debugging

  def read_packages(self, package_data_path: str) -> None:
    """Reads Package Data from .csv file.

    Args:
        package_data_path (string): String representing the
        path to the relevant .csv file.
    """
    with open(package_data_path, 'r') as package_data_file:
      package_data_reader = csv.reader(package_data_file)
      next(package_data_reader)
      for row in package_data_reader:
        # Stores a dictionary where the key is a package id and
        # the tuple of its corresponding type and goal destination.
        # node_coords['Pack_1'] = (M, A)
        self.pack_data[row[_PackageHeaders.PACKAGE_ID.value]] = (row[_PackageHeaders.PACKAGE_TYPE.value], row[_PackageHeaders.PACKAGE_GOAL.value])
      # print(f"Package Type Details: {self.pack_data}") # NOTE: For Debugging

  def read_nodes(self, nodes_path: str) -> None:
    """Reads Node Data from .csv file.

    Args:
        nodes_path (string): String representing the
        path to the relevant .csv file.
    """
    with open(nodes_path, 'r') as nodes_file:
      node_reader = csv.reader(nodes_file)
      next(node_reader)
      for row in node_reader:
        # Stores a dictionary where the key is a node and
        # the value is a tuple of the (X, Y) coordinate.
        # node_coords['A'] = (X Coord of A, Y Coord of A)
        self.node_coords[row[_NodeHeaders.NODE.value]] = (int(row[_NodeHeaders.X_CO.value]), int(row[_NodeHeaders.Y_CO.value]))
      # print(self.node_coords) # NOTE: For Debugging

  def read_connections(self, connections_path: str) -> None:
    """Read node connections from .csv file.

    Args:
        connections_path (string): String representing the
        path to the relevant .csv file.
    """
    with open(connections_path, 'r') as nodes_file:
      connection_reader = csv.reader(nodes_file)
      next(connection_reader)
      for row in connection_reader:
        # If connection doesn't exist between the 2 Nodes,
        # Skip reading their distance
        if(not int(row[_ConnectionHeaders.IS_AVAIL.value])):
          continue
        
        if(row[_ConnectionHeaders.NODE_A.value] not in self.existing_connections):
          self.existing_connections[row[_ConnectionHeaders.NODE_A.value]] = list()
        
        if(row[_ConnectionHeaders.NODE_B.value] not in self.existing_connections):
          self.existing_connections[row[_ConnectionHeaders.NODE_B.value]] = list()

        self.existing_connections[row[_ConnectionHeaders.NODE_A.value]].append(row[_ConnectionHeaders.NODE_B.value])
        self.existing_connections[row[_ConnectionHeaders.NODE_B.value]].append(row[_ConnectionHeaders.NODE_A.value])

        # Stores a dictionary where the key is a tuple that
        # consists of 2 nodes and and the value is the actual
        # distance between them.
        # E.g. coord_connections[(A, B)] = (Dist Between A and B)
        # & coord_connections[(B, A)] = (Dist Between A and B)
        # (I'm increasing the space complexity here so it doesn't look too efficient lol)
        self.coord_connections[(row[_ConnectionHeaders.NODE_A.value], row[_ConnectionHeaders.NODE_B.value])] \
          = int(row[_ConnectionHeaders.DIST.value])
        self.coord_connections[(row[_ConnectionHeaders.NODE_B.value], row[_ConnectionHeaders.NODE_A.value])] \
          = int(row[_ConnectionHeaders.DIST.value])
    # print(self.coord_connections) # NOTE: For Debugging

  def __getAllTraversableNodes(self, startNode: str, maxNodes:int = 0) -> list:
    """Performs a DFS from start node to check if all
    nodes in the graph can be reached.

    Args:
        startNode (string): String representing the starting node.
        maxNodes (int, optional): Number of nodes expected to be
        present for a fully connected graph. Defaults to 0.

    Returns:
        list: List containing all nodes visited by DFS from the
        startNode.
    """
    visited = [startNode]
    q = Queue()
    list(map(q.put, self.existing_connections[startNode]))

    while not q.empty():
      # Check if the max number of nodes have been visited
      # to cut short the DFS
      if maxNodes:
        if len(visited) == maxNodes:
          return visited
      
      neighbour = q.get()
      if neighbour not in visited:
        visited.append(neighbour)
      for node in self.existing_connections[neighbour]:
        if node not in visited:
          q.put(node)
    return visited

  def __validateGraphConnectedness(self) -> None:
    """Ensures that the graph of nodes and connections
    result in a connected graph (i.e. All nodes can travel
    to all other nodes in some way).

    Raises:
        ValueError: Throws an error (To prevent program from
        continuing) if the graph is not connected.
    """
    # Get the first node on the list
    allInputNodes = list(self.node_coords.keys())
    numInputNodes = len(allInputNodes)
    startNode = allInputNodes[0]
    visitedNodes = self.__getAllTraversableNodes(startNode)

    if len(visitedNodes) != numInputNodes:
      raise ValueError("Input nodes and connections do NOT result in a connected graph")

  def get_parsed_data(self) -> ParsedData:
    """Returns a parsed data object containing all
    parsed information

    Returns:
        ParsedData: A ParsedData object that acts as a container
        for all processed data.
    """
    return ParsedData(self.node_coords, self.coord_connections, self.existing_connections, \
      self.truck_max_units, self.pack_types, self.pack_data)
