import pygame

pygame.init()

#GREEN CODE: does not work, or work on it later

WIDTH = 1280
HEIGHT = 720
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

#game variables
TOKENS = 50
game_state = 'starting screen'
game_paused = False
menu_state = 'main'
#powerup 1, powerup 2
SHOP_ITEMS = [0, 0]
PRICES = [5, 10]

#define font
font = pygame.font.SysFont("arialblack", 40)
font2 = pygame.font.SysFont("arvo", 13)
#define color
TEXT_COL = (255, 255, 255)

#Text function
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

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
quit_img = pygame.image.load("button_sprites/quit.png").convert_alpha()
video_img = pygame.image.load('button_sprites/video.png').convert_alpha()
audio_img = pygame.image.load('button_sprites/audio.png').convert_alpha() #red
keys_img = pygame.image.load('button_sprites/keys.png').convert_alpha() #green
back_img = pygame.image.load('button_sprites/back.png').convert_alpha() #red
pause_img = pygame.image.load("button_sprites/pause.png").convert_alpha() 
start_img = pygame.image.load('button_sprites/new.png').convert_alpha() #red
instr_img = pygame.image.load('button_sprites/instr.png').convert_alpha()
shop_img = pygame.image.load('button_sprites/shop.png').convert_alpha()

#sprites
question_img = pygame.image.load("button_sprites/question_card.png").convert_alpha()

#Button instances
resume_btn = Button(200, 80, resume_img, 1)
options_btn = Button(200, 220, options_img, 1)
quit_btn = Button(200, 370, quit_img, 1)
video_btn = Button(WIDTH -300, 75, video_img, 1)
audio_btn = Button(WIDTH -300, 200, audio_img, 1)
keys_btn = Button(WIDTH -300, 325, keys_img, 1)
back_btn = Button(20, 20, back_img, 0.8)
pause_btn = Button(20, 20, pause_img, 0.8)
start_btn = Button(500, 120, start_img, 1)
instr_btn = Button(492, 300, instr_img, 1)
shop_btn = Button(535, 480, shop_img, 1)

#sprite instances
question_btn = Button(60, 80, question_img, 1)

# Display time for text - Chat GPT
show_error = False
error_start_time = 0
ERROR_DISPLAY_DURATION = 2000  # 2 seconds

# Display time for text 2 - Regulus
show_error2 = False
error_start_time2 = 0
ERROR_DISPLAY_DURATION2 = 2000  # 2 seconds

# Shop function - Regulus
def shop():
    screen.fill("lightblue")
    draw_text(f"{TOKENS}", font, TEXT_COL, 1000, 250)
    for i in range(len(SHOP_ITEMS)):
        if i == 0:
            draw_text(f"{SHOP_ITEMS[i]}", font, TEXT_COL, 700, 250)
        if i == 1:
            draw_text(f"{SHOP_ITEMS[i]}", font, TEXT_COL, 700, 500)
    
    if question_btn.draw(screen):
        paying1()

def paying1():
    global TOKENS, show_error, error_start_time
    if TOKENS > 50:
        TOKENS -= PRICES[0]
        SHOP_ITEMS[0] += 1
    else:
        show_error = True
        error_start_time = pygame.time.get_ticks()
        #Put this with other button
        # show_error2 = True
        # error_start_time2 = pygame.time.get_ticks()

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

    #starting screen - Regulus
    if game_state == 'starting screen':
        screen.fill('seagreen') 

        if start_btn.draw(screen):
            game_state = 'playing'

        if instr_btn.draw(screen):
            print("Instr")
        
        if shop_btn.draw(screen):
            game_state = 'shop'

    #if game is paused, activate menu - Regulus
    elif game_state == 'playing': #- Regulus
        screen.fill((52, 78, 91))
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
                    game_paused = False
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
        else: #- Regulus
            draw_text(f"I am a powerup", font, TEXT_COL, 160, 250)
            if pause_btn.draw(screen):
                game_paused = True
            #Darren put the game here
    
    if game_state == 'shop':
        shop()
        if back_btn.draw(screen):
            game_state = "starting screen"

#Show error - chatgpt
    if show_error:
        current_time = pygame.time.get_ticks()
        if current_time - error_start_time < ERROR_DISPLAY_DURATION:
            draw_text("Not enough tokens!", font, TEXT_COL, 160, 250)
        else:
            show_error = False

#Show error 2 - Regulus
    if show_error2:
        current_time2 = pygame.time.get_ticks()
        if current_time2 - error_start_time2 < ERROR_DISPLAY_DURATION2:
            draw_text("Not enough tokens!", font, TEXT_COL, 400, 250)
        else:
            show_error = False

    pygame.display.flip()
    clock.tick(30)
    #---------------------------


pygame.quit()
