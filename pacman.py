import pygame

class PacMan:
    def __init__(self):
        self.x, self.y = 1, 1  # Posição inicial
        self.direction = (0, 0)

    def move(self, maze):
        # Aqui, você implementa a lógica para verificar se a próxima célula é livre.
        new_x = self.x + self.direction[0]
        new_y = self.y + self.direction[1]
        if maze.is_path(new_x, new_y):
            self.x, self.y = new_x, new_y

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (self.x * 20, self.y * 20), 10)

    def handle_input(self, event):
        # Muda a direção com base na entrada do jogador
        if event.key == pygame.K_UP:
            self.direction = (0, -1)
        elif event.key == pygame.K_DOWN:
            self.direction = (0, 1)
        elif event.key == pygame.K_LEFT:
            self.direction = (-1, 0)
        elif event.key == pygame.K_RIGHT:
            self.direction = (1, 0)
