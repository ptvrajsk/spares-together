import sys
from src.module_parser import InputParser
from src.module_constraints import TruckDelegator

if __name__ == "__main__":

  if(len(sys.argv) != 6):
    print("Missing Parameters!")
    print(f"Usage: python {sys.argv[0]} <path_to_nodes_csv> <path_to_connections_csv> <path_to_truck_data> <path_to_package_type_data> <path_to_packages>")
    quit()

  try:
    parser = InputParser(sys.argv[1], sys.argv[2], \
      sys.argv[3], sys.argv[4], sys.argv[5])
    truckDelegator = TruckDelegator(parser.get_parsed_data())
    truckDelegator.optimizeRoute()
  except ValueError as e:
    print(e.message)