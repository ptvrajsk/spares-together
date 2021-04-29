$start_node = Read-Host -Prompt "Enter Start node"
$goal_node = Read-Host -Prompt "Enter Goal Node"
python3 .\main.py .\data\csv\nodes.csv .\data\csv\connections.csv .\data\csv\truck.csv .\data\csv\package_units.csv .\data\csv\packages.csv $start_node $goal_node