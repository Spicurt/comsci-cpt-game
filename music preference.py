import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30

# Colors
GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (169, 169, 169)

# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('User Preferences')

# Clock to control the frame rate
clock = pygame.time.Clock()

# Load music
pygame.mixer.music.load('your_music_file.mp3') # Your music file as placeholder
pygame.mixer.music.play(-1)  # Play music in a loop



pygame.quit()
sys.exit()
