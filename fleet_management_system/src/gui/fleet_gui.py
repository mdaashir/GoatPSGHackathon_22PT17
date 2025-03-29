import pygame
from fleet_management_system.src.models.nav_graph import NavGraph
from fleet_management_system.src.models.robot import Robot

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class FleetGUI:
    def __init__(self, json_path):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Fleet Management System")
        self.graph = NavGraph(json_path)
        self.robots = [Robot(1, 0, self.graph)]

        # Get min and max values for proper scaling
        x_vals = [coord[0] for coord in self.graph.vertices.values()]
        y_vals = [coord[1] for coord in self.graph.vertices.values()]

        self.min_x, self.max_x = min(x_vals), max(x_vals)
        self.min_y, self.max_y = min(y_vals), max(y_vals)

        # Compute scaling factor to fit within window size
        self.scale_x = WIDTH / (self.max_x - self.min_x + 1)
        self.scale_y = HEIGHT / (self.max_y - self.min_y + 1)
        self.scale = min(self.scale_x, self.scale_y) * 0.8  # Keep some margin

        # Centering offset
        self.offset_x = (WIDTH - (self.max_x - self.min_x) * self.scale) / 2
        self.offset_y = (HEIGHT - (self.max_y - self.min_y) * self.scale) / 2

    def transform_coords(self, x, y):
        """ Convert world coordinates to screen coordinates """
        screen_x = (x - self.min_x) * self.scale + self.offset_x
        screen_y = HEIGHT - ((y - self.min_y) * self.scale + self.offset_y)  # Flip Y-axis
        return int(screen_x), int(screen_y)

    def draw_graph(self):
        for start, neighbors in self.graph.edges.items():
            x1, y1 = self.transform_coords(*self.graph.vertices[start])
            for end in neighbors:
                x2, y2 = self.transform_coords(*self.graph.vertices[end])
                pygame.draw.line(self.screen, BLACK, (x1, y1), (x2, y2), 2)

        for node, (x, y) in self.graph.vertices.items():
            pygame.draw.circle(self.screen, GREEN, self.transform_coords(x, y), 8)

    def draw_robots(self):
        for robot in self.robots:
            x, y = self.transform_coords(*self.graph.vertices[robot.current_position])
            color = RED if robot.status == "waiting" else GREEN
            pygame.draw.circle(self.screen, color, (x, y), 10)

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            self.screen.fill(WHITE)
            self.draw_graph()
            self.draw_robots()

            pygame.display.flip()
            clock.tick(30)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    for v, pos in self.graph.vertices.items():
                        if abs(pos[0] - x) < 10 and abs(pos[1] - y) < 10:
                            self.robots.append(Robot(v))

        pygame.quit()
