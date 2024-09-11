import numpy as np
import pygame
import networkx as nx
import math
from navigation_logics import NavigationLogics
import sys
import time

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

        # images
        self.car_image = pygame.image.load('images/car.png')
        self.car_image = pygame.transform.scale(self.car_image, (80, 80))  # Scale the image to fit
        self.start_point_image = pygame.image.load('images/start_point.jpeg')
        self.start_point_image = pygame.transform.scale(self.start_point_image, (34, 34))  # Scale the image to fit
        self.end_point_image = pygame.image.load('images/end_point.jpeg')
        self.end_point_image = pygame.transform.scale(self.end_point_image, (34, 34))

        self.restart_game_logics()

    def restart_game_logics(self):
        self.visited_edges = set()
        self.colors = {edge: (0, 0, 0) for edge in self.edges}
        self.current_d_path = None
        self.current_d_edge = None
        self.timer = 0
        self.est_time = None
        self.prev_est_time = None
        self.prev_d_path = None
        self.logics = NavigationLogics(self.nodes, self.edges, self.src_node, self.dest_node, self.positions)

    def update_timer(self):
        # update timer
        if self.current_d_edge is not None:
            self.timer += self.logics.get_time_for_crossing_edge(self.current_d_edge)

    def update_estimated_time(self):
        # update estimated arrival time
        if len(self.current_d_path) > 0:
            self.est_time = self.timer
            for edge in self.current_d_path:
                self.est_time += self.logics.get_time_for_crossing_edge(edge)

        # update prev estimated arrival time - for the case where the path just changed
        self.prev_est_time = None
        if self.prev_d_path is not None:
            path_changed = False
            if len(self.prev_d_path) != len(self.current_d_path) + 1:
                path_changed = True
            else:
                for i in range(len(self.current_d_path)):
                    if self.prev_d_path[i+1] != self.current_d_path[i]:
                        path_changed = True
                        break

            if path_changed:
                self.prev_est_time = self.timer
                first_edge = True
                for edge in self.prev_d_path:
                    if first_edge:
                        first_edge = False
                        continue
                    self.prev_est_time += self.logics.get_time_for_crossing_edge(edge)

    def draw_car_on_edge(self, edge):
        if edge is None:
            return
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
        if d_edge_list is not None:
            n1, n2 = edge
            if (n1, n2) in d_edge_list:
                return n1, n2
            if (n2, n1) in d_edge_list:
                return n2, n1
        return None

    def draw_d_arrow(self, d_edge, color):
        start_pos = self.to_screen(self.positions[d_edge[0]])
        end_pos = self.to_screen(self.positions[d_edge[1]])
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
        self.draw_buttons()
        self.draw_timers()

        # Draw edges: color by traffic & mark current path
        for edge in self.edges:

            start_pos = self.to_screen(self.positions[edge[0]])
            end_pos = self.to_screen(self.positions[edge[1]])
            color = colors[edge]
            line_width = 2

            if self.edge_in_d_edge_list(edge, self.visited_edges):
                # color visited in green
                color = (0, 255, 0)

            d_edge = self.edge_in_d_edge_list(edge, current_d_path)
            if d_edge is not None:
                # mark current planned path to dest
                line_width = 5
                color = colors[edge]
                self.draw_d_arrow(d_edge, color)

            pygame.draw.line(self.screen, color,
                             start_pos, end_pos, line_width)

        # draw car on the current edge
        self.draw_car_on_edge(current_d_edge)
        self.visited_edges.add(current_d_edge)

        # Draw nodes: mark src & dist
        node_color = (50, 100, 200)  # Node color
        node_radius = 10  # Radius of nodes
        for node in self.graph.nodes():
            pos = self.positions[node]
            screen_pos = self.to_screen(pos)

            # Highlight src_node and dest_node with different colors or effects
            if node == self.src_node:
                pygame.draw.circle(self.screen, node_color, screen_pos, node_radius + 16, 3)
                self.draw_text("Starting Point", screen_pos, node_color)
                self.screen.blit(self.start_point_image, (screen_pos[0] - 17, screen_pos[1] - 17))

            elif node == self.dest_node:
                pygame.draw.circle(self.screen, node_color, screen_pos, node_radius + 16, 3)
                self.draw_text("Destination", screen_pos, node_color)
                self.screen.blit(self.end_point_image, (screen_pos[0] - 17, screen_pos[1] - 17))
            else:
                pygame.draw.circle(self.screen, node_color, screen_pos, node_radius)

        # Update the display
        pygame.display.flip()

    def to_screen(self, pos):
        """Convert position from graph layout (-1,1) range to screen coordinates."""
        x = int((pos[0] + 1) * (self.width - 200) / 2 + 100)  # Scale and center
        y = int((pos[1] + 1) * (self.height - 200) / 2 + 100)
        return x, y

    def draw_text(self, text, position, color):
        """Draw text labels near the nodes."""
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(text, True, color)  # Render text in black color
        text_rect = text_surface.get_rect(center=(position[0], position[1] - 40))  # Position text above the node
        self.screen.blit(text_surface, text_rect)  # Draw text on the screen

    def translate_traffic_into_color(self):
        colors = {}
        for edge in self.edges:
            traffic = self.logics.traffic_index[edge]
            colors[edge] = (traffic * 255, 0, 0)
        return colors

    def draw_buttons(self):
        button_color = (0, 128, 255)  # Blue color
        button_hover_color = (0, 200, 255)  # Lighter blue when hovered
        text_color = (255, 255, 255)  # White color
        font = pygame.font.SysFont(None, 36)

        self.next_button = pygame.Rect(10, 10, 80, 50)  # (x, y, width, height)
        self.show_prev_path_button = pygame.Rect(100, 10, 300, 50)
        self.restart_button = pygame.Rect(410, 10, 100, 50)
        self.quit_button = pygame.Rect(520, 10, 80, 50)

        # Check if the mouse is over the button
        mouse_pos = pygame.mouse.get_pos()
        if self.next_button.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, button_hover_color, self.next_button)
        else:
            pygame.draw.rect(self.screen, button_color, self.next_button)
        if self.show_prev_path_button.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, button_hover_color, self.show_prev_path_button)
        else:
            pygame.draw.rect(self.screen, button_color, self.show_prev_path_button)
        if self.restart_button.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, button_hover_color, self.restart_button)
        else:
            pygame.draw.rect(self.screen, button_color, self.restart_button)
        if self.quit_button.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, button_hover_color, self.quit_button)
        else:
            pygame.draw.rect(self.screen, button_color, self.quit_button)

        # Render the button text
        text = font.render("Next", True, text_color)
        self.screen.blit(text, (self.next_button.x + 10, self.next_button.y + 10))
        text = font.render("Show Previous Path", True, text_color)
        self.screen.blit(text, (self.show_prev_path_button.x + 10, self.show_prev_path_button.y + 10))
        text = font.render("Restart", True, text_color)
        self.screen.blit(text, (self.restart_button.x + 10, self.restart_button.y + 10))
        text = font.render("Quit", True, text_color)
        self.screen.blit(text, (self.quit_button.x + 10, self.quit_button.y + 10))

    def draw_timers(self):
        font = pygame.font.SysFont(None, 24)
        color = (0, 0, 0)

        # Render the current time text
        timer_text = f"Time: {round(self.timer * 60, 2)} minutes"
        timer_surface = font.render(timer_text, True, color)
        timer_rect = timer_surface.get_rect(topleft=(10, 550))  # Set 'topleft' to align left side
        self.screen.blit(timer_surface, timer_rect)

        # Render the estimated arrival time text
        if self.est_time is not None:
            est_timer_text = f"Estimated arrival time: {round(self.est_time * 60, 2)} minutes"
            if self.prev_est_time is not None:
                est_timer_text += f", instead of {round(self.prev_est_time * 60, 2)} minutes on the previous path"
                color = (255, 0, 0)
            est_timer_surface = font.render(est_timer_text, True, color)
            est_timer_rect = est_timer_surface.get_rect(topleft=(10, 580))  # Aligns with the same left position
            self.screen.blit(est_timer_surface, est_timer_rect)

    def run(self):
        # buttons
        next_pressed = False
        quit_pressed = False

        got_to_dest = False
        while not quit_pressed:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_pressed = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.next_button.collidepoint(event.pos):
                        next_pressed = True
                    elif self.show_prev_path_button.collidepoint(event.pos):
                        self.draw_graph(self.colors, self.prev_d_path, self.current_d_edge)
                        time.sleep(2)
                    elif self.quit_button.collidepoint(event.pos):
                        quit_pressed = True
                    elif self.restart_button.collidepoint(event.pos):
                        # restart logics
                        self.restart_game_logics()
                        got_to_dest = False
                        next_pressed = False

            if next_pressed and got_to_dest:
                self.update_timer()
                self.current_d_path = []
                self.current_d_edge = None

            if next_pressed and not got_to_dest:
                next_pressed = False
                self.update_timer()

                # update logics
                self.logics.update()

                # get edge colors
                self.colors = self.translate_traffic_into_color()

                # get current directed path
                self.prev_d_path = self.current_d_path
                self.current_d_path = self.logics.current_d_path

                # get current directed edge
                self.current_d_edge = None
                if len(self.current_d_path) > 0:
                    self.current_d_edge = self.current_d_path[0]
                    # check if got to dest
                    if self.current_d_edge[1] == self.dest_node:
                        got_to_dest = True

                # update timers
                self.update_estimated_time()

            self.draw_graph(self.colors, self.current_d_path, self.current_d_edge)

        pygame.quit()
        sys.exit()


