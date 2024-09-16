
ASTAR__ZERO_H = 0
ASTAR__AERIAL_DIST_H = 1
ASTAR__DIJKSTRA_H = 2
ASTAR__COMBINATION_H = 3
ASTAR__NONADMISSIBLE_H = 4
QLEARNING = 5

class Agent:
    def __init__(self, goal_node, edges, nodes_positions, max_speed_limit):
        """
        Initialize the agent.
        """
        self.goal_node = goal_node
        self.path = []
        self.edges = edges
        self.nodes_positions = nodes_positions
        self.max_speed_limit = max_speed_limit


    def find_path(self, start_node, edge_costs):
        """
        Find best path from start node to dest node taking the cost into account
        :param start_node: The source node the agent starts from.
        :param edge_costs: A dictionary of with edges as keys and the time cost to cross the edge as values..
        """
        return None

