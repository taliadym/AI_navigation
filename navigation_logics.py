import numpy as np
from agents.AStarAgent import AStarAgent
from agents.QLearningAgent import QLearningAgent
import csv
from agents.agent import ASTAR__ZERO_H, ASTAR__ARIAL_DIST_H, ASTAR__DIJKSTRA_H, QLEARNING

RESULTS_FILE = 'results_recording.csv'
speed_limits = [20, 40, 80, 90, 120]
max_speed_limit = max(speed_limits)


def add_row_to_csv(row, file_path):
    with open(file_path, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=row.keys())

        # Check if the file is empty; if so, write the header
        if file.tell() == 0:  # Check if the file is empty
            writer.writeheader()
        writer.writerow(row)


class NavigationLogics:
    def __init__(self, nodes, edges, src_node, dest_node, nodes_positions, results_file=RESULTS_FILE, agent_enum=0):
        self.nodes = nodes
        self.src_node = src_node
        self.dest_node = dest_node
        self.nodes_positions = nodes_positions

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

        # all agents will be recorded,
        # but only the path according to agent_enum will be shown on gui and forwarded to manager
        self.agents = [
            # *** agents for changing costs ***
            AStarAgent(dest_node, self.edges, nodes_positions, max_speed_limit, self.road_length, ASTAR__ZERO_H),
            AStarAgent(dest_node, self.edges, nodes_positions, max_speed_limit, self.road_length, ASTAR__ARIAL_DIST_H),
            AStarAgent(dest_node, self.edges, nodes_positions, max_speed_limit, self.road_length, ASTAR__DIJKSTRA_H),
            QLearningAgent(dest_node, self.edges, nodes_positions, max_speed_limit),
            # *** agents for mean costs ***
            AStarAgent(dest_node, self.edges, nodes_positions, max_speed_limit, self.road_length, ASTAR__ZERO_H),
            AStarAgent(dest_node, self.edges, nodes_positions, max_speed_limit, self.road_length, ASTAR__ARIAL_DIST_H),
            AStarAgent(dest_node, self.edges, nodes_positions, max_speed_limit, self.road_length, ASTAR__DIJKSTRA_H),
            QLearningAgent(dest_node, self.edges, nodes_positions, max_speed_limit)]

        self.agent_enum = agent_enum
        self.agent_current_d_paths = [None for _ in self.agents]
        self.agent_current_node = [self.src_node for _ in self.agents]
        self.agent_total_path_cost = [0 for _ in self.agents]
        self.results_file = results_file
        self.num_of_different_agents = 4
        self.calculate_paths_only_once = True

    def get_edge_dist(self, edge):
        n1, n2 = edge
        pos1 = self.nodes_positions[n1]
        pos2 = self.nodes_positions[n2]
        return np.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

    def get_first_edge(self, path):
        if path is None:
            return None
        if len(path) == 0:
            return None
        return path[0]

    def get_time_for_crossing_edge(self, edge):
        if edge is None:
            return 0
        v = (1 - self.traffic_index[edge]) * self.speed_limit[edge]
        x = self.road_length[edge]
        return x / v

    def get_mean_time_for_crossing_edge(self, edge):
        if edge is None:
            return 0
        v = (1 - self.edge_traffic_mean[edge]) * self.speed_limit[edge]
        x = self.road_length[edge]
        return x / v

    def record_agents_results(self):
        row = {}

        # fill row with agents results
        for i in range(len(self.agents)):
            row[str(i)] = round(60 * self.agent_total_path_cost[i], 2)

        add_row_to_csv(row, self.results_file)

    def find_path_of_all_agents(self, changing_time_cost, mean_time_cost):

        for i in range(self.num_of_different_agents):

            # *** changing costs ***
            # update path
            self.agent_current_d_paths[i] = \
                self.agents[i].find_path(self.agent_current_node[i], changing_time_cost)

            # update cost
            self.agent_total_path_cost[i] += self.get_time_for_crossing_edge(
                self.get_first_edge(self.agent_current_d_paths[i]))

            # update current node
            if self.agent_current_d_paths[i]:
                self.agent_current_node[i] = self.agent_current_d_paths[i][0][1]

            # *** mean costs ***
            if self.calculate_paths_only_once:
                # update path
                self.agent_current_d_paths[i + self.num_of_different_agents] = \
                    self.agents[i + self.num_of_different_agents].find_path(
                        self.agent_current_node[i + self.num_of_different_agents], mean_time_cost)

                # update cost
                self.agent_total_path_cost[i + self.num_of_different_agents] += self.get_time_for_crossing_edge(
                    self.get_first_edge(self.agent_current_d_paths[i + self.num_of_different_agents]))
        self.calculate_paths_only_once = False

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
        changing_time_cost = {edge: self.get_time_for_crossing_edge(edge) for edge in self.edges}
        mean_time_cost = {edge: self.get_mean_time_for_crossing_edge(edge) for edge in self.edges}

        # calculate paths by each one of the agents
        self.find_path_of_all_agents(changing_time_cost, mean_time_cost)

        # save path and current node according to the requested agent (this will be forwarded to manager - shown on gui)
        self.current_d_path = self.agent_current_d_paths[self.agent_enum]
        self.current_node = self.agent_current_node[self.agent_enum]

        # TODO: delete
        print(self.current_node)
        print(self.current_d_path)

        if self.current_node == self.dest_node:
            # record all agents results into csv file
            self.record_agents_results()
