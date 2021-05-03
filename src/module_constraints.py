"""
  This module contains all code that handles solving constraints.

  ....

  Accessible Classes
  ------------------
  TruckDelegator
    This class will primarily handle solving constraints related
    to sorting packages and package routes into trucks.
"""

from enum import Enum
from src.module_route_searcher import RouteSearcher
from src.model_data import ParsedData

class _ConstraintRules(Enum):
  """Enumeration to Easily identify the index of
  constraints in the constraints dictionary.

  Args:
      Enum (int): Describes the index of constraint.
  """
  OVERWEIGHT = 0

class TruckDelegator:
  """
    This class will primarily handle solving constraints related
    to sorting packages and package routes into trucks.

    ....

    Attributes
    ----------
    routeSearcher: RouteSearcher
      RouteSearcher instantiation in charge of handling all actions related to searching
      for optimal routes between nodes.

    truck_max_weight: int
      An Integer value that represents the maximum amount of data that can be stored
      on a truck.

    package_types: dict
      A Dictionary that stores data relating types of packages and their respective weights.

    package_data: dict
      A Dictionary that stores data regarding each individual package and its associated data.

    constraints: dict
      A Dictionary containing a set of constraints that must be abided by to form a valid truck
      load for delivery.

    Methods
    -------
    getOptimizedRoute() -> dict:
      A Function that optimizes the delivery routes for all packages.

  """

  routeSearcher: RouteSearcher = None
  truck_max_weight: int = None
  package_types: dict = None
  package_data: dict = None
  # Key refers to Rule Description, Value is Rule
  contraints = None

  def __init__(self, parsedData: ParsedData) -> None:
    self.routeSearcher = RouteSearcher(parsedData)
    self.truck_max_weight = parsedData.get_max_truck_weight()
    self.package_types = parsedData.get_package_type_data()
    self.package_data = parsedData.get_package_data()
    # Key refers to Rule Description, Value is Rule
    self.contraints = {
      _ConstraintRules.OVERWEIGHT.value: self._isTruckOverweight
    }

  def getOptimizedRoute(self) -> dict:
    """Optimizes the delivery route of a set number of packages.

    Returns:
        dict: Dictionary containing truck loads and their individual
        optimized paths.
    """
    truck_loads = self.routeSearcher.getRoutesForEachPackage()
    return self._combineSharedRoutes(truck_loads)

  def _combineSharedRoutes(self, individual_truck_loads: dict) -> dict:
    """Combines a set of truck loads if any of them share a common route

    Args:
        individual_truck_loads (dict): Dictionary containing individidual
        truck load information.

    Returns:
        dict: Dictionary containing combined truck load information.
    """
    combined_package_routes = dict()

    for truck_load_id, load_data in individual_truck_loads.items():

        isMerged = False
        (individual_package, individual_route) = load_data
        
        for newtruck_id, (combined_packages, combined_route) in combined_package_routes.items():
          hypothetical_new_package_load = combined_packages + [individual_package]

          """  If merging these 2 packages into a single truck load causes a constraint fail then don't bother. """
          if self.contraints[_ConstraintRules.OVERWEIGHT.value](hypothetical_new_package_load):
            continue
          
          """ Find overlapping route and merge them together. """
          if self._isSubList(individual_route, combined_route):
            combined_package_routes[newtruck_id] = (hypothetical_new_package_load, combined_route)
            isMerged = True
          elif self._isSubList(combined_route, individual_route):
            combined_package_routes[newtruck_id] = (hypothetical_new_package_load, individual_route)
            isMerged = True
          
        """ If overlapping route not found, for now package will be in its own load. """
        if not isMerged:
          combined_package_routes[len(combined_package_routes.keys())] = ([individual_package], individual_route)

    return combined_package_routes

  def _extract_package_weight(self, package_id: str) -> str:
    """Extracts a package's category from its ID

    Args:
        package_id (str): Package ID

    Returns:
        str: String representing the package's category
    """
    (category, _) = self.package_data[package_id]
    return self.package_types[category]

  def _isTruckOverweight(self, truck_packages: list) -> bool:
    """Checks if a particular set of packages abide by the
    weight constraint.

    Args:
        truck_packages (list): List of package IDs

    Returns:
        bool: True if they abide by weight constraint, false otherwise.
    """
    # [Pack_1, Pack_3] -> (map) -> [1, 2] -> (sum) -> 3
    return sum(map(self._extract_package_weight, truck_packages)) > self.truck_max_weight

          
  def _isSubList(self, list1: list, list2: list) -> bool:
      """Checks if one list is a sub-list of the other
      in the exact order.

      Args:
          list1 (list): A list of values.
          list2 (list): A list of values.

      Returns:
          bool: True if list1 is a sub-list of list2, False
          otherwise.
      """
      lenList1 = len(list1)
      if lenList1 > len(list2):
        return False

      counter = 0
      while counter < lenList1:
        if list1[counter] != list2[counter]:
          return False
        counter += 1
      return True




