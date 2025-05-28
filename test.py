def find_start_node(nodes):
    start_nodes = set()
    end_nodes = set()
    for start, end in nodes:
        start_nodes.add(start)
        end_nodes.add(end)
    candidate_start_nodes = start_nodes - end_nodes
    if len(candidate_start_nodes) == 1:
        return candidate_start_nodes.pop()
    else:
        return None


nodes = [("E", "G"), ("B", "D"), ("C", "F"), ("D", "C"),  ("Z", "B"), ("F", "E")]
start_node = find_start_node(nodes)
print("起点节点是：", start_node)
