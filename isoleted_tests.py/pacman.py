import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 30
WALL_SIZE = CELL_SIZE
# Define maze dimensions
MAZE_WIDTH = 19
MAZE_HEIGHT = 21
# Calculate screen dimensions based on maze size
SCREEN_WIDTH = MAZE_WIDTH * CELL_SIZE
SCREEN_HEIGHT = MAZE_HEIGHT * CELL_SIZE

PACMAN_SPEED = 2
GHOST_SPEED = 2
DOT_SIZE = 4

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()

# Define the maze layout
# 0 = empty path
# 1 = wall
# 2 = dot
# 3 = power pellet
MAZE_LAYOUT = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,1],
    [1,3,1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,3,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,2,1,2,1,1,1,1,1,2,1,2,1,1,2,1],
    [1,2,2,2,2,1,2,2,2,1,2,2,2,1,2,2,2,2,1],
    [1,1,1,1,2,1,1,1,0,1,0,1,1,1,2,1,1,1,1],
    [1,1,1,1,2,1,0,0,0,0,0,0,0,1,2,1,1,1,1],
    [1,1,1,1,2,1,0,1,1,0,1,1,0,1,2,1,1,1,1],
    [0,0,0,0,2,0,0,1,0,0,0,1,0,0,2,0,0,0,0],
    [1,1,1,1,2,1,0,1,1,1,1,1,0,1,2,1,1,1,1],
    [1,1,1,1,2,1,0,0,0,0,0,0,0,1,2,1,1,1,1],
    [1,1,1,1,2,1,0,1,1,1,1,1,0,1,2,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,2,1],
    [1,3,2,1,2,2,2,2,2,2,2,2,2,2,2,1,2,3,1],
    [1,1,2,1,2,1,2,1,1,1,1,1,2,1,2,1,2,1,1],
    [1,2,2,2,2,1,2,2,2,1,2,2,2,1,2,2,2,2,1],
    [1,2,1,1,1,1,1,1,2,1,2,1,1,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

class PacMan:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.grid_x = x // CELL_SIZE
        self.grid_y = y // CELL_SIZE
        self.direction = 0  # 0: right, 1: left, 2: up, 3: down
        self.next_direction = None
        self.mouth_open = True
        self.animation_counter = 0
        self.speed = PACMAN_SPEED
        self.radius = CELL_SIZE // 2 - 2
        
    def can_move(self, dx, dy):
        next_x = (self.x + dx * self.speed) // CELL_SIZE
        next_y = (self.y + dy * self.speed) // CELL_SIZE
        
        # Check if the next position is within bounds
        if next_x < 0 or next_x >= MAZE_WIDTH or next_y < 0 or next_y >= MAZE_HEIGHT:
            return False
            
        # Check if the next position is a wall
        return MAZE_LAYOUT[next_y][next_x] != 1

    def move(self):
        keys = pygame.key.get_pressed()
        # Store the next direction based on key press
        if keys[pygame.K_RIGHT]:
            self.next_direction = 0
        elif keys[pygame.K_LEFT]:
            self.next_direction = 1
        elif keys[pygame.K_UP]:
            self.next_direction = 2
        elif keys[pygame.K_DOWN]:
            self.next_direction = 3

        # Try to change to the next direction if it's possible
        if self.next_direction is not None:
            can_change = False
            if self.next_direction == 0 and self.can_move(1, 0):  # Right
                self.direction = 0
                can_change = True
            elif self.next_direction == 1 and self.can_move(-1, 0):  # Left
                self.direction = 1
                can_change = True
            elif self.next_direction == 2 and self.can_move(0, -1):  # Up
                self.direction = 2
                can_change = True
            elif self.next_direction == 3 and self.can_move(0, 1):  # Down
                self.direction = 3
                can_change = True
                
            if can_change:
                self.next_direction = None

        # Move in the current direction if possible
        if self.direction == 0 and self.can_move(1, 0):  # Right
            self.x += self.speed
        elif self.direction == 1 and self.can_move(-1, 0):  # Left
            self.x -= self.speed
        elif self.direction == 2 and self.can_move(0, -1):  # Up
            self.y -= self.speed
        elif self.direction == 3 and self.can_move(0, 1):  # Down
            self.y += self.speed

        # Handle tunnel
        if self.x < 0:
            self.x = SCREEN_WIDTH - CELL_SIZE
        elif self.x >= SCREEN_WIDTH:
            self.x = 0

        # Update grid position
        self.grid_x = self.x // CELL_SIZE
        self.grid_y = self.y // CELL_SIZE
            
        # Animation
        self.animation_counter += 1
        if self.animation_counter >= 10:
            self.mouth_open = not self.mouth_open
            self.animation_counter = 0
    
    def draw(self):
        # Draw Pac-Man body
        pygame.draw.circle(screen, YELLOW, (int(self.x + CELL_SIZE//2), int(self.y + CELL_SIZE//2)), self.radius)
        
        # Draw mouth
        if self.mouth_open:
            if self.direction == 0:  # Right
                start_angle = math.radians(30)
                end_angle = math.radians(330)
            elif self.direction == 1:  # Left
                start_angle = math.radians(210)
                end_angle = math.radians(150)
            elif self.direction == 2:  # Up
                start_angle = math.radians(120)
                end_angle = math.radians(60)
            else:  # Down
                start_angle = math.radians(300)
                end_angle = math.radians(240)
            
            center_x = self.x + CELL_SIZE//2
            center_y = self.y + CELL_SIZE//2
            
            pygame.draw.polygon(screen, BLACK, [
                (center_x, center_y),
                (center_x + math.cos(start_angle) * self.radius,
                 center_y - math.sin(start_angle) * self.radius),
                (center_x + math.cos(end_angle) * self.radius,
                 center_y - math.sin(end_angle) * self.radius)
            ])

class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.grid_x = x // CELL_SIZE
        self.grid_y = y // CELL_SIZE
        self.color = color
        self.direction = random.randint(0, 3)
        self.speed = GHOST_SPEED
        self.radius = CELL_SIZE // 2 - 2
        
    def can_move(self, dx, dy):
        next_x = (self.x + dx * self.speed) // CELL_SIZE
        next_y = (self.y + dy * self.speed) // CELL_SIZE
        
        if next_x < 0 or next_x >= MAZE_WIDTH or next_y < 0 or next_y >= MAZE_HEIGHT:
            return False
            
        return MAZE_LAYOUT[next_y][next_x] != 1

    def move(self, pacman):
        # Simple ghost AI - try to move toward Pac-Man while respecting walls
        possible_directions = []
        if self.can_move(1, 0):  # Right
            possible_directions.append(0)
        if self.can_move(-1, 0):  # Left
            possible_directions.append(1)
        if self.can_move(0, -1):  # Up
            possible_directions.append(2)
        if self.can_move(0, 1):  # Down
            possible_directions.append(3)
            
        if possible_directions:
            if random.random() < 0.2:  # Sometimes move randomly
                self.direction = random.choice(possible_directions)
            else:  # Otherwise try to move toward Pac-Man
                distances = []
                for d in possible_directions:
                    if d == 0:  # Right
                        next_x = self.x + CELL_SIZE
                        next_y = self.y
                    elif d == 1:  # Left
                        next_x = self.x - CELL_SIZE
                        next_y = self.y
                    elif d == 2:  # Up
                        next_x = self.x
                        next_y = self.y - CELL_SIZE
                    else:  # Down
                        next_x = self.x
                        next_y = self.y + CELL_SIZE
                        
                    dist = math.sqrt((next_x - pacman.x)**2 + (next_y - pacman.y)**2)
                    distances.append(dist)
                    
                self.direction = possible_directions[distances.index(min(distances))]

        # Move in the chosen direction
        if self.direction == 0 and self.can_move(1, 0):  # Right
            self.x += self.speed
        elif self.direction == 1 and self.can_move(-1, 0):  # Left
            self.x -= self.speed
        elif self.direction == 2 and self.can_move(0, -1):  # Up
            self.y -= self.speed
        elif self.direction == 3 and self.can_move(0, 1):  # Down
            self.y += self.speed

        # Handle tunnel
        if self.x < 0:
            self.x = SCREEN_WIDTH - CELL_SIZE
        elif self.x >= SCREEN_WIDTH:
            self.x = 0

        # Update grid position
        self.grid_x = self.x // CELL_SIZE
        self.grid_y = self.y // CELL_SIZE
    
    def draw(self):
        center_x = self.x + CELL_SIZE//2
        center_y = self.y + CELL_SIZE//2
        
        # Draw ghost body
        pygame.draw.circle(screen, self.color, (int(center_x), int(center_y)), self.radius)
        # Draw rectangle bottom
        pygame.draw.rect(screen, self.color, 
                        (center_x - self.radius, center_y, 
                         self.radius * 2, self.radius))

def draw_maze():
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            cell = MAZE_LAYOUT[y][x]
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, WALL_SIZE, WALL_SIZE)
            
            if cell == 1:  # Wall
                pygame.draw.rect(screen, BLUE, rect)
            elif cell == 2:  # Dot
                pygame.draw.circle(screen, WHITE,
                                 (x * CELL_SIZE + CELL_SIZE//2,
                                  y * CELL_SIZE + CELL_SIZE//2),
                                 DOT_SIZE)
            elif cell == 3:  # Power pellet
                pygame.draw.circle(screen, WHITE,
                                 (x * CELL_SIZE + CELL_SIZE//2,
                                  y * CELL_SIZE + CELL_SIZE//2),
                                 DOT_SIZE * 2)

def check_collision(x1, y1, x2, y2, tolerance=CELL_SIZE-10):
    distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return distance < tolerance

def main():
    # Create game objects
    # Place Pac-Man in a valid starting position
    pacman = PacMan(9 * CELL_SIZE, 15 * CELL_SIZE)
    
    # Place ghosts in the center area
    ghosts = [
        Ghost(7 * CELL_SIZE, 8 * CELL_SIZE, RED),
        Ghost(8 * CELL_SIZE, 8 * CELL_SIZE, (255, 192, 203)),  # Pink
        Ghost(10 * CELL_SIZE, 8 * CELL_SIZE, (0, 255, 255)),   # Cyan
        Ghost(11 * CELL_SIZE, 8 * CELL_SIZE, (255, 165, 0))    # Orange
    ]
    
    score = 0
    game_over = False
    running = True
    
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_SPACE:
                    # Reset game
                    pacman = PacMan(9 * CELL_SIZE, 15 * CELL_SIZE)
                    ghosts = [
                        Ghost(7 * CELL_SIZE, 8 * CELL_SIZE, RED),
                        Ghost(8 * CELL_SIZE, 8 * CELL_SIZE, (255, 192, 203)),
                        Ghost(10 * CELL_SIZE, 8 * CELL_SIZE, (0, 255, 255)),
                        Ghost(11 * CELL_SIZE, 8 * CELL_SIZE, (255, 165, 0))
                    ]
                    # Reset maze dots
                    for y in range(MAZE_HEIGHT):
                        for x in range(MAZE_WIDTH):
                            if MAZE_LAYOUT[y][x] == 0:
                                MAZE_LAYOUT[y][x] = 2
                    score = 0
                    game_over = False
        
        if not game_over:
            # Update game state
            pacman.move()
            
            # Check for dot collection
            if MAZE_LAYOUT[pacman.grid_y][pacman.grid_x] == 2:  # Regular dot
                MAZE_LAYOUT[pacman.grid_y][pacman.grid_x] = 0
                score += 10
            elif MAZE_LAYOUT[pacman.grid_y][pacman.grid_x] == 3:  # Power pellet
                MAZE_LAYOUT[pacman.grid_y][pacman.grid_x] = 0
                score += 50
            
            # Move ghosts
            for ghost in ghosts:
                ghost.move(pacman)
                # Check collision with ghosts
                if check_collision(pacman.x + CELL_SIZE//2, pacman.y + CELL_SIZE//2, 
                                 ghost.x + CELL_SIZE//2, ghost.y + CELL_SIZE//2):
                    game_over = True
            
            # Check win condition
            dots_remaining = False
            for y in range(MAZE_HEIGHT):
                for x in range(MAZE_WIDTH):
                    if MAZE_LAYOUT[y][x] in [2, 3]:
                        dots_remaining = True
                        break
                if dots_remaining:
                    break
            
            if not dots_remaining:
                game_over = True
        
        # Drawing
        screen.fill(BLACK)
        
        # Draw maze
        draw_maze()
        
        # Draw Pac-Man and ghosts
        pacman.draw()
        for ghost in ghosts:
            ghost.draw()
        
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))
        
        if game_over:
            # Check if player won
            won = not any(MAZE_LAYOUT[y][x] in [2, 3] for y in range(MAZE_HEIGHT) for x in range(MAZE_WIDTH))
            message = 'You Win!' if won else 'Game Over!'
            game_over_text = font.render(f'{message} Press SPACE to restart', True, WHITE)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(game_over_text, text_rect)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()