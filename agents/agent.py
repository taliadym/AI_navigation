
class Agent:
    def __init__(self, goal_node):
        """
        Initialize the agent with a start node and a goal node.

        :param start_node: The starting node of the agent.
        :param goal_node: The goal node the agent aims to reach.
        """
        self.goal_node = goal_node
        self.path = []

    def __str__(self):
        """String representation of the agent's current status."""
        return f"Agent at {self.current_node}, Goal: {self.goal_node}, Path: {self.path}"

    def find_path(self, start_node):
        return None

