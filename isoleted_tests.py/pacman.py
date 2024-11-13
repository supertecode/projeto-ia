import pygame
import random
import heapq
from typing import List, Tuple, Set
import math
import tkinter as tk
from tkinter import font

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 30
WALL_SIZE = CELL_SIZE
# Define maze dimensions
MAZE_WIDTH = 19
MAZE_HEIGHT = 22
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
    [1,1,1,1,2,1,0,1,0,0,0,1,0,1,2,1,1,1,1],
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

MAZE_LAYOUT_2 = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,1,1,1,1,1,2,2,2,2,2,2,1],
    [1,2,1,1,2,1,2,1,2,2,2,1,2,1,2,1,1,2,1],
    [1,2,1,1,2,1,2,1,3,1,3,1,2,1,2,1,1,2,1],
    [1,2,2,2,2,1,2,2,2,1,2,2,2,1,2,2,2,2,1],
    [1,1,1,1,2,1,1,1,1,1,1,1,2,1,1,1,1,1,1],
    [1,1,1,1,2,1,0,0,0,1,0,0,0,1,2,1,1,1,1],
    [1,1,1,1,2,1,0,1,1,0,1,1,0,1,2,1,1,1,1],
    [1,1,1,1,2,1,0,1,3,0,3,1,0,1,2,1,1,1,1],
    [0,0,0,0,2,0,0,0,0,0,0,0,0,0,2,0,0,0,0],
    [1,1,1,1,2,1,0,1,1,1,1,1,0,1,2,1,1,1,1],
    [1,1,1,1,2,1,0,1,2,2,2,1,0,1,2,1,1,1,1],
    [1,1,1,1,2,1,0,1,1,1,1,1,0,1,2,1,1,1,1],
    [1,2,2,2,2,2,2,1,1,1,1,1,2,2,2,2,2,2,1],
    [1,2,1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,2,1],
    [1,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,1],
    [1,2,2,2,2,1,1,1,1,1,1,1,1,1,2,2,2,2,1],
    [1,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

MAZE_LAYOUT_3 = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,2,1,2,1,2,1,1,1,1,2,1],
    [1,3,1,1,1,1,2,1,3,1,3,1,2,1,1,1,1,3,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,1,1,1,2,1,1,1,1,1,1,1,1,1,2,1,1,1,1],
    [1,1,1,1,2,1,0,0,0,1,0,0,0,1,2,1,1,1,1],
    [1,1,1,1,2,1,0,1,1,1,1,1,0,1,2,1,1,1,1],
    [1,1,1,1,2,1,0,1,0,0,0,1,0,1,2,1,1,1,1],
    [1,1,1,1,2,1,0,1,0,1,0,1,0,1,2,1,1,1,1],
    [0,0,0,0,2,0,0,1,0,0,0,1,0,0,2,0,0,0,0],
    [1,1,1,1,2,1,0,1,1,1,1,1,0,1,2,1,1,1,1],
    [1,2,2,2,2,1,0,0,0,0,0,0,0,1,2,2,2,2,1],
    [1,2,1,1,2,1,0,1,1,1,1,1,0,1,2,1,1,2,1],
    [1,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,1,1,2,1,2,1,1,1,1,1,1,2,1],
    [1,2,1,1,1,1,1,1,2,1,2,1,1,1,1,1,1,2,1],
    [1,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,1],
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
    # Convert direction to number (0=right, 1=left, 2=up, 3=down)
        if dx > 0: direction = 0
        elif dx < 0: direction = 1
        elif dy < 0: direction = 2
        else: direction = 3
    
        return not check_wall_collision(self.x, self.y, direction, self.speed, CELL_SIZE)

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

        # Túnel da esquerda e direita
        if self.x < 0:
            self.x = SCREEN_WIDTH - CELL_SIZE
        elif self.x >= SCREEN_WIDTH:
            self.x = 0

        # Update grid position
        center_x = self.x + CELL_SIZE//2
        center_y = self.y + CELL_SIZE//2
        self.grid_x = center_x // CELL_SIZE
        self.grid_y = center_y // CELL_SIZE
        
        print('POSIÇÃO DO PACMAN: ',self.grid_x, self.grid_y)
            
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

    def manhattan_distance(self, x1: int, y1: int, x2: int, y2: int) -> int:
        """Calculate Manhattan distance between two points."""
        return abs(x1 - x2) + abs(y1 - y2)

    def get_valid_neighbors(self, x: int, y: int, maze):
        """Get valid neighboring cells (not walls)."""
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # up, down, left, right
        neighbors = []
        
        for dx, dy in directions:
            new_x = x + dx
            new_y = y + dy
            
            # Handle tunnel wrap-around
            if new_x < 0:
                new_x = len(maze[0]) - 1
            elif new_x >= len(maze[0]):
                new_x = 0

            # checkCollision = check_wall_collision(self.x, self.y, self.direction, self.speed, CELL_SIZE)
            # Check if the position is valid and not a wall
            # if(checkCollision):
            #     print('COLISAO')
            # else:
            #     print('SEMCOLISAO')
            #     neighbors.append((new_x, new_y))
                
            if (maze[new_y][new_x] != 1):  # Assuming 1 represents walls
                neighbors.append((new_x, new_y))
                print(neighbors)
                
        return neighbors

    def find_next_move(self, maze, pacman_x: int, pacman_y: int):
        """
        Find the next best move using Greedy Best-First Search.
        Returns the next grid position (x, y).
        """
        # Priority queue for Greedy Best-First Search
        # Format: (priority, (x, y))
        pq = [(0, (self.grid_x, self.grid_y))]
        visited = set()
        
        # Keep track of where we came from to reconstruct the path
        came_from = {}
        
        while pq:
            _, current = heapq.heappop(pq)
            
            if current in visited:
                continue
                
            visited.add(current)
            
            # If we found Pacman's position, reconstruct the path
            if current == (pacman_x, pacman_y):
                break
                
            # Check all valid neighbors
            for next_pos in self.get_valid_neighbors(current[0], current[1], maze):
                if next_pos not in visited:
                    # Calculate priority using Manhattan distance
                    priority = self.manhattan_distance(next_pos[0], next_pos[1], 
                                                    pacman_x, pacman_y)
                    heapq.heappush(pq, (priority, next_pos))
                    came_from[next_pos] = current

        # If we can't find a path to Pacman, return current position
        if not came_from:
            return (self.grid_x, self.grid_y)

        # Reconstruct the path
        current = (pacman_x, pacman_y)
        path = []
        
        while current in came_from:
            path.append(current)
            current = came_from[current]
            
        # Return the next position in the path
        # If path is empty, stay in current position
        if path:
            return path[-1]  # The next step towards Pacman
        return (self.grid_x, self.grid_y)

    def update(self, maze, pacman_x: int, pacman_y: int):
        """Update ghost position using Greedy Best-First Search."""
        # Convert Pacman's pixel coordinates to grid coordinates
        target_grid_x = pacman_x // CELL_SIZE
        target_grid_y = pacman_y // CELL_SIZE
        
        # Find next move
        next_x, next_y = self.find_next_move(maze, target_grid_x, target_grid_y)
        
        # Calculate direction to move
        dx = next_x - self.grid_x
        dy = next_y - self.grid_y
        
        # Update position based on direction
        if dx > 1:  # Wrap around left
            self.x -= self.speed
        elif dx < -1:  # Wrap around right
            self.x += self.speed
        else:
            self.x += dx * self.speed
            
        self.y += dy * self.speed
        
        # Handle tunnel wrap-around
        if self.x < 0:
            self.x = SCREEN_WIDTH - CELL_SIZE
        elif self.x >= SCREEN_WIDTH:
            self.x = 0

        print('POSIÇÃO DO FANTASMA: ',self.grid_x, self.grid_y)
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

