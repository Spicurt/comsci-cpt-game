import pygame
import button

pygame.init()

WIDTH = 640
HEIGHT = 480
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

#game variables
game_paused = False
menu_state = "main"

#define font
font = pygame.font.SysFont("arialblack", 40)
#define color
TEXT_COL = (255, 255, 255)

#load images
resume_img = pygame.image.load("Sprites/resume.png").convert_alpha()
options_img = pygame.image.load("Sprites/menu.png").convert_alpha()
quit_img = pygame.image.load("Sprites/exit.png").convert_alpha()
video_img = pygame.image.load('Sprites/video.png').convert_alpha()
audio_img = pygame.image.load('Sprites/audio.png').convert_alpha()
keys_img = pygame.image.load('Sprites/keys.png').convert_alpha()
back_img = pygame.image.load('Sprites/back.png').convert_alpha()

#create button instances
resume_btn = button.Button(304, 125, resume_img, 1)
options_btn = button.Button(297, 250, options_img, 1)
quit_btn = button.Button(336, 375, quit_img, 1)
video_btn = button.Button(226, 75, video_img, 1)
audio_btn = button.Button(225, 200, audio_img, 1)
keys_btn = button.Button(246, 325, keys_img, 1)
back_btn = button.Button(1, 1, back_img, 1)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

# #display time for text- my own code
# display_time = 0

running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_paused = True
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
    #display_time += 1

    # DRAWING
    screen.fill((52, 78, 91))

    # if display_time >= 100:
    #     game_paused = True

    #check if game is paused
    if game_paused == True: #IMPORTANT IMPORTANT TMSFDOPSP
        #check menu state
        if menu_state == "main": 
            #draw pause screen buttons 
            if resume_btn.draw(screen):
                game_paused = False
            if options_btn.draw(screen):
                menu_state = "options"
            if quit_btn.draw(screen):
                running = False
        if menu_state == "options":
            #draw different buttons
            if video_btn.draw(screen):
                print("Video Settings")
            if audio_btn.draw(screen):
                print("Audio Settings")
            if keys_btn.draw(screen):
                print("Change Key Bindings")
            if back_btn.draw(screen):
                menu_state = "main"
    else:
        draw_text("press SPACE to pause", font, TEXT_COL, 100, 210)

    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(30)
    #---------------------------


pygame.quit()
