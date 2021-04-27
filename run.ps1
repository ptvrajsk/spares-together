$start_node = Read-Host -Prompt "Enter Start node"
$goal_node = Read-Host -Prompt "Enter Goal Node"
python3 .\a-star-spares.py .\Data\csv\nodes.csv .\Data\csv\connections.csv $start_node $goal_node