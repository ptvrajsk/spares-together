import sys
import time
import pprint
from src.module_parser import InputParser
from src.module_constraints import TruckDelegator

if __name__ == "__main__":

  if(len(sys.argv) != 6):
    print("Missing Parameters!")
    print(f"Usage: python {sys.argv[0]} <path_to_nodes_csv> <path_to_connections_csv> <path_to_truck_data> <path_to_package_type_data> <path_to_packages>")
    quit()

  try:
    startTime = time.time()
    parser = InputParser(sys.argv[1], sys.argv[2], \
      sys.argv[3], sys.argv[4], sys.argv[5])
    truckDelegator = TruckDelegator(parser.get_parsed_data())
    optimizedRoute = truckDelegator.getOptimizedRoute()
    endTime = time.time()
    print("\n\n")
    print("Optimized Route:")
    print("----")
    for truckId, truck_load_data in optimizedRoute.items():
      packages, route = truck_load_data
      print(f"Trip ID:\t{truckId}")
      print(f"Packages:\t{packages}")
      print(f"Route:\t\t{route}")
      print("\n")

    # pprint.pprint(optimizedRoute)
    print("\n")
    print("Time Taken (s):")
    print("----")
    print(f"{endTime-startTime:.4}s")
    print("\n\n")

  except ValueError as e:
    print(e.message)