import pygame
import sys

pygame.init()

# Screen dimensions
WIDTH = 640
HEIGHT = 480
SIZE = (WIDTH, HEIGHT)

# Initialize screen and clock
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# Colors
BG = (20, 30, 50)

# Load fonts
mytextfont = pygame.font.Font("font.ttf", 50)
label_font = pygame.font.Font("font.ttf", 36)
volume_font = pygame.font.Font("font.ttf", 30)
control_font = pygame.font.Font("font.ttf", 30)

# Load images and set positions
button_image = pygame.transform.scale(pygame.image.load("play_button.png"), (300, 100))
button_rect = button_image.get_rect(center=(320, 130))

menu_text = mytextfont.render("FROGGER", True, (255, 255, 255))
text_rect = menu_text.get_rect(center=(320, 50))

options_button = pygame.transform.scale(pygame.image.load("Options_button_pixleart.jpeg"), (50, 50))
options_button_rect = options_button.get_rect(center=(600, 450))

back_button = pygame.transform.scale(pygame.image.load("back-button2 (1).png"), (75, 75))
back_button_loc = back_button.get_rect(center=(50, 450))

label_text = label_font.render("Options", True, (255, 255, 255))
label_rect = label_text.get_rect(center=(320, 50))

volume_text = volume_font.render("Volume", True, (255, 255, 255))
volume_loc = volume_text.get_rect(center=(320, 100))

on_button = pygame.transform.scale(pygame.image.load("Sound_On_button.png"), (50, 50))
on_button_loc = on_button.get_rect(center=(250, 150))

off_button = pygame.transform.scale(pygame.image.load("Sound_off_button.png"), (50, 50))
off_button_loc = off_button.get_rect(center=(400, 150))

control_text = control_font.render("Control settings", True, (255, 255, 255))
control_loc = control_text.get_rect(center=(320, 200))

exit_button = pygame.transform.scale(pygame.image.load("Exit_game(1).png"), (300, 100))
exit_button_loc = exit_button.get_rect(center=(320, 400))

arrow_button = pygame.transform.scale(pygame.image.load("Arrow_keys_options.png"), (80, 80))
arrow_button_loc = arrow_button.get_rect(center=(400, 250))

wasd_button = pygame.transform.scale(pygame.image.load("wasd.png"), (80, 80))
wasd_button_loc = wasd_button.get_rect(center=(250, 250))

# Game state
current_screen = "main_menu"
volume_on = True

# Load music
pygame.mixer.init()
sound = pygame.mixer.Sound("339124__zagi2__gaming-arcade-loop.wav")
sound.play(-1)

def main_menu():
    pygame.display.set_caption("Menu")
    screen.fill(BG)
    screen.blit(button_image, button_rect)
    screen.blit(menu_text, text_rect)
    screen.blit(options_button, options_button_rect)
    screen.blit(exit_button, exit_button_loc)

def game_screen():
    screen.fill((0, 100, 0))

def options_menu():
    screen.fill(BG)
    screen.blit(volume_text, volume_loc)
    screen.blit(back_button, back_button_loc)
    screen.blit(label_text, label_rect)
    screen.blit(on_button, on_button_loc)
    screen.blit(off_button, off_button_loc)
    screen.blit(control_text, control_loc)
    screen.blit(arrow_button, arrow_button_loc)
    screen.blit(wasd_button, wasd_button_loc)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == "main_menu":
                if button_rect.collidepoint(event.pos):
                    current_screen = "game"
                elif options_button_rect.collidepoint(event.pos):
                    current_screen = "options"
                elif exit_button_loc.collidepoint(event.pos):
                    running = False
            elif current_screen == "options":
                if back_button_loc.collidepoint(event.pos):
                    current_screen = "main_menu"
                elif on_button_loc.collidepoint(event.pos):
                    volume_on = True
                    pygame.mixer.unpause()
                elif off_button_loc.collidepoint(event.pos):
                    volume_on = False
                    pygame.mixer.pause()

    if current_screen == "main_menu":
        main_menu()
    elif current_screen == "game":
        game_screen()
    elif current_screen == "options":
        options_menu()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
