from collections import deque

def bfs(src_node, dest_node, edges, time_cost):
    queue = deque([(src_node, [src_node], 0)])  # (current_node, path, total_time_cost)
    visited = set()

    while queue:
        current_node, path, current_time_cost = queue.popleft()

        if current_node == dest_node:
            return path, current_time_cost  # Return path and total time cost when destination is reached

        if current_node in visited:
            continue

        visited.add(current_node)

        # Explore outgoing edges from the current node
        for edge in edges:
            if edge[0] == current_node:
                next_node = edge[1]
                new_time_cost = current_time_cost + time_cost.get(edge, float('inf'))  # Add edge's time cost

                if next_node not in visited:
                    queue.append((next_node, path + [next_node], new_time_cost))

    return None # No path found, return None and infinite cost
