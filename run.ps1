$start_node = Read-Host -Prompt "Enter Start node"
$goal_node = Read-Host -Prompt "Enter Goal Node"
python3 .\main.py .\data\csv\nodes.csv .\data\csv\connections.csv $start_node $goal_node