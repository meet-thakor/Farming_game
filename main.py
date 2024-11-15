import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 60
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE
WHITE = (255, 255, 255)
GREEN = (34, 177, 76)
BROWN = (139, 69, 19)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Set up colors for different crop states
CROP_COLORS = {
    "empty": WHITE,
    "fertilized": (255, 255, 255),  # A different color for fertilized soil
    "planted": (255, 255, 0),
    "watered": (0, 255, 0),
    "harvested": (255, 165, 0)
}

# Crop growth times (in seconds)
CROP_GROWTH_TIMES = {
    "wheat": 10,   # 10 seconds to grow
    "corn": 12     # 12 seconds to grow
}

# Set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Farming Game")

# Fonts for text
font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 16)

# Crop class to represent a crop in the game
class Crop:
    def __init__(self, name, growth_time):
        self.name = name
        self.growth_time = growth_time
        self.age = 0
        self.state = "empty"  # "empty", "fertilized", "planted", "watered", "harvested"
        self.time_planted = None

    def fertilize(self):
        if self.state == "empty":
            self.state = "fertilized"
            return True
        return False

    def plant(self):
        if self.state == "fertilized":
            self.state = "planted"
            self.age = 0
            self.time_planted = pygame.time.get_ticks() / 1000  # Get the current time in seconds
            return True
        return False

    def water(self):
        if self.state == "planted":
            self.state = "watered"
            return True
        return False

    def grow(self):
        if self.state == "watered":
            # Check if the crop has reached the growth time
            time_elapsed = pygame.time.get_ticks() / 1000 - self.time_planted
            if time_elapsed >= self.growth_time:
                self.state = "harvested"
                return True
        return False

    def harvest(self):
        if self.state == "harvested":
            self.state = "empty"
            return True
        return False

# Farm class to manage the farm grid and crops
class Farm:
    def __init__(self):
        self.grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    def fertilize_soil(self, x, y):
        if self.grid[y][x] is None:
            crop = Crop("wheat", CROP_GROWTH_TIMES["wheat"])  # Default to wheat for now
            if crop.fertilize():
                self.grid[y][x] = crop
                return True
        return False

    def plant_crop(self, x, y, crop_name):
        if self.grid[y][x] is not None and self.grid[y][x].state == "fertilized":
            crop = self.grid[y][x]
            if crop.plant():
                self.grid[y][x] = crop
                return True
        return False

    def water_crop(self, x, y):
        if self.grid[y][x] is not None:
            crop = self.grid[y][x]
            if crop.water():
                return True
        return False

    def grow_crops(self):
        for row in self.grid:
            for cell in row:
                if cell is not None:
                    cell.grow()

    def harvest_crop(self, x, y):
        if self.grid[y][x] is not None:
            crop = self.grid[y][x]
            if crop.harvest():
                self.grid[y][x] = None
                return True
        return False

    def draw(self, screen):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                crop = self.grid[y][x]

                if crop is None:
                    pygame.draw.rect(screen, WHITE, rect)
                else:
                    color = CROP_COLORS[crop.state]
                    pygame.draw.rect(screen, color, rect)
                
                pygame.draw.rect(screen, BLACK, rect, 2)  # Draw the grid border

                # Draw the crop name in the cell
                if crop is not None:
                    label = small_font.render(crop.name, True, BLACK)
                    screen.blit(label, (x * CELL_SIZE + 5, y * CELL_SIZE + 5))

# Function to display a message on the screen
def display_message(message, color, position):
    label = font.render(message, True, color)
    screen.blit(label, position)

# Main game loop
def game_loop():
    farm = Farm()
    clock = pygame.time.Clock()
    running = True
    selected_crop = "wheat"
    mouse_x, mouse_y = 0, 0

    while running:
        screen.fill(GREEN)  # Set the background color

        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        grid_x, grid_y = min(mouse_x // CELL_SIZE, GRID_WIDTH - 1), min(mouse_y // CELL_SIZE, GRID_HEIGHT - 1)

        # Draw the farm grid
        farm.draw(screen)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click to fertilize, plant, or water
                    if farm.grid[grid_y][grid_x] is None:
                        farm.fertilize_soil(grid_x, grid_y)  # Fertilize first
                    elif farm.grid[grid_y][grid_x] is not None:
                        crop = farm.grid[grid_y][grid_x]
                        if crop.state == "fertilized":
                            farm.plant_crop(grid_x, grid_y, selected_crop)
                        elif crop.state == "planted":
                            farm.water_crop(grid_x, grid_y)
                elif event.button == 3:  # Right click to harvest
                    farm.harvest_crop(grid_x, grid_y)

        # Grow crops every frame
        farm.grow_crops()

        # Display instructions
        display_message("Left click to fertilize, plant, or water. Right click to harvest.", BLACK, (10, 10))
        display_message(f"Current crop: {selected_crop}", BLACK, (10, 40))

        # Update the screen
        pygame.display.flip()

        # Set the game speed (FPS)
        clock.tick(60)

# Start the game loop
if __name__ == "__main__":
    game_loop()
    pygame.quit()
