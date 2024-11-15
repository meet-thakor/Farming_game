import pygame
from farm import Farm
from settings import TOOL_ICONS, screen, font, small_font
from sound import play_sound, stop_sound_if_expired
from utils import display_message, display_tool_info

# Initialize Pygame
pygame.init()

# Explicitly initialize the font module
pygame.font.init()

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
                        play_sound(fertilize_sound, "fertilizer")
                    elif dragging_tool == "water_can":
                        farm.water_crop(grid_x, grid_y)
                        play_sound(water_sound, "water_can")
                    elif dragging_tool == "wheat":
                        farm.plant_crop(grid_x, grid_y, "wheat")
                    elif dragging_tool == "harvest":
                        if farm.harvest_crop(grid_x, grid_y):
                            farm.money += 10  # Add money for harvesting
                            play_sound(harvest_sound, "harvest")
                    dragging_tool = None

        # Display the selected tool and money
        display_message(f"Selected Tool: {selected_tool}", BLACK, (140, 10), screen)
        display_message(f"Money: ${farm.money}", BLACK, (140, 40), screen)

        # Display tooltip for selected tool
        display_tool_info(selected_tool, screen)

        # Update the screen
        pygame.display.flip()

        # Manage sound effects duration
        stop_sound_if_expired()

        # Set the game speed (FPS)
        clock.tick(60)

# Start the game loop
if __name__ == "__main__":
    game_loop()
    pygame.quit()
