echo -n "Enter Start Node: "
read start_node
echo -n "Enter Goal Node: "
read goal_node
python3 main.py ./data/csv/nodes.csv ./data/csv/connections.csv ./data/csv/truck.csv ./data/csv/package_units.csv ./data/csv/packages.csv $start_node $goal_node