# def check_collision(x1, y1, x2, y2, tolerance=CELL_SIZE-10):
#     distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
#     return distance < tolerance
def check_wall_collision(x, y, direction, speed, cell_size):
    """
    Check if moving in the given direction would result in a wall collision.
    Returns True if there's a collision, False otherwise.
    
    Args:
        x, y: Current position in pixels
        direction: 0=right, 1=left, 2=up, 3=down
        speed: Movement speed in pixels
        cell_size: Size of each maze cell in pixels
    """
    # Calculate the corners of the entity (Pac-Man or ghost)
    left = x
    right = x + cell_size - 1
    top = y
    bottom = y + cell_size - 1
    
    # Add some tolerance to make movement smoother
    tolerance = 5
    
    if direction == 0:  # Right
        # Check right side
        next_x = right + speed
        cell_x = next_x // cell_size
        top_cell_y = (top + tolerance) // cell_size
        bottom_cell_y = (bottom - tolerance) // cell_size
        
        for cell_y in range(top_cell_y, bottom_cell_y + 1):
            if cell_y >= 0 and cell_y < len(MAZE_LAYOUT) and cell_x < len(MAZE_LAYOUT[0]):
                if MAZE_LAYOUT[cell_y][cell_x] == 1:
                    return True
                    
    elif direction == 1:  # Left
        # Check left side
        next_x = left - speed
        cell_x = next_x // cell_size
        top_cell_y = (top + tolerance) // cell_size
        bottom_cell_y = (bottom - tolerance) // cell_size
        
        for cell_y in range(top_cell_y, bottom_cell_y + 1):
            if cell_y >= 0 and cell_y < len(MAZE_LAYOUT) and cell_x >= 0:
                if MAZE_LAYOUT[cell_y][cell_x] == 1:
                    return True
                    
    elif direction == 2:  # Up
        # Check top side
        next_y = top - speed
        cell_y = next_y // cell_size
        left_cell_x = (left + tolerance) // cell_size
        right_cell_x = (right - tolerance) // cell_size
        
        for cell_x in range(left_cell_x, right_cell_x + 1):
            if cell_y >= 0 and cell_x >= 0 and cell_x < len(MAZE_LAYOUT[0]):
                if MAZE_LAYOUT[cell_y][cell_x] == 1:
                    return True
                    
    else:  # Down
        # Check bottom side
        next_y = bottom + speed
        cell_y = next_y // cell_size
        left_cell_x = (left + tolerance) // cell_size
        right_cell_x = (right - tolerance) // cell_size
        
        for cell_x in range(left_cell_x, right_cell_x + 1):
            if cell_y < len(MAZE_LAYOUT) and cell_x >= 0 and cell_x < len(MAZE_LAYOUT[0]):
                if MAZE_LAYOUT[cell_y][cell_x] == 1:
                    return True
    
    return False

def check_entity_collision(x1, y1, x2, y2, cell_size):
    """
    Check for collision between two entities (Pac-Man and ghosts).
    Returns True if there's a collision, False otherwise.
    
    Args:
        x1, y1: Position of first entity in pixels
        x2, y2: Position of second entity in pixels
        cell_size: Size of each maze cell in pixels
    """
    # Use center points for more accurate collision detection
    center1_x = x1 + cell_size // 2
    center1_y = y1 + cell_size // 2
    center2_x = x2 + cell_size // 2
    center2_y = y2 + cell_size // 2
    
    # Calculate distance between centers
    distance = math.sqrt((center1_x - center2_x) ** 2 + (center1_y - center2_y) ** 2)
    
    # Collision occurs if distance is less than 3/4 of a cell size
    collision_threshold = cell_size * 0.75
    return distance < collision_threshold

def center_window(window, width, height):
    # Get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # Calculate position coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    
    # Set the window position
    window.geometry('%dx%d+%d+%d' % (width, height, x, y))

# Function to handle button clicks
def set_level(level):
    global level_var
    level_var.set(level)
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("Pac-man")

# Set window properties
window_width = 300
window_height = 400
center_window(root, window_width, window_height)  # Center the window
root.configure(bg="#000000")  # Set background color to black

