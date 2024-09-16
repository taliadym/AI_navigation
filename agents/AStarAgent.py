import heapq
import math
from collections import defaultdict
from agents.agent import Agent, ASTAR__ZERO_H, ASTAR__ARIAL_DIST_H, ASTAR__DIJKSTRA_H, ASTAR__COMBINATION_H, ASTAR__NONADMISSIBLE_H


class AStarAgent(Agent):
    def __init__(self, goal_node, edges, nodes_positions, roads_length, speed_limit, heuristic):
        """
        Initialize the A* agent with additional parameters needed for pathfinding.

        :param start_node: The starting node of the agent.
        :param goal_node: The goal node the agent aims to reach.
        :param edges: List of edges represented as tuples (start_node, end_node).
        :param edge_costs: Dictionary with edge costs {(start_node, end_node): cost}.
        :param nodes_positions: Dictionary of node positions {node: (x, y)}.
        """
        max_speed_limit = 120
        min_speed_limit = 20
        super().__init__(goal_node, edges, nodes_positions, max_speed_limit)
        self.heuristic = ZeroHeuristic()
        if heuristic == ASTAR__ARIAL_DIST_H:
            self.heuristic = ArialDistHeuristic(nodes_positions, max_speed_limit)
        elif heuristic == ASTAR__DIJKSTRA_H:
            self.heuristic = DijkstraHeuristic(goal_node, edges, roads_length, speed_limit)
        elif heuristic == ASTAR__COMBINATION_H:
            self.heuristic = AdmissibleCombinationHeuristic(nodes_positions, max_speed_limit, goal_node, edges, roads_length, speed_limit)
        elif heuristic == ASTAR__NONADMISSIBLE_H:
            self.heuristic = NonAdmissibleHeuristic(nodes_positions, min_speed_limit, speed_limit)

    def find_path(self, start_node, edge_costs):
        """Find the shortest path from the start node to the goal node using A* algorithm."""
        # Initialize the priority queue with edges starting from the start node
        open_set = []  # (f_cost, current_edge, total_cost, path)

        # Start with edges directed out from the source node
        for edge in self.edges:
            if edge[0] == start_node:
                initial_cost = edge_costs.get(edge, float('inf'))
                f_cost = initial_cost + self.heuristic.heuristic(edge[1], self.goal_node)
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
                new_f_cost = new_g_cost + self.heuristic.heuristic(next_edge[1], self.goal_node)

                # Add the new path to the priority queue
                heapq.heappush(open_set, (new_f_cost, next_edge, new_g_cost, path + [next_edge]))

        return None  # No path found


class Heuristic():
    def heuristic(self, start_node, goal):
        pass


class ZeroHeuristic(Heuristic):
    def heuristic(self, start_node, goal):
        return 0

class NonAdmissibleHeuristic(Heuristic):
    def __init__(self, nodes_positions, min_speed_limit, speed_limit):
        self.nodes_positions = nodes_positions
        self.min_speed_limit = float(min_speed_limit) * 0.01
        self.speed_limit = speed_limit

    def heuristic(self, start_node, goal):
        """
        the heuristic calculates the time it takes to get from node to goal under two relaxations:
        1. there exists a direct path from node to goal with length which is exactly their arial distance
        2. the speed limit in that path is the minimal, and there is no traffic
        """
        node_pos = self.nodes_positions[start_node]
        goal_pos = self.nodes_positions[goal]
        distance = math.sqrt((node_pos[0] - goal_pos[0]) ** 2 + (node_pos[1] - goal_pos[1]) ** 2)
        return distance / self.min_speed_limit

class AdmissibleCombinationHeuristic(Heuristic):
    def __init__(self, nodes_positions, max_speed_limit, goal_node, edges, roads_length, speed_limit):
        self.arial = ArialDistHeuristic(nodes_positions, max_speed_limit)
        self.dijkstra = DijkstraHeuristic(goal_node, edges, roads_length, speed_limit)

    def heuristic(self, start_node, goal_node):
        return 0.5 * self.arial.heuristic(start_node, goal_node) +\
               0.5 * self.dijkstra.heuristic(start_node, goal_node)


class ArialDistHeuristic(Heuristic):
    def __init__(self, nodes_positions, max_speed_limit):
        self.nodes_positions = nodes_positions
        self.max_speed_limit = max_speed_limit

    def heuristic(self, start_node, goal):
        """
        the heuristic calculates the time it takes to get from node to goal under two relaxations:
        1. there exists a direct path from node to goal with length which is exactly their arial distance
        2. the speed limit in that path is the maximal, and there is no traffic
        """
        node_pos = self.nodes_positions[start_node]
        goal_pos = self.nodes_positions[goal]
        distance = math.sqrt((node_pos[0] - goal_pos[0]) ** 2 + (node_pos[1] - goal_pos[1]) ** 2)
        return distance / self.max_speed_limit


class DijkstraHeuristic(Heuristic):
    def __init__(self, goal_node, edges, roads_length, speed_limit):
        """
        Initialize the DijkstraHeuristic with precomputed shortest path costs from all nodes to the goal node.
        """
        self.goal_node = goal_node
        self.edges = edges
        self.edge_costs = {edge: roads_length[edge]/speed_limit[edge] for edge in edges}
        self.dijkstra_costs = self.compute_dijkstra_costs()

    def compute_dijkstra_costs(self):
        """
        Compute shortest path costs from all nodes to the goal node using Dijkstra's algorithm.
        Returns a dictionary with nodes as keys and their cost to the goal node as values.
        """
        costs = defaultdict(lambda: float('inf'))
        costs[self.goal_node] = 0
        priority_queue = [(0, self.goal_node)]  # (cost, node)

        # Reverse the edges to work from goal node backwards
        reverse_edges = defaultdict(list)
        for start, end in self.edges:
            reverse_edges[end].append((start, self.edge_costs.get((start, end), float('inf'))))

        visited = set()

        while priority_queue:
            current_cost, current_node = heapq.heappop(priority_queue)

            if current_node in visited:
                continue
            visited.add(current_node)

            for neighbor, edge_cost in reverse_edges[current_node]:
                new_cost = current_cost + edge_cost
                if new_cost < costs[neighbor]:
                    costs[neighbor] = new_cost
                    heapq.heappush(priority_queue, (new_cost, neighbor))

        return costs

    def heuristic(self, start_node, goal):
        """
        Return the precomputed Dijkstra cost from the start node to the goal node.
        """
        return self.dijkstra_costs.get(start_node, float('inf'))


