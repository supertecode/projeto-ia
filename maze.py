import pygame

class Maze:
    def __init__(self, level):
        self.grid = self.load_maze(level)

    def load_maze(self, level):
        # Carrega o labirinto de um arquivo ou define diretamente no código
        if level == 1:
            return [[1, 1, 1, 1], [1, 0, 0, 1], [1, 1, 1, 1]]
        # Adicione mais labirintos para níveis diferentes

    def is_path(self, x, y):
        return self.grid[y][x] == 0

    def draw(self, screen):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == 1:
                    pygame.draw.rect(screen, (50, 50, 50), (x * 20, y * 20, 20, 20))
