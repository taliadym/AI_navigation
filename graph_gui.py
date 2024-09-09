import pygame
import networkx as nx
import math


# Define the GraphVisualizer class
class GraphVisualizer:
    def __init__(self, nodes, edges, src_node, dest_node):
        self.nodes = nodes
        self.edges = edges
        self.src_node = src_node
        self.dest_node = dest_node

        # Initialize pygame and set up the display
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Graph Visualizer')

        # Set up the graph using networkx
        self.graph = nx.Graph()
        self.graph.add_nodes_from(nodes)
        self.graph.add_edges_from(edges)

        # Compute the positions of the nodes using a spring layout
        self.positions = nx.spring_layout(self.graph, seed=42)
        self.node_color = (50, 100, 200)  # Node color
        self.node_radius = 10  # Radius of nodes
        self.font = pygame.font.SysFont(None, 24)

        # Load an image to display over an edge
        self.car_image = pygame.image.load('car.png')  # Update path to your image
        self.car_image = pygame.transform.scale(self.car_image, (80, 80))  # Scale the image to fit

    def draw_car_on_edge(self, edge):
        start_pos = self.positions[edge[0]]
        end_pos = self.positions[edge[1]]
        start_screen_pos = self.to_screen(start_pos)
        end_screen_pos = self.to_screen(end_pos)

        # Calculate the midpoint of the edge
        midpoint = ((start_screen_pos[0] + end_screen_pos[0]) // 2,
                    (start_screen_pos[1] + end_screen_pos[1]) // 2)

        # Calculate the angle of the edge in degrees
        angle = math.degrees(math.atan2(end_screen_pos[0] - start_screen_pos[0],
                             end_screen_pos[1] - start_screen_pos[1]))

        # Rotate the car image based on the calculated angle
        rotated_car = pygame.transform.rotate(self.car_image,
                                              angle)  # Negative angle to adjust for Pygame's rotation direction

        # Blit (draw) the rotated car image at the midpoint of the edge
        rotated_rect = rotated_car.get_rect(center=midpoint)
        self.screen.blit(rotated_car, rotated_rect)

    def draw_graph(self, colors, d_edge_for_car):
        # Clear the screen with a white background
        self.screen.fill((255, 255, 255))

        # Draw edges
        for edge in self.graph.edges():
            start_pos = self.positions[edge[0]]
            end_pos = self.positions[edge[1]]
            pygame.draw.line(self.screen, colors[edge],
                             self.to_screen(start_pos), self.to_screen(end_pos), 2)
        self.draw_car_on_edge(d_edge_for_car)

        # Draw nodes
        for node in self.graph.nodes():
            pos = self.positions[node]
            screen_pos = self.to_screen(pos)

            # Highlight src_node and dest_node with different colors or effects
            if node == self.src_node:
                color = (0, 255, 0)  # Green color for source node
                pygame.draw.circle(
                    self.screen, color, self.to_screen(pos), self.node_radius + 5, 3)
                self.draw_text("Starting Point", screen_pos)

            elif node == self.dest_node:
                color = (255, 0, 0)  # Red color for destination node
                pygame.draw.circle(
                    self.screen, color, self.to_screen(pos), self.node_radius + 5, 3)
                self.draw_text("Destination", screen_pos)
            else:
                color = self.node_color

                pygame.draw.circle(self.screen, color, self.to_screen(pos), self.node_radius)

        # Update the display
        pygame.display.flip()

    def to_screen(self, pos):
        """Convert position from graph layout (-1,1) range to screen coordinates."""
        x = int((pos[0] + 1) * (self.width - 200) / 2 + 100)  # Scale and center
        y = int((pos[1] + 1) * (self.height - 200) / 2 + 100)
        return x, y

    def draw_text(self, text, position):
        """Draw text labels near the nodes."""
        text_surface = self.font.render(text, True, (0, 0, 0))  # Render text in black color
        text_rect = text_surface.get_rect(center=(position[0], position[1] - 30))  # Position text above the node
        self.screen.blit(text_surface, text_rect)  # Draw text on the screen

    def run(self):
        red_intensity = 0
        # Main loop to handle events and update the graph visualization
        running = True
        while running:
            red_intensity = (red_intensity + 1) % 255
            color = (red_intensity, 0, 0)
            colors = {edge : color for edge in self.edges}
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw_graph(colors, (1, 2))
        pygame.quit()


# Example usage
nodes = [1, 2, 3, 4, 5]
edges = [(1, 2), (1, 3), (2, 4), (3, 5), (4, 5)]

# Create a GraphVisualizer object and run it
visualizer = GraphVisualizer(nodes, edges, 1, 5)
visualizer.run()
