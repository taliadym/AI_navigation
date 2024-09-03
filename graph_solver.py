
class GraphSolver:
    def __init__(self, nodes, edges, src_node, dest_node):
        self.nodes = nodes
        self.edges = edges
        self.src_node = src_node
        self.dest_node = dest_node

        # where the car is currently
        self.current_node = self.src_node

        # this holds the current path - sorted list of DIRECTED edges from current_node to dest_node
        self.current_d_path = []

        # this holds the traffic index for each edge (0-no traffic, 1-full traffic), should be in (0, 1) - NOT 0, 1
        self.traffic_index = {edge: 0 for edge in self.edges}

    def run_solver(self):
        # use agent
        return 0  # called in each iteration by graph_gui::run
