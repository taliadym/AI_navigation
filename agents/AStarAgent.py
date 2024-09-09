import heapq
import math
from agents.agent import Agent

class AStarAgent(Agent):
    def __init__(self, goal_node, edges, nodes_positions, max_speed_limit):
        """
        Initialize the A* agent with additional parameters needed for pathfinding.

        :param start_node: The starting node of the agent.
        :param goal_node: The goal node the agent aims to reach.
        :param edges: List of edges represented as tuples (start_node, end_node).
        :param edge_costs: Dictionary with edge costs {(start_node, end_node): cost}.
        :param nodes_positions: Dictionary of node positions {node: (x, y)}.
        :param max_speed_limit: The maximum speed limit for heuristic calculations.
        """
        super().__init__(goal_node, edges, nodes_positions, max_speed_limit)

    def heuristic(self, node, goal):
        """
        Heuristic function calculating the estimated time to reach the goal.

        :param node: The current node.
        :param goal: The goal node.
        :return: The estimated time based on the Euclidean distance divided by the maximum speed limit.
        """
        node_pos = self.nodes_positions[node]
        goal_pos = self.nodes_positions[goal]
        distance = math.sqrt((node_pos[0] - goal_pos[0]) ** 2 + (node_pos[1] - goal_pos[1]) ** 2)
        return distance / self.max_speed_limit

    def find_path(self, start_node, edge_costs):
        """Find the shortest path from the start node to the goal node using A* algorithm."""
        # Initialize the priority queue with edges starting from the start node
        open_set = []  # (f_cost, current_edge, total_cost, path)

        # Start with edges directed out from the source node
        for edge in self.edges:
            if edge[0] == start_node:
                initial_cost = edge_costs.get(edge, float('inf'))
                f_cost = initial_cost + self.heuristic(edge[1], self.goal_node)
                heapq.heappush(open_set, (f_cost, edge, initial_cost, [edge]))

        # Track visited nodes to avoid revisiting
        visited = set()

        while open_set:
            # Pop the edge with the lowest f_cost from the priority queue
            current_f_cost, current_edge, current_g_cost, path = heapq.heappop(open_set)

            # Current node is the destination node of the current edge
            current_node = current_edge[1]

            # If the destination node is reached, return the path of edges
            if current_node == self.goal_node:
                self.path = path
                return path

            # Mark the current node as visited
            visited.add(current_node)

            # Explore outgoing edges from the current node
            for next_edge in self.edges:
                # Ensure the edge starts from the current node and has not been visited
                if next_edge[0] != current_node or next_edge[1] in visited:
                    continue

                # Calculate the g_cost for the new path
                new_g_cost = current_g_cost + edge_costs.get(next_edge, float('inf'))

                # Calculate f_cost using heuristic
                new_f_cost = new_g_cost + self.heuristic(next_edge[1], self.goal_node)

                # Add the new path to the priority queue
                heapq.heappush(open_set, (new_f_cost, next_edge, new_g_cost, path + [next_edge]))

        return None  # No path found
