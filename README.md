# Smart Navigation

## Description

This project focuses on solving the problem of efficient navigation between two points within a road network, akin to applications like Google Maps or Waze. The problem is modeled as a dynamic graph where intersections are represented as nodes and roads as edges, with real-time traffic conditions influencing the optimal route. The objective is to find the fastest path between two locations, considering fluctuating traffic conditions, road lengths, and speed limits.

## Getting Started

These instructions will help you set up and run the project on your local machine.

### Setting Up the Environment

1. **Clone the Repository**

   First, clone the repository to your local machine.

   ```bash
   git clone https://github.com/taliadym/AI_navigation.git
   cd AI_navigation
   ```

2. **Create a Virtual Environment**

   Create a virtual environment to manage project dependencies. This keeps your project isolated from other Python projects.

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**

   - **On Windows:**

     ```bash
     venv\Scripts\activate
     ```

   - **On macOS and Linux:**

     ```bash
     source venv/bin/activate
     ```

   After activation, your command prompt should show the name of the virtual environment, indicating that it is active.

4. **Install Project Dependencies**

   With the virtual environment active, install the required packages listed in the `requirements.txt` file.

   ```bash
   pip install -r requirements.txt
   ```

### Running the Project

To run the project on randomly generated nodes and edges, with random starting point and destination, displaying the A* zero heuristic, run:
```bash
python main.py
```

To run the project on randomly generated nodes and edges, with random starting point and destination, displaying an agent of your choice, run:
```bash
python main.py -a <agent number>
```
where the agents number are as follows:

0: A* Zero Heuristic

1: A* Aerial Dist Heuristic

2: A* Dijkstra Heuristic

3: A* Combination Heuristic

4: A* Non-Admissible Heuristic

5: Q Learning