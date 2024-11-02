import pygame
from pacman import PacMan
from ghost import Ghost
from maze import Maze

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.pacman = PacMan()          # Inicializa o Pac-Man
        self.ghosts = [Ghost("blinky"), Ghost("pinky"), Ghost("inky"), Ghost("clyde")]
        self.maze = Maze(level=1)       # Inicializa o labirinto do primeiro nível

    def run(self):
        running = True
        while running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(5)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                self.pacman.handle_input(event)
               

    def update(self):
        self.pacman.move(self.maze)     # Move o Pac-Man baseado no input do jogador
        for ghost in self.ghosts:
            ghost.move(self.pacman, self.maze)  # Move cada fantasma usando IA

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.maze.draw(self.screen)     # Desenha o labirinto
        self.pacman.draw(self.screen)   # Desenha o Pac-Man
        for ghost in self.ghosts:
            ghost.draw(self.screen)     # Desenha cada fantasma
        pygame.display.flip()
