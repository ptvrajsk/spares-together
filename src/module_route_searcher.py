"""
  This module holds all the code related route searching and optimization
"""
import math
from queue import PriorityQueue
from src.model_data import ParsedData

# Performs A* Search Given Data Points  & Start + Goal Node
class RouteSearcher:
  """
  A class that will handle all route optimization and searching
  to find an optimal route through nodes based on deliverables.

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
  
  package_data: dict
    A Dictionary that stores data regarding each individual package and its associated data.


  Methods
  -------  
  retrace_steps(start_node: str, goal_node: str, visited_node_pairs: list) -> list
    Returns a list of that starts and ends at the respective nodes.
  
  getOptimalRoute(start_node: str, goal_node: str) -> list
    Returns the an optimal route between 2 nodes.
  """

  node_coords: dict = None
  coord_connections: dict = None
  existing_connections: dict = None
  package_data: dict = None


  def __init__(self, parsedData: ParsedData) -> None:
    self.node_coords = parsedData.get_node_data()
    self.coord_connections = parsedData.get_connection_data()
    self.existing_connections = parsedData.get_existing_connections()
    self.package_data = parsedData.get_package_data()

  def getRoutesForEachPackage(self) -> dict:
    """Gets the optimal route for each package.

    Returns:
        dict: A Dictionary of arbitrary keys where each value
        is a tuple of a list of packages and their shared route.
    """

    package_route_combinations = dict()
    
    for package_id, package_data in self.package_data.items():
      (package_size, package_goal) = package_data
      package_route = self.getOptimalRoute(list(self.node_coords.keys())[0], package_goal)
      package_route_combinations[len(package_route_combinations.keys())] = (package_id, package_route)
    
    return package_route_combinations

  def _heuristic_distance(self, node_a: str, node_b: str) -> float:
    """Calculates and returns the heuristic distance between
    2 nodes.

    Args:
        node_a (str): Node to start heuristic calculation from.
        node_b (str): Node to start heuristic calculation from.

    Returns:
        float: Float representing distance between 2 nodes.
    """
    (node_a_x, node_a_y) = self.node_coords[node_a]
    (node_b_x, node_b_y) = self.node_coords[node_b]
    return math.sqrt(math.pow((node_a_x - node_b_x), 2) + math.pow((node_a_y - node_b_y), 2))

  def retrace_steps(self, start_node: str, goal_node: str, visited_node_pairs: list) -> list:
    """Retrieve the exact stepts from a starting node to a goal node
    given a list of visited nodes

    Args:
        start_node (str): Starting Node.
        goal_node (str): Ending Node.
        visited_node_pairs (list): List of tuples representing the
        currently visited node and immediate parent node.

    Returns:
        list: A list of nodes arranged from a start node and the
        list of node traversals to the end node.
    """
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

  def _get_actual_distance_between_directly_connected_nodes(self, nodeA: str, nodeB:str) -> int:
    return self.coord_connections[(nodeA, nodeB)]

  def getOptimalRoute(self, start_node: str, goal_node: str) -> list:
    """Calculates the optimal route from a start node to and end
    node using A* Search Algorithm

    Args:
        start_node (str): Starting Node.
        goal_node (str): Ending Node.

    Returns:
        list: List containing arrangement of nodes representing
        the optimal path.
    """
    visited_node_pairs = []
    pq = PriorityQueue()
    root_branches = self.existing_connections[start_node]
    for branch in root_branches:
      heur_dist = self._heuristic_distance(branch, goal_node)
      path_cost = self._get_actual_distance_between_directly_connected_nodes(start_node, branch)
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

        heur_dist = self._heuristic_distance(branch, goal_node)
        total_path_cost += self._get_actual_distance_between_directly_connected_nodes(current_node, branch)
        pq.put(((heur_dist + total_path_cost), total_path_cost, branch, current_node))

    return "ERROR: Route NOT found"