# Example 1 usage
nodes = [1, 2, 3, 4, 5, 6, 7, 8]
edges = []
for i in range(len(nodes)):
    for j in range(len(nodes)):
        if i < j:
            edges.append((nodes[i], nodes[j]))

# # Example 2 usage
# nodes = [1, 2, 3, 4, 5, 6, 7, 8]
# edges = []
# pairs = [(1, 2), (1, 3), (1, 4), (4, 5), (4, 6), (4, 7), (4, 8)]
# for start, end in pairs:
#     edges.append((start, end))  # Edge from start to end
#     edges.append((end, start))  # Edge from end to start
#
# # Example 3 usage
# nodes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
# edges = []
# for i in range(len(nodes)):
#     for j in range(len(nodes)):
#         if i < j:
#             edges.append((nodes[i], nodes[j]))
#
# # Example 4 usage
# nodes = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# edges = []
# pairs = [
#     # Circle 1
#     (1, 2), (2, 3), (3, 1),  # Nodes 1, 2, 3 form a circle
#     # Circle 2
#     (4, 5), (5, 6), (6, 4),  # Nodes 4, 5, 6 form a circle
#     # Circle 3
#     (7, 8), (8, 9), (9, 7),  # Nodes 7, 8, 9 form a circle
#     # Optional connections between circles
#     (3, 4),  # Connecting Circle 1 to Circle 2
#     (6, 7)   # Connecting Circle 2 to Circle 3
# ]
# for start, end in pairs:
#     edges.append((start, end))  # Edge from start to end
#     edges.append((end, start))  # Edge from end to start
# visualizer = NavigationManager(nodes, edges, 1, 8)

# Create a GraphVisualizer object and run it
visualizer = NavigationManager(nodes, edges, 1, 3)
visualizer.run()
