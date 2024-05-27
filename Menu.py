#https://www.youtube.com/watch?v=2iyx8_elcYg&ab_channel=CodingWithRuss
import pygame


pygame.init()

WIDTH = 640
HEIGHT = 480
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
clock = pygame.time.Clock()
pygame.display.set_caption("Main Menu")

#Game variable:
game_paused = False

#Drawing text
font = pygame.font.SysFont("arialblack", 40)

TEXT_COL = (255, 255, 255)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))
# ---------------------------
# Initialize global variables


# ---------------------------

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

    # GAME STATE UPDATES
    # All game math and comparisons happen here

    # DRAWING
    screen.fill((52, 78, 91))  # always the first drawing command

    #checking if game is paused or no
    if game_paused == True:
        pass
        #display menu
    else:
        draw_text("Press SPACE to pause", font, TEXT_COL, 71, 211)

    # Must be the last two lines
    # of the game loop
    pygame.display.update()
    clock.tick(30)
    #---------------------------


pygame.quit()