echo -n "Enter Start Node: "
read start_node
echo -n "Enter Goal Node: "
read goal_node
python3 a-star-spares.py ./Data/csv/nodes.csv ./Data/csv/connections.csv $start_node $goal_node