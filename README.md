# Project Process

## Idea of Optimality
For this project, what constitutes an optimal route is a route which manages to distribute from the Supply Depo (start node) to all deliverable nodes (goal nodes) in the shortest travel distance. [Will probably ditch the Priority Requirement due to time constraint in implementation]

## Generating Data

### Nodes
The generated graph must be connected (i.e. all nodes must be able to access all other nodes with some through some route). To do this,

- To start of we produced a random set of `17` nodes using a coordinate system (`(X, Y)` coordinates like on a graph)
- This will allow us to easily compute heuristic estimates (straight-line-distance) and assign arbitrary values for the actual distance as needed by the `A* Search` component of our program.

### Supply Depot
We also set aside a node to act as the supply point (since the our tool is supposed to address a delivery issue) and all trips will begin at this `SupplyDepot` node. The coordinates for this node is also randomized just like all other nodes.

### Connections
- Generated a set of random connections between the nodes where each node has a `70%` chance of a valid connection to another node.
  - The `70%` was an approximate figure. For a graph to definitely be connected we found that it needs to have at least `n-1` and at most `n * (n-1)/2` nodes, given that we are starting with a set of `17` nodes. We experimented and concluded that a probability of `0.7` consistently gave us connected graphs that generated routes of approximately `1 to 5` nodes which is sufficient for a Proof-Of-Concept program.

### Package Types
To introduce the constraint satisfaction issue, we created package types that have a corresponding weight that will act as a limiter on the amount of cargo that can be stored on a single truck load. These are,

- `S` - Small `(Weight: 1)`
- `M` - Small `(Weight: 2)`
- `L` - Small `(Weight: 3)`

### Max Truck Load
Along with the package weights, we also assigned a maximum weight limit of `10` on the truck which will be used for our CSP later.

### Package Data
Generating package data was trivial once the parameters of the package were already defined. Primarily we need to ensure that each package has,

- `Package ID` - For identification
- `Type` - For the individual package's weight.
- `Goal` - Where the package was to be delivered.

## Algorithmic Planning
To generate optimal routes, we felt that beginning with the route search first would be best as the delivery route should be considered in tandem with the constraints when deciding how to optimize the load. So we landed upon the general idea of,

- Check Optimal Route for each package (assuming that it takes its constitutes its own truck load)
- Iterate through packages and routes while checking constraints to decide how we can merge routes and package loads for least distance travelled.

## Route Searching
Uses the typical A* Search algorithm, not much to say here.

## Constraint Satisfaction
Currently the primary constraint is weight. So when we generate possible combinations of routes for the packages we need to ensure that the weight limits are not breached.

Another idea perhaps is to consider different constraints for different steps of the optimization process. i.e.,

- When direclty merging shared routes only check for weight.
- When trying to combine branching routes into a singular truck load we must check for weight + that the distance travelled of our new route is not greater than doing both old routes seperately. For e.g.

  - Pack_1 -> [SuplyDepot, A, B, D]
  - Pack_2 -> [SupplyDepot, A, K]
  - If we decide to have Pack_1 and 2 in a single load the distance travelled by for example, [SupplyDepot, A, K, B, D] must be lesser or equal to the combined distances of [SuplyDepot, A, B, D] + [SupplyDepot, A, K]
  - @@@@Just and Idea, need to test workability and optimality@@@@

## Looking at Time Complexity
It would primarily seem that a majority of the time complexity comes from repeating the `A* Search` for a set of `n` packages and performing the constraint satisfaction process for these `n` individual routes would make up the over-arching Time Complextiy of the program. At the moment, since CSP part is still in progress, we need to re-visit examining the time complexity based on our implementation of the CSP.

## Space Complexity
Pretty much same thing as time, need to wait and see.

## Code Structuring
We split the files into separate modules that handle different sections of the code (e.g parsing, searching, csp, modelling data, etc...). This way its easier to reference and document and trace through our program should we face any bugs or come need to make any tweaks.