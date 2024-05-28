import pygame
# import sys

pygame.init()

WIDTH = 640
HEIGHT = 480
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
pygame.display.set_caption("Buttons")

#load button images
start = pygame.image.load('Sprites/button_new-game.png').convert_alpha()
#exit_img = pygame.image.load('Sprites/button_exit.png').convert_alpha()
instructions = pygame.image.load('Sprites/button_instructions.png').convert_alpha()

#button class - chatGPT
class Button(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def btn_new():
    print("Start button was clicked!")
def btn_instr():
    print("Exit button was clicked!")

# Create a button instance
button = Button(start, 190, 222)
button2 = Button(instructions, 180, 343)

# Create a sprite group and add the button
buttons = pygame.sprite.Group()
buttons.add(button, button2)

# Main game loop
running = True
while running:
    screen.fill((52, 78, 91))  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if button.is_clicked(event.pos):
                    btn_new()
                if button2.is_clicked(event.pos):
                    btn_instr()

    # Draw the button
    buttons.draw(screen)

    pygame.display.flip()

pygame.quit()
# sys.exit()
