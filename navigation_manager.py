import pygame
import networkx as nx
import math
from navigation_logics import NavigationLogics
import time
import sys

class NavigationManager:

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

        # images
        self.car_image = pygame.image.load('images/car.png')
        self.car_image = pygame.transform.scale(self.car_image, (80, 80))  # Scale the image to fit
        self.start_point_image = pygame.image.load('images/start_point.jpeg')
        self.start_point_image = pygame.transform.scale(self.start_point_image, (34, 34))  # Scale the image to fit
        self.end_point_image = pygame.image.load('images/end_point.jpeg')
        self.end_point_image = pygame.transform.scale(self.end_point_image, (34, 34))

        self.visited_edges = []

        # logics
        self.logics = NavigationLogics(nodes, edges, src_node, dest_node)

    def draw_car_on_edge(self, edge):
        start_pos = self.positions[edge[0]]
        end_pos = self.positions[edge[1]]
        start_screen_pos = self.to_screen(start_pos)
        end_screen_pos = self.to_screen(end_pos)

        # Calculate the midpoint of the edge
        midpoint = ((start_screen_pos[0] + end_screen_pos[0]) // 2,
                    (start_screen_pos[1] + end_screen_pos[1]) // 2)

        # Calculate the angle of the edge in degrees
        angle = math.degrees(math.atan2(- end_screen_pos[0] + start_screen_pos[0],
                             - end_screen_pos[1] + start_screen_pos[1]))

        # Rotate the car image based on the     §\]calculated angle
        rotated_car = pygame.transform.rotate(self.car_image,
                                              angle)  # Negative angle to adjust for Pygame's rotation direction

        # Blit (draw) the rotated car image at the midpoint of the edge
        rotated_rect = rotated_car.get_rect(center=midpoint)
        self.screen.blit(rotated_car, rotated_rect)

    def edge_in_d_edge_list(self, edge, d_edge_list):
        n1, n2 = edge
        return (n1, n2) in d_edge_list or (n2, n1) in d_edge_list

    def draw_arrow(self, start_pos, end_pos, color):
        angle = math.atan2(end_pos[1] - start_pos[1], end_pos[0] - start_pos[0])
        arrowhead_length = 15

        # Calculate the points of the arrowhead
        arrow_point1 = (end_pos[0] - (arrowhead_length + 8) * math.cos(angle - math.pi / 6),
                        end_pos[1] - (arrowhead_length + 8) * math.sin(angle - math.pi / 6))
        arrow_point2 = (end_pos[0] - (arrowhead_length + 8) * math.cos(angle + math.pi / 6),
                        end_pos[1] - (arrowhead_length + 8) * math.sin(angle + math.pi / 6))

        # Draw the arrowhead using a polygon
        pygame.draw.polygon(self.screen, color, [end_pos, arrow_point1, arrow_point2])

    def draw_graph(self, colors, current_d_path, current_d_edge):
        # Clear the screen with a white background
        self.screen.fill((255, 255, 255))
        self.draw_button()

        # Draw edges: color by traffic & mark current path
        for edge in self.edges:

            start_pos = self.to_screen(self.positions[edge[0]])
            end_pos = self.to_screen(self.positions[edge[1]])
            color = colors[edge]
            line_width = 2

            if self.edge_in_d_edge_list(edge, self.visited_edges):
                # color visited in green
                color = (0, 255, 0)

            if self.edge_in_d_edge_list(edge, current_d_path):
                # mark current planned path to dest
                line_width = 5
                color = colors[edge]
                self.draw_arrow(start_pos, end_pos, color)

            pygame.draw.line(self.screen, color,
                             start_pos, end_pos, line_width)

        # draw car on the current edge
        self.draw_car_on_edge(current_d_edge)
        self.visited_edges.append(current_d_edge)

        # Draw nodes: mark src & dist
        for node in self.graph.nodes():
            pos = self.positions[node]
            screen_pos = self.to_screen(pos)

            # Highlight src_node and dest_node with different colors or effects
            if node == self.src_node:
                pygame.draw.circle(self.screen, self.node_color, screen_pos, self.node_radius + 16, 3)
                self.draw_text("Starting Point", screen_pos, self.node_color)
                self.screen.blit(self.start_point_image, (screen_pos[0] - 17, screen_pos[1] - 17))

            elif node == self.dest_node:
                pygame.draw.circle(self.screen, self.node_color, screen_pos, self.node_radius + 16, 3)
                self.draw_text("Destination", screen_pos, self.node_color)
                self.screen.blit(self.end_point_image, (screen_pos[0] - 17, screen_pos[1] - 17))
            else:
                pygame.draw.circle(self.screen, self.node_color, screen_pos, self.node_radius)

        # Update the display
        pygame.display.flip()

    def to_screen(self, pos):
        """Convert position from graph layout (-1,1) range to screen coordinates."""
        x = int((pos[0] + 1) * (self.width - 200) / 2 + 100)  # Scale and center
        y = int((pos[1] + 1) * (self.height - 200) / 2 + 100)
        return x, y

    def draw_text(self, text, position, color):
        """Draw text labels near the nodes."""
        text_surface = self.font.render(text, True, color)  # Render text in black color
        text_rect = text_surface.get_rect(center=(position[0], position[1] - 40))  # Position text above the node
        self.screen.blit(text_surface, text_rect)  # Draw text on the screen

    def translate_traffic_into_color(self):
        colors = {}
        for edge in self.edges:
            traffic = self.logics.traffic_index[edge]
            colors[edge] = (traffic * 255, 0, 0)
        return colors

    def draw_button(self):
        button_color = (200, 0, 0)  # Red color
        # button_hover_color = (255, 0, 0)  # Brighter red when hovered
        # self.button_rect = pygame.Rect(10, 10, 100, 50)  # (x, y, width, height)
        # font = pygame.font.SysFont(None, 36)
        # # Check if the mouse is over the button
        # mouse_pos = pygame.mouse.get_pos()
        # if self.button_rect.collidepoint(mouse_pos):
        #     pygame.draw.rect(self.screen, button_hover_color, self.button_rect)
        # else:
        #     pygame.draw.rect(self.screen, button_color, self.button_rect)
        #
        # # Render the button text
        # text = font.render("Quit", True, (0, 255, 255))
        # self.screen.blit(text, (self.button_rect.x + 20, self.button_rect.y + 10))

    def run(self):
        # Main loop to handle events and update the graph visualization
        running = True
        got_to_dest = False
        while running:
            self.draw_button()

            if not got_to_dest:
                # update logics
                self.logics.update()

                # get edge colors
                colors = self.translate_traffic_into_color()

                # get current directed path
                current_d_path = self.logics.current_d_path

                # get current directed edge
                current_d_edge = current_d_path[0]
                # check if got to dest
                if current_d_edge[1] == self.dest_node:
                    got_to_dest = True

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.button_rect.collidepoint(event.pos):
                            running = False  # Stop the game loop when the button is clicked

                self.draw_graph(colors, current_d_path, current_d_edge)
                # time.sleep(1)

        pygame.quit()
        sys.exit()


# Example usage
nodes = [1, 2, 3, 4, 5, 6, 7, 8]
edges = []
for i in range(len(nodes)):
    for j in range(len(nodes)):
        if i < j:
            edges.append((nodes[i], nodes[j]))


# Create a GraphVisualizer object and run it
visualizer = NavigationManager(nodes, edges, 1, 5)
visualizer.run()
