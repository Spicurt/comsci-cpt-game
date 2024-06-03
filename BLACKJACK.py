import pygame

pygame.init()

WIDTH = 640
HEIGHT = 480
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

#game variables
game_state = 'starting screen'
game_paused = False
menu_state = 'main'

#define font
font = pygame.font.SysFont("arialblack", 40)
#define color
TEXT_COL = (255, 255, 255)

#Button Class - Coding With Russ
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
    
    def draw(self, surface):
        action = False

        #get mouse pos
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

            #allows more clicks
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        #draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

#Button images
resume_img = pygame.image.load("button_sprites/resume.png").convert_alpha()
options_img = pygame.image.load("button_sprites/menu.png").convert_alpha()
quit_img = pygame.image.load("button_sprites/exit.png").convert_alpha()
video_img = pygame.image.load('button_sprites/video.png').convert_alpha()
audio_img = pygame.image.load('button_sprites/audio.png').convert_alpha()
keys_img = pygame.image.load('button_sprites/keys.png').convert_alpha()
back_img = pygame.image.load('button_sprites/back.png').convert_alpha()
pause_img = pygame.image.load("button_sprites/pause.png").convert_alpha()
start_img = pygame.image.load('button_sprites/new.png').convert_alpha()
instr_img = pygame.image.load('button_sprites/instr.png').convert_alpha()
shop_img = pygame.image.load('button_sprites/shop.png').convert_alpha()

#Button instances
resume_btn = Button(207, 80, resume_img, 1)
options_btn = Button(220, 220, options_img, 1)
quit_btn = Button(240, 370, quit_img, 1)
video_btn = Button(226, 75, video_img, 1)
audio_btn = Button(225, 200, audio_img, 1)
keys_btn = Button(230, 325, keys_img, 1)
back_btn = Button(1, 1, back_img, 0.8)
pause_btn = Button(1, 1, pause_img, 0.8)
start_btn = Button(50, 200, start_img, 1)
instr_btn = Button(350, 200, instr_img, 1)
shop_btn = Button(50, 400, shop_img, 1)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

# #display time for text- my own code
# display_time = 0

running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         game_paused = True
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
    #display_time += 1

    # DRAWING
    screen.fill((52, 78, 91))

    # if display_time >= 100:
    #     game_paused = True

    #if game is paused, activate menu - partly Coding With Russ partly Regulus
    if game_state == 'playing':
        if game_paused == True: #IMPORTANT IMPORTANT TMSFDOPSP
            #check main state
            if menu_state == "main": 
                #draw pause screen buttons 
                if resume_btn.draw(screen):
                    game_paused = False
                if options_btn.draw(screen):
                    menu_state = "options"
                if quit_btn.draw(screen):
                    game_state = "starting screen"
            if menu_state == "options":
                if video_btn.draw(screen):
                    print("Video Settings")
                if audio_btn.draw(screen):
                    print("Audio Settings")
                if keys_btn.draw(screen):
                    print("Change Key Bindings")
                if back_btn.draw(screen):
                    menu_state = "main"
        #if game not paused, draw pause button + other functions - Regulus PUT GAME HERE, PLAY HERE
        else:
            if pause_btn.draw(screen):
                game_paused = True
    elif game_state == 'starting screen':
        screen.fill('seagreen') 

        if start_btn.draw(screen):
            game_state = 'playing'

        if instr_btn.draw(screen):
            print("Instr")
        
        if shop_btn.draw(screen):
            print("Shop")


    pygame.display.flip()
    clock.tick(30)
    #---------------------------


pygame.quit()
