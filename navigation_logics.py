import numpy as np
from agents.AStarAgent import AStarAgent

speed_limits = [20, 40, 80, 90, 120]
max_speed_limit = max(speed_limits)


class NavigationLogics:
    def __init__(self, nodes, edges, src_node, dest_node, nodes_positions):
        self.nodes = nodes
        self.src_node = src_node
        self.dest_node = dest_node
        self.nodes_positions = nodes_positions
        self.agent = AStarAgent(dest_node, edges, nodes_positions, max_speed_limit)

        # where the car is currently
        self.current_node = self.src_node

        # this holds the current path - sorted list of DIRECTED edges from current_node to dest_node
        self.current_d_path = []

        # this holds the traffic index for each edge (0-no traffic, 1-full traffic), should be in (0, 1) - NOT 0, 1
        self.edges = []
        self.traffic_index = {edge: 0 for edge in edges}
        self.edge_traffic_mean = {}
        self.edge_traffic_std = {}
        self.speed_limit = {}
        self.road_length = {}

        for edge in edges:
            self.edges.append(edge)
            self.edge_traffic_mean[edge] = np.random.uniform(0.001, 0.9)
            self.edge_traffic_std[edge] = np.random.uniform(0.1, 0.9)
            self.speed_limit[edge] = speed_limits[int(np.random.uniform(0, 5))]
            self.road_length[edge] = round(100 * self.get_edge_dist(edge), 4)

        # add the opposite direction to all edges
        for edge in edges:
            n1, n2 = edge
            opposite_edge = (n2, n1)
            self.edges.append(opposite_edge)
            self.edge_traffic_mean[opposite_edge] = self.edge_traffic_mean[edge]
            self.edge_traffic_std[opposite_edge] = self.edge_traffic_std[edge]
            self.speed_limit[opposite_edge] = self.speed_limit[edge]
            self.road_length[opposite_edge] = self.road_length[edge]
            self.traffic_index[opposite_edge] = self.traffic_index[edge]

    def get_edge_dist(self, edge):
        n1, n2 = edge
        pos1 = self.nodes_positions[n1]
        pos2 = self.nodes_positions[n2]
        return np.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

    def get_time_for_crossing_edge(self, edge):
        if edge is None:
            return 0
        v = (1 - self.traffic_index[edge]) * self.speed_limit[edge]
        x = self.road_length[edge]
        return x / v

    def update(self):
        # called in each iteration by manager::run

        # update traffic index: draw from normal distribution
        for edge in self.edges:
            mean = self.edge_traffic_mean[edge]
            std = self.edge_traffic_std[edge]
            index = np.random.normal(mean, std)
            index = min(0.99999, index)
            index = max(0.00001, index)
            self.traffic_index[edge] = index

        # find the current_d_path: self.current_node->self.dest_node, using agent
        time_cost = {edge: self.get_time_for_crossing_edge(edge) for edge in self.edges}
        # self.current_d_path = a_star(self.current_node, self.dest_node, self.edges, time_cost, self.nodes_positions, max_speed_limit)
        self.current_d_path = self.agent.find_path(self.current_node, time_cost)
        # self.current_d_path = bfs(self.current_node, self.dest_node, self.edges, time_cost)

        print(self.current_node)
        print(self.current_d_path)

        # update current node
        if self.current_d_path:
            self.current_node = self.current_d_path[0][1]




