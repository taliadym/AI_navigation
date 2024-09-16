import argparse
from navigation_manager import run_random_graph, NavigationManager

def main():
    parser = argparse.ArgumentParser(description='Run navigation simulation with various agents.')
    parser.add_argument(
        '-a',
        type=int,
        choices=range(6),
        default=0,
        help='Choose the agent number (0: A* Zero Heuristic, 1: A* Aerial Distance Heuristic, 2: A* Dijkstra Heuristic, 3: A* Combination Heuristic, 4: A* Non-Admissible Heuristic, 5: Q Learning)'
    )
    args = parser.parse_args()
    agent_number = args.a
    nodes, edges, src, dest = run_random_graph()
    visualizer = NavigationManager(nodes, edges, src, dest, agent_number)
    visualizer.run()


if __name__ == '__main__':
    main()