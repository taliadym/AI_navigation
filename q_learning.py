import numpy as np
import random


# Define the environment
class GridWorld:
    def __init__(self, size, start, goal, obstacles):
        self.size = size
        self.start = start
        self.goal = goal
        self.obstacles = obstacles
        self.state = start

    def reset(self):
        self.state = self.start
        return self.state

    def step(self, action):
        row, col = self.state
        if action == 0:  # Up
            row = max(row - 1, 0)
        elif action == 1:  # Down
            row = min(row + 1, self.size - 1)
        elif action == 2:  # Left
            col = max(col - 1, 0)
        elif action == 3:  # Right
            col = min(col + 1, self.size - 1)

        next_state = (row, col)
        reward = -1  # Default reward
        if next_state == self.goal:
            reward = 10
        elif next_state in self.obstacles:
            reward = -10
            next_state = self.state  # Reset to current state if obstacle

        self.state = next_state
        return next_state, reward, (next_state == self.goal)  # State, Reward, Done (goal reached or not)


# Q-learning parameters
alpha = 0.1  # Learning rate
gamma = 0.9  # Discount factor
epsilon = 0.1  # Exploration rate
episodes = 1000
actions = 4  # Up, Down, Left, Right

# Define the grid world environment
grid_size = 5
start_state = (0, 0)
goal_state = (4, 4)
obstacles = [(1, 1), (2, 2), (3, 3)]  # Example obstacles
env = GridWorld(grid_size, start_state, goal_state, obstacles)

# Initialize Q-table (state-action pairs)
q_table = np.zeros((grid_size, grid_size, actions))

# Q-learning algorithm
for episode in range(episodes):
    state = env.reset()
    done = False

    while not done:
        row, col = state

        # Choose action (ε-greedy policy)
        if random.uniform(0, 1) < epsilon:
            action = random.randint(0, actions - 1)  # Explore: random action
        else:
            action = np.argmax(q_table[row, col])  # Exploit: best known action

        # Take action and observe the next state and reward
        next_state, reward, done = env.step(action)
        next_row, next_col = next_state

        # Update Q-value using the Q-learning update rule
        q_table[row, col, action] = q_table[row, col, action] + alpha * (
                reward + gamma * np.max(q_table[next_row, next_col]) - q_table[row, col, action]
        )

        # Move to the next state
        state = next_state

# Output learned Q-values (for visualizing the agent's learning)
print("Learned Q-table:")
print(q_table)
