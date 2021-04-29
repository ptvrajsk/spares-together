import csv
from enum import Enum
from queue import Queue

# To help identify which index of the array contains
# which value
class NodeHeaders(Enum):
  NODE = 0
  X_CO = 1
  Y_CO = 2

# To help identify which index of the array contains
# which value
class ConnectionHeaders(Enum):
  NODE_A = 0
  NODE_B = 1
  IS_AVAIL = 2
  DIST = 3

# To help identify which index of the array contains
# which value
class TruckHeaders(Enum):
  MAX_TRUCK_WEIGHT = 0

# To help identify which index of the array contains
# which value
class PackageUnitHeaders(Enum):
  PACKAGE_TYPE = 0
  WEIGHT = 1

# To help identify which index of the array contains
# which value
class PackageHeaders(Enum):
  PACKAGE_ID = 0
  PACKAGE_TYPE = 1
  PACKAGE_GOAL = 2

# Parses CSV Input for Search Algorithm
class InputParser:
  # Stores the coordinates of each node
  node_coords = dict()
  # Stores the distance between 2 coordinates
  coord_connections = dict()
  # Stores the list of possible connections to each node
  existing_connections = dict()
  # Truck Max Units
  truck_max_units = None
  # Package Types
  pack_types = dict()
  # Package Data
  pack_data = dict()

  def __init__(self, nodes_path, connections_path, \
    truck_path, package_type_path, package_data_path):
    self.read_nodes(nodes_path)
    self.read_connections(connections_path)
    self.read_truck_data(truck_path)
    self.read_package_types(package_type_path)
    self.read_packages(package_data_path)
    self.validateGraphConnectedness()


  def read_truck_data(self, truck_path):
    with open(truck_path, 'r') as truck_file:
      truck_reader = csv.reader(truck_file)
      next(truck_reader)
      for row in truck_reader:
        self.truck_max_units = int(row[TruckHeaders.MAX_TRUCK_WEIGHT.value])
      # print(f"Max Truck Weight: {self.truck_max_units}") # NOTE: For Debugging

  def read_package_types(self, package_type_path):
    with open(package_type_path, 'r') as package_type_file:
      package_type_reader = csv.reader(package_type_file)
      next(package_type_reader)
      for row in package_type_reader:
        # Stores a dictionary where the key is a package type and
        # the value is the weight of the package type.
        # node_coords['S'] = 1
        self.pack_types[row[PackageUnitHeaders.PACKAGE_TYPE.value]] = int(row[PackageUnitHeaders.WEIGHT.value])
      # print(f"Package Type Details: {self.pack_types}") # NOTE: For Debugging

  def read_packages(self, package_data_path):
    with open(package_data_path, 'r') as package_data_file:
      package_data_reader = csv.reader(package_data_file)
      next(package_data_reader)
      for row in package_data_reader:
        # Stores a dictionary where the key is a package id and
        # the tuple of its corresponding type and goal destination.
        # node_coords['Pack_1'] = (M, A)
        self.pack_data[row[PackageHeaders.PACKAGE_ID.value]] = (row[PackageHeaders.PACKAGE_TYPE.value], row[PackageHeaders.PACKAGE_GOAL.value])
      # print(f"Package Type Details: {self.pack_data}") # NOTE: For Debugging

  def read_nodes(self, nodes_path):
    with open(nodes_path, 'r') as nodes_file:
      node_reader = csv.reader(nodes_file)
      next(node_reader)
      for row in node_reader:
        # Stores a dictionary where the key is a node and
        # the value is a tuple of the (X, Y) coordinate.
        # node_coords['A'] = (X Coord of A, Y Coord of A)
        self.node_coords[row[NodeHeaders.NODE.value]] = (int(row[NodeHeaders.X_CO.value]), int(row[NodeHeaders.Y_CO.value]))
      # print(self.node_coords) # NOTE: For Debugging

  def read_connections(self, connections_path):
    with open(connections_path, 'r') as nodes_file:
      connection_reader = csv.reader(nodes_file)
      next(connection_reader)
      for row in connection_reader:
        # If connection doesn't exist between the 2 Nodes,
        # Skip reading their distance
        if(not int(row[ConnectionHeaders.IS_AVAIL.value])):
          continue
        
        if(row[ConnectionHeaders.NODE_A.value] not in self.existing_connections):
          self.existing_connections[row[ConnectionHeaders.NODE_A.value]] = list()
        
        if(row[ConnectionHeaders.NODE_B.value] not in self.existing_connections):
          self.existing_connections[row[ConnectionHeaders.NODE_B.value]] = list()

        self.existing_connections[row[ConnectionHeaders.NODE_A.value]].append(row[ConnectionHeaders.NODE_B.value])
        self.existing_connections[row[ConnectionHeaders.NODE_B.value]].append(row[ConnectionHeaders.NODE_A.value])

        # Stores a dictionary where the key is a tuple that
        # consists of 2 nodes and and the value is the actual
        # distance between them.
        # E.g. coord_connections[(A, B)] = (Dist Between A and B)
        # & coord_connections[(B, A)] = (Dist Between A and B)
        # (I'm increasing the space complexity here so it doesn't look too efficient lol)
        self.coord_connections[(row[ConnectionHeaders.NODE_A.value], row[ConnectionHeaders.NODE_B.value])] \
          = int(row[ConnectionHeaders.DIST.value])
        self.coord_connections[(row[ConnectionHeaders.NODE_B.value], row[ConnectionHeaders.NODE_A.value])] \
          = int(row[ConnectionHeaders.DIST.value])
    # print(self.coord_connections) # NOTE: For Debugging

  def getDFSNodes(self, startNode, maxNodes=0):
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

  def validateGraphConnectedness(self):
    # Get the first node on the list
    allInputNodes = list(self.node_coords.keys())
    numInputNodes = len(allInputNodes)
    startNode = allInputNodes[0]
    visitedNodes = self.getDFSNodes(startNode)

    if len(visitedNodes) != numInputNodes:
      raise ValueError("Input nodes and connections do NOT result in a connected graph")

  def get_node_data(self):
    return self.node_coords

  def get_connection_data(self):
    return self.coord_connections
  
  def get_existing_connections(self):
    return self.existing_connections