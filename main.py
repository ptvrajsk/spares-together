import sys
from src.module_parser import InputParser
from src.module_route_searcher import RouteSearcher


if __name__ == "__main__":

  if(len(sys.argv) != 5):
    print("Missing Parameters!")
    print(f"Usage: python {sys.argv[0]} <path_to_nodes_csv> <path_to_connections_csv> <start_node> <goal_node>")
    quit()

  try:
    parser = InputParser(sys.argv[1], sys.argv[2])
    routeSearcher = RouteSearcher(parser.get_node_data(), parser.get_connection_data(), \
      parser.get_existing_connections())
    print(routeSearcher.getOptimalRoute(sys.argv[3], sys.argv[4]))
  except ValueError as e:
    print(e.message)