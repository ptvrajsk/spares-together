import sys
import csv
from enum import Enum

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
  CSV_DELIM = ','
  node_coords = dict()
  coord_connections = dict()

  def __init__(self, nodes_path, connections_path):
    
    with open(nodes_path, 'r') as nodes_file:
      node_reader = csv.reader(nodes_file)
      next(node_reader)
      for row in node_reader:
        # Stores a dictionary where the key is a node and
        # the value is a tuple of the (X, Y) coordinate.
        # node_coords['A'] = (X Coord of A, Y Coord of A)
        self.node_coords[row[NodeHeaders.NODE.value]] = (row[NodeHeaders.X_CO.value], row[NodeHeaders.Y_CO.value])

      # print(self.node_coords)

    with open(connections_path, 'r') as nodes_file:
      connection_reader = csv.reader(nodes_file)
      next(connection_reader)
      for row in connection_reader:
        # If connection doesn't exist between the 2 Nodes,
        # Skip reading their distance
        if(not int(row[ConnectionHeaders.IS_AVAIL.value])):
          continue

        # Stores a dictionary where the key is a tuple that
        # consists of 2 nodes and and the value is the actual
        # distance between them.
        # E.g. coord_connections[(A, B)] = (Dist Between A and B)\
        self.coord_connections[(row[ConnectionHeaders.NODE_A.value], row[ConnectionHeaders.NODE_B.value])] \
          = row[ConnectionHeaders.DIST.value]
        
      # print(self.coord_connections)
    


if __name__ == "__main__":
  parser = InputParser(sys.argv[1], sys.argv[2])