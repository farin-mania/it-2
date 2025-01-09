import pygame
import sys


class TetrominoPolygon:
    def __init__(self, shape_type, x, y, cell_size=30):
        self.x = x
        self.y = y
        self.cell_size = cell_size

        # Define shapes using vertices in a clockwise direction
        # Each vertex is relative to the top-left corner (x, y)
        self.SHAPES = {
            "I": [
                (0, 0),
                (self.cell_size, 0),
                (self.cell_size, self.cell_size * 4),
                (0, self.cell_size * 4),
            ],
            "O": [
                (0, 0),
                (self.cell_size * 2, 0),
                (self.cell_size * 2, self.cell_size * 2),
                (0, self.cell_size * 2),
            ],
            "T": [
                (0, self.cell_size),
                (self.cell_size, self.cell_size),
                (self.cell_size, 0),
                (self.cell_size * 2, 0),
                (self.cell_size * 2, self.cell_size),
                (self.cell_size * 3, self.cell_size),
                (self.cell_size * 3, self.cell_size * 2),
                (0, self.cell_size * 2),
            ],
            "S": [
                (self.cell_size, 0),
                (self.cell_size * 3, 0),
                (self.cell_size * 3, self.cell_size),
                (self.cell_size * 2, self.cell_size),
                (self.cell_size * 2, self.cell_size * 2),
                (0, self.cell_size * 2),
                (0, self.cell_size),
                (self.cell_size, self.cell_size),
            ],
            "Z": [
                (0, 0),
                (self.cell_size * 2, 0),
                (self.cell_size * 2, self.cell_size),
                (self.cell_size * 3, self.cell_size),
                (self.cell_size * 3, self.cell_size * 2),
                (self.cell_size, self.cell_size * 2),
                (self.cell_size, self.cell_size),
                (0, self.cell_size),
            ],
            "J": [
                (self.cell_size, 0),
                (self.cell_size * 2, 0),
                (self.cell_size * 2, self.cell_size * 3),
                (0, self.cell_size * 3),
                (0, self.cell_size * 2),
                (self.cell_size, self.cell_size * 2),
                (self.cell_size, 0),
            ],
            "L": [
                (0, 0),
                (self.cell_size, 0),
                (self.cell_size, self.cell_size * 2),
                (self.cell_size * 2, self.cell_size * 2),
                (self.cell_size * 2, self.cell_size * 3),
                (0, self.cell_size * 3),
            ],
        }

        self.color = {
            "I": (0, 255, 255),  # Cyan
            "O": (255, 255, 0),  # Yellow
            "T": (128, 0, 128),  # Purple
            "S": (255, 0, 0),  # Red
            "Z": (0, 255, 0),  # Green
            "J": (255, 192, 203),  # Pink
            "L": (255, 165, 0),  # Orange
        }[shape_type]

        self.vertices = self.SHAPES[shape_type]

    def draw(self, surface):
        # Offset vertices by the piece's position
        positioned_vertices = [(self.x + x, self.y + y) for x, y in self.vertices]

        # Draw the filled polygon
        pygame.draw.polygon(surface, self.color, positioned_vertices)
        # Draw the border
        pygame.draw.polygon(surface, (0, 0, 0), positioned_vertices, 2)


def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 600))
    pygame.display.set_caption("Tetris Shapes as Polygons")

    # Create instances of different shapes
    shapes = [
        TetrominoPolygon("I", 50, 50),
        TetrominoPolygon("O", 150, 50),
        TetrominoPolygon("T", 250, 50),
        TetrominoPolygon("S", 50, 200),
        TetrominoPolygon("Z", 150, 200),
        TetrominoPolygon("J", 250, 200),
        TetrominoPolygon("L", 50, 350),
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))  # White background

        # Draw all shapes
        for shape in shapes:
            shape.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
