import numpy as np
from a_star import a_star

speed_limits = [20, 40, 80, 90, 120]


class NavigationLogics:
    def __init__(self, nodes, edges, src_node, dest_node):
        self.nodes = nodes
        self.src_node = src_node
        self.dest_node = dest_node

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
            self.edge_traffic_std[edge] = np.random.uniform(0.1, 0.5)
            self.speed_limit[edge] = speed_limits[int(np.random.uniform(0, 5))]
            self.road_length[edge] = np.random.uniform(0.1, 100)

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
        time_cost = {edge: self.road_length[edge]/((1 - self.traffic_index[edge]) * self.speed_limit[edge]) for edge in self.edges}
        self.current_d_path = a_star(self.current_node, self.dest_node, self.edges, time_cost)

        print(self.current_node)
        print(self.current_d_path)

        # update current node
        if self.current_d_path:
            self.current_node = self.current_d_path[0][1]




