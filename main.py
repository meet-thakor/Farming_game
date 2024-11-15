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
DARK_GRAY = (64, 64, 64)

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

# Tool icons (we'll use basic rectangles as placeholders)
TOOL_ICONS = {
    "fertilizer": pygame.Surface((40, 40)),
    "water_can": pygame.Surface((40, 40)),
    "wheat": pygame.Surface((40, 40)),
    "harvest": pygame.Surface((40, 40))
}

TOOL_ICONS["fertilizer"].fill(BROWN)
TOOL_ICONS["water_can"].fill(BLUE)
TOOL_ICONS["wheat"].fill(YELLOW := (255, 255, 0))
TOOL_ICONS["harvest"].fill(ORANGE := (255, 165, 0))

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
    selected_tool = "fertilizer"  # Default tool
    dragging_tool = None
    mouse_x, mouse_y = 0, 0

    while running:
        screen.fill(GREEN)  # Set the background color

        # Draw the farm grid
        farm.draw(screen)

        # Draw the sidebar
        pygame.draw.rect(screen, DARK_GRAY, pygame.Rect(0, 0, 120, SCREEN_HEIGHT))  # Sidebar
        screen.blit(TOOL_ICONS["fertilizer"], (20, 20))
        screen.blit(TOOL_ICONS["water_can"], (20, 80))
        screen.blit(TOOL_ICONS["wheat"], (20, 140))
        screen.blit(TOOL_ICONS["harvest"], (20, 200))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x < 120:  # Clicking on the sidebar
                    if 20 <= mouse_y <= 60:
                        selected_tool = "fertilizer"
                    elif 80 <= mouse_y <= 120:
                        selected_tool = "water_can"
                    elif 140 <= mouse_y <= 180:
                        selected_tool = "wheat"
                    elif 200 <= mouse_y <= 240:
                        selected_tool = "harvest"
                else:
                    dragging_tool = selected_tool  # Begin dragging the selected tool
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging_tool:
                    # Get the grid position where the tool is dropped
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_x, grid_y = min(mouse_x // CELL_SIZE, GRID_WIDTH - 1), min(mouse_y // CELL_SIZE, GRID_HEIGHT - 1)

                    # Apply the tool action based on the tool selected
                    if dragging_tool == "fertilizer":
                        farm.fertilize_soil(grid_x, grid_y)
                    elif dragging_tool == "water_can":
                        farm.water_crop(grid_x, grid_y)
                    elif dragging_tool == "wheat":
                        farm.plant_crop(grid_x, grid_y, "wheat")
                    elif dragging_tool == "harvest":
                        farm.harvest_crop(grid_x, grid_y)
                    dragging_tool = None

        # Display the selected tool
        display_message(f"Selected Tool: {selected_tool}", BLACK, (140, 10))

        # Update the screen
        pygame.display.flip()

        # Set the game speed (FPS)
        clock.tick(60)

# Start the game loop
if __name__ == "__main__":
    game_loop()
    pygame.quit()
