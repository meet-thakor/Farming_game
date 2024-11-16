import pygame
from farm import Farm
from settings import (
     screen, SCREEN_WIDTH, SCREEN_HEIGHT, TOOL_ICONS, GREEN, DARK_GRAY, BLACK, WHITE, CELL_SIZE, GRID_WIDTH, GRID_HEIGHT
)
from sound import play_sound, stop_sound_if_expired
from utils import display_message, display_tool_info

# Initialize the fullscreen state
fullscreen = False

# Load sound files
fertilize_sound = pygame.mixer.Sound("sounds/fertilize.mp3")
water_sound = pygame.mixer.Sound("sounds/watering.mp3")
harvest_sound = pygame.mixer.Sound("sounds/harvest.mp3")

def toggle_fullscreen():
    global screen, fullscreen
    if fullscreen:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Switch to windowed mode
    else:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Switch to fullscreen mode
    fullscreen = not fullscreen  # Toggle the fullscreen flag

    
def game_loop():
    farm = Farm()
    clock = pygame.time.Clock()
    running = True
    selected_tool = "fertilizer"  # Default tool
    dragging_tool = None
    mouse_x, mouse_y = 0, 0

    while running:

        # Fill the background
        screen.fill(GREEN)  # Set the background color

        # Draw the farm grid
        farm.draw(screen)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False  # Exit the game if ESC is pressed
                elif event.key == pygame.K_f:
                    toggle_fullscreen()  # Toggle fullscreen mode when 'F' key is pressed
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
                elif mouse_y < SCREEN_HEIGHT - 100:  # Clicking inside the grid
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

        # Update farm (this will update crop growth)
        farm.update()

        # Draw the sidebar
        pygame.draw.rect(screen, DARK_GRAY, pygame.Rect(0, 0, 120, SCREEN_HEIGHT))  # Sidebar
        screen.blit(TOOL_ICONS["fertilizer"], (20, 20))
        screen.blit(TOOL_ICONS["water_can"], (20, 80))
        screen.blit(TOOL_ICONS["wheat"], (20, 140))
        screen.blit(TOOL_ICONS["harvest"], (20, 200))

        # Draw the UI Section
        ui_section_height = 100
        ui_rect = pygame.Rect(0, SCREEN_HEIGHT - ui_section_height, SCREEN_WIDTH, ui_section_height)
        pygame.draw.rect(screen, WHITE, ui_rect)

        # Display the selected tool and money in the UI section
        display_message(f"Selected Tool: {selected_tool}", BLACK, (140, SCREEN_HEIGHT - ui_section_height + 10), screen)
        display_message(f"Money: ${farm.money}", BLACK, (140, SCREEN_HEIGHT - ui_section_height + 40), screen)

        # Display tooltip for selected tool in the UI section
        display_tool_info(selected_tool, screen, y_offset=SCREEN_HEIGHT - ui_section_height + 70)

        # Update the screen
        pygame.display.flip()

        # Manage sound effects duration
        stop_sound_if_expired()

        # Set the game speed (FPS)
        clock.tick(60)

    pygame.quit()

    print("Game loop ended")  # Debug

if __name__ == "__main__":
    try:
        game_loop()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Cleaning up resources...")  # Debug
        pygame.display.quit()  # Close the display window
        pygame.mixer.quit()    # Stop all sound-related resources
        pygame.quit()          # Quit Pygame
        print("Pygame quit successfully")  # Debug
        exit()                 # Terminate the Python script completely