# Optional: Prevent window resizing
root.resizable(False, False)

# Set custom font
custom_font = font.Font(family="Helvetica", size=16, weight="bold")
title_font = font.Font(family="Helvetica", size=20, weight="bold")
select_level = font.Font(family="Helvetica", size=18, weight="bold")

# Create a variable to store the selected level
level_var = tk.IntVar()

# Create the title
title_label = tk.Label(root, text="Pac-man", font=title_font, fg="#ffff00", bg="#000000")
title_label.pack(pady=20)
select_lebel = tk.Label(root, text="Selecione a fase", font=select_level, fg="#ffff00", bg="#000000" )
select_lebel.pack(pady = 18)

# Create the buttons
button_frame = tk.Frame(root, bg="#000000")
button_frame.pack(pady=20)

tk.Button(button_frame, text="1", command=lambda: set_level(1), font=custom_font, fg="#ffff00", bg="#000000", relief=tk.FLAT, padx=20, pady=10).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="2", command=lambda: set_level(2), font=custom_font, fg="#ffff00", bg="#000000", relief=tk.FLAT, padx=20, pady=10).grid(row=0, column=1, padx=10)
tk.Button(button_frame, text="3", command=lambda: set_level(3), font=custom_font, fg="#ffff00", bg="#000000", relief=tk.FLAT, padx=20, pady=10).grid(row=0, column=2, padx=10)
tk.Button(button_frame, text="Quit", command=root.destroy, font=custom_font, fg="#ffff00", bg="#000000", relief=tk.FLAT, padx=20, pady=10).grid(row=1, column=1, padx=10, pady=10)

# Run the main loop
root.mainloop()

# Print the selected level
print(f"Selected level: {level_var.get()}")

if level_var.get() == 0:
    quit()
    exit()

def main():
    # Create game objects
    # Place Pac-Man in a valid starting position
    pacman = PacMan(9 * CELL_SIZE, 15 * CELL_SIZE)
    
    # Place ghosts in the center area
    ghosts = [
        Ghost(9 * CELL_SIZE, 8 * CELL_SIZE, RED),
        # Ghost(8 * CELL_SIZE, 8 * CELL_SIZE, (255, 192, 203)),  # Pink
        # Ghost(10 * CELL_SIZE, 8 * CELL_SIZE, (0, 255, 255)),   # Cyan
        # Ghost(11 * CELL_SIZE, 8 * CELL_SIZE, (255, 165, 0))    # Orange
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
                        Ghost(9 * CELL_SIZE, 9 * CELL_SIZE, RED),
                        # Ghost(8 * CELL_SIZE, 8 * CELL_SIZE, (255, 192, 203)),
                        # Ghost(10 * CELL_SIZE, 8 * CELL_SIZE, (0, 255, 255)),
                        # Ghost(11 * CELL_SIZE, 8 * CELL_SIZE, (255, 165, 0))
                    ]
                    # Reset maze dots TODO CORRIGIR PRA RESETAR CORRETAMENTE, ELE DEIXA ATE ONDE ER AP SER ESPÇO EM BRANCO COM PONTOS
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
                # ghost.move(pacman)
                ghost.update(MAZE_LAYOUT, pacman.x, pacman.y)
                # Check collision with ghostsJ
                # if check_collision(pacman.x + CELL_SIZE//2, pacman.y + CELL_SIZE//2, 
                #                  ghost.x + CELL_SIZE//2, ghost.y + CELL_SIZE//2):
                #     game_over = True
                if check_entity_collision(pacman.x, pacman.y, 
                         ghost.x, ghost.y, 
                         CELL_SIZE):
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