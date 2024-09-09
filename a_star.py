import heapq


def a_star(src_node, dest_node, edges, edge_costs):
    # Initialize the priority queue with edges starting from the src_node
    open_set = []  # (f_cost, current_edge, total_cost, path)

    # Start with edges directed out from the source node
    for edge in edges:
        if edge[0] == src_node:
            initial_cost = edge_costs.get(edge, float('inf'))
            heapq.heappush(open_set, (initial_cost + heuristic(edge[1], dest_node), edge, initial_cost, [edge]))

    # Track visited nodes to avoid revisiting
    visited = set()

    while open_set:
        # Pop the edge with the lowest f_cost from the priority queue
        current_f_cost, current_edge, current_g_cost, path = heapq.heappop(open_set)

        # Current node is the destination node of the current edge
        current_node = current_edge[1]

        # If the destination node is reached, return the path of edges
        if current_node == dest_node:
            return path

        # Mark the current node as visited
        visited.add(current_node)

        # Explore outgoing edges from the current node
        for next_edge in edges:
            # Ensure the edge starts from the current node and has not been visited
            if next_edge[0] != current_node or next_edge[1] in visited:
                continue

            # Calculate the g_cost for the new path
            new_g_cost = current_g_cost + edge_costs.get(next_edge, float('inf'))

            # Calculate f_cost using heuristic (0 by default)
            new_f_cost = new_g_cost + heuristic(next_edge[1], dest_node)

            # Add the new path to the priority queue
            heapq.heappush(open_set, (new_f_cost, next_edge, new_g_cost, path + [next_edge]))

    return None  # No path found


def heuristic(node, goal):
    # Placeholder heuristic (0 for simplicity, replace with distance if available)
    return 0

