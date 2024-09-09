
class Agent:
    def __init__(self, goal_node):
        """
        Initialize the agent with a goal node.
        :param goal_node: The goal node the agent aims to reach.
        """
        self.goal_node = goal_node
        self.path = []


    def find_path(self, start_node, edge_costs):
        """
        Find best path from start node to dest node taking the cost into account
        :param start_node: The source node the agent starts from.
        :param edge_costs: A dictionary of with edges as keys and the time cost to cross the edge as values..
        """
        return None

