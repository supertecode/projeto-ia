import pygame

# Inicialização do pygame
pygame.init()

# Definições de tela
screen = pygame.display.set_mode((400, 400))

# Classe PacMan
class PacMan:
    def __init__(self):
        self.x = 1  # Posição inicial x
        self.y = 1  # Posição inicial y
        self.color = (255, 255, 0)  # Cor do PacMan

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x * 20, self.y * 20), 10)

# Função para lidar com a entrada do usuário
def handle_input(pacman):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pacman.move(0, -1)  # Mover para cima
                print("cima")
            elif event.key == pygame.K_DOWN:
                pacman.move(0, 1)  # Mover para baixo
                print("baixo")
            elif event.key == pygame.K_LEFT:
                pacman.move(-1, 0)  # Mover para a esquerda
                print("esquerda")
            elif event.key == pygame.K_RIGHT:
                pacman.move(1, 0)  # Mover para a direita
                print("direita")
    return True

# Criação da instância do PacMan
pacman = PacMan()

# Loop principal
running = True
while running:
    running = handle_input(pacman)  # Chama a função de manipulação de entrada

    # Limpa a tela
    screen.fill((0, 0, 0))
    
    # Desenha o PacMan
    pacman.draw(screen)

    # Atualiza a tela
    pygame.display.flip()

# Encerramento do pygame
pygame.quit()
