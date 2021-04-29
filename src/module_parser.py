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

# Parses CSV Input for Search Algorithm
class InputParser:
  # Stores the coordinates of each node
  node_coords = dict()
  # Stores the distance between 2 coordinates
  coord_connections = dict()
  # Stores the list of possible connections to each node
  existing_connections = dict()

  def __init__(self, nodes_path, connections_path):
    self.read_nodes(nodes_path)
    self.read_connections(connections_path)
    self.validateGraphConnectedness()
      

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