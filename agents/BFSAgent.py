from collections import deque
from agents.agent import Agent


class BFSAgent(Agent):
    def __init__(self, goal_node, edges, nodes_positions, max_speed_limit):
        """
        Initialize the BFS agent
        """
        super().__init__(goal_node, edges, nodes_positions, max_speed_limit)

    def find_path(self, start_node, edge_costs):
        """
        Implement BFS to find the shortest path from start_node to the goal_node.
        :param start_node: The source node the agent starts from.
        :param edges: A list of directed edges represented as tuples (start_node, end_node).
        :param edge_costs: A dictionary of edges with their respective time costs.
        :return: A tuple containing the path found, or None if no path is found.
        """
        # Initialize the queue with the starting node, an empty path, and zero cost.
        queue = deque([(start_node, [], 0)])  # (current_node, path, total_time_cost)
        visited = set()

        while queue:
            current_node, path, current_time_cost = queue.popleft()

            # Check if the goal node is reached
            if current_node == self.goal_node:
                # path_len = len(path)
                # for i in range(path_len):
                #     if i != path_len - 1:
                #         self.path.append((path[i], path[i + 1]))
                self.total_cost = current_time_cost
                self.path = path
                return self.path

            if current_node in visited:
                continue

            visited.add(current_node)

            # Explore outgoing edges from the current node
            for edge in self.edges:
                if edge[0] == current_node:
                    next_node = edge[1]
                    new_time_cost = current_time_cost + edge_costs[edge]  # Add edge's time cost

                    if next_node not in visited:
                        queue.append((next_node, path + [edge], new_time_cost))

        # No path found
        self.path = None
        self.total_cost = float('inf')
        return None


