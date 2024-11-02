import pygame
from search_algorithms import greedy_search, a_star

class Ghost:
    def __init__(self, name):
        self.name = name
        self.x, self.y = 5, 5  # Posição inicial
        self.color = (255, 0, 0) if name == "blinky" else (0, 0, 255)

    def move(self, pacman, maze):
        if self.name == "blinky":
            # Blinky usa o algoritmo A*
            self.x, self.y = a_star((self.x, self.y), (pacman.x, pacman.y), maze)
        else:
            # Outros usam busca gulosa
            self.x, self.y = greedy_search((self.x, self.y), (pacman.x, pacman.y), maze)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x * 20, self.y * 20), 10)
