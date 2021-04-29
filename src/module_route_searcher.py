import math
from queue import PriorityQueue

# Performs A* Search Given Data Points  & Start + Goal Node
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