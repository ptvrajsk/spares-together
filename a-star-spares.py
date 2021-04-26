import sys
import csv
import math
from enum import Enum
from queue import PriorityQueue

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
    
    with open(nodes_path, 'r') as nodes_file:
      node_reader = csv.reader(nodes_file)
      next(node_reader)
      for row in node_reader:
        # Stores a dictionary where the key is a node and
        # the value is a tuple of the (X, Y) coordinate.
        # node_coords['A'] = (X Coord of A, Y Coord of A)
        self.node_coords[row[NodeHeaders.NODE.value]] = (int(row[NodeHeaders.X_CO.value]), int(row[NodeHeaders.Y_CO.value]))

      # print(self.node_coords)

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
        
      # print(self.coord_connections)

  def get_node_data(self):
    return self.node_coords

  def get_connection_data(self):
    return self.coord_connections
  
  def get_existing_connections(self):
    return self.existing_connections


class RouteSearcher:

  node_coords = None
  coord_connections = None
  existing_connections = None

  def __init__(self, node_coords, coord_connections, existing_connections):
    self.node_coords = node_coords
    self.coord_connections = coord_connections
    self.existing_connections = existing_connections

  # Basic Distance between points formula for heuristic measure
  # Straight line distance ensures admissibility
  def heuristic_distance(self, node_a, node_b):
    (node_a_x, node_a_y) = self.node_coords[node_a]
    (node_b_x, node_b_y) = self.node_coords[node_b]
    return math.sqrt(math.pow((node_a_x - node_b_x), 2) + math.pow((node_a_y - node_b_y), 2))

  def retrace_steps(self, start_node, goal_node, visited_node_pairs):
    steps = [goal_node]
    current_node = goal_node
    
    while current_node != start_node:
      for (parent, child) in visited_node_pairs:
        if(child == current_node):
          steps.append(parent)
          current_node = parent
          break
    steps.reverse()
    return steps

  def getOptimalRoute(self, start_node, goal_node):
    isRouteComplete = False
    visited_node_pairs = []
    pq = PriorityQueue()
    root_branches = self.existing_connections[start_node]
    for branch in root_branches:
      heur_dist = self.heuristic_distance(branch, goal_node)
      path_cost = self.coord_connections[(start_node, branch)]
      # Fills priority queue with ((Heur Dist to Goal + Dist to Branch), Path Cost, Branch, Parent Node)
      # so that Priority Queue can sort the closes branch
      pq.put(((heur_dist + path_cost), path_cost, branch, start_node))
    
    while not pq.empty():
      # Extract Queue Data
      (calculated_dist, total_path_cost, current_node, parent_node) = pq.get()

      # Set Visited Path
      visited_node_pairs.append((parent_node, current_node))

      if current_node == goal_node:
        print(visited_node_pairs)
        return self.retrace_steps(start_node, goal_node, visited_node_pairs)
      
      # Add all possible newly possible routes
      branches = self.existing_connections[current_node]
      for branch in branches:
        
        # Don't want to backstep from to the node we came from
        if branch == parent_node:
          continue

        heur_dist = self.heuristic_distance(branch, goal_node)
        total_path_cost += self.coord_connections[(current_node, branch)]
        pq.put(((heur_dist + total_path_cost), total_path_cost, branch, current_node))

    return "ERROR: Route NOT found"


if __name__ == "__main__":
  parser = InputParser(sys.argv[1], sys.argv[2])
  routeSearcher = RouteSearcher(parser.get_node_data(), parser.get_connection_data(), \
    parser.get_existing_connections())
  print(routeSearcher.getOptimalRoute(sys.argv[3], sys.argv[4]))