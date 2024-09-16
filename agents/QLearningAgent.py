import random
from collections import defaultdict
from agents.agent import Agent
import numpy as np


class QLearningAgent(Agent):
    def __init__(self, goal_node, edges, nodes_positions, max_speed_limit, learning_rate=0.9, discount_factor=0.9,
                 exploration_rate=0.1):
        """
        Initialize the Q-learning agent with parameters for learning.

        :param goal_node: The goal node the agent aims to reach.
        :param edges: List of edges represented as tuples (start_node, end_node).
        :param nodes_positions: Dictionary of node positions {node: (x, y)}.
        :param max_speed_limit: The maximum speed limit for heuristic calculations.
        :param learning_rate: The learning rate (alpha) for Q-value updates.
        :param discount_factor: The discount factor (gamma) to weigh future rewards.
        :param exploration_rate: The initial exploration rate (epsilon) for epsilon-greedy strategy.
        """
        super().__init__(goal_node, edges, nodes_positions, max_speed_limit)

        # self.q_table is a defaultdict where each key corresponds to a state (a node in our Q-learning context).
        # The value of each key is another defaultdict, which represents the actions for that state.
        # This inner dictionary holds the Q-values associated with each possible action from the given state.
        self.q_table = defaultdict(lambda: defaultdict(float))

        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
    def get_possible_actions(self, current_node):
        """
        Get all possible actions (edges) from the current node.

        :param current_node: The n9ode from which to find possible actions.
        :return: A list of possible edges (actions).
        """
        # print("the edges are: ", self.edges)
        a = [edge for edge in self.edges if edge[0] == current_node]
        # print("cur node is: ", current_node, ", and the edges are:", a)
        return a

    def choose_action(self, current_node):
        """
        Choose an action using an epsilon-greedy strategy.

        :param current_node: The current node of the agent.
        :return: The chosen action (edge).
        """
        if random.uniform(0, 1) < self.exploration_rate:
            # Explore: select a random action
            actions = self.get_possible_actions(current_node)
            if actions:
                return random.choice(actions)
            else:
                return None
        else:
            # Exploit: select the action with the highest Q-value
            possible_actions = self.get_possible_actions(current_node)
            if not possible_actions:
                return None
            # Choose the action with the maximum Q-value
            best_action = max(possible_actions, key=lambda action: self.q_table[current_node][action])
            return best_action

    def update_q_value(self, current_node, action, reward, next_node):
        """
        Update the Q-value for a state-action pair.

        :param current_node: The current node of the agent.
        :param action: The action taken (edge).
        :param reward: The reward received after taking the action.
        :param next_node: The resulting node after taking the action.
        """
        current_q_value = self.q_table[current_node][action]
        max_future_q = max(self.q_table[next_node].values(), default=0)
        new_q_value = current_q_value + self.learning_rate * (
                    reward + self.discount_factor * max_future_q - current_q_value)
        self.q_table[current_node][action] = new_q_value

    def find_path(self, start_node, edge_costs, episodes=100):
        """
        Find the optimal path using Q-learning by training over multiple episodes.

        :param start_node: The starting node of the agent.
        :param edge_costs: A dictionary of edges and their associated time costs.
        :param episodes: The number of episodes for training.
        :return: The learned optimal path from start to goal node.
        """

        for episode in range(episodes):
            current_node = start_node
            path = []

            while current_node != self.goal_node:
                # Choose an action based on the current node
                action = self.choose_action(current_node)
                if action is None:
                    break  # No possible actions; terminate

                next_node = action[1]  # The destination node of the selected edge
                reward = -edge_costs.get(action, float('inf'))  # Negative reward to minimize cost

                # Update the Q-value for the state-action pair
                self.update_q_value(current_node, action, reward, next_node)

                # Move to the next node
                current_node = next_node
                path.append(action)

            # Decay exploration rate over time to reduce randomness
            self.exploration_rate *= 0.995

        # After training, determine the best path by exploiting learned Q-values
        return self._exploit_path(start_node)

    def _exploit_path(self, start_node):
        """
        Exploit the learned Q-values to find the best path.

        :param start_node: The starting node of the agent.
        :return: The optimal path according to the Q-table.
        """
        current_node = start_node
        path = []

        while current_node != self.goal_node:
            action = self.choose_action(current_node)
            if action is None:
                break
            current_node = action[1]
            path.append(action)

        self.path = path
        return path
