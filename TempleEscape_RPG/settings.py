# settings.py
import pygame

# Screen Dimensions
WIDTH = 800
HEIGHT = 600
FPS = 60

# Layout
TEXT_BOX_HEIGHT = 250
TEXT_BOX_Y = HEIGHT - TEXT_BOX_HEIGHT

# Jungle Temple Color Palette (RGB)
JUNGLE_DARK = (12, 25, 18)     # Deep dark green background
STONE = (45, 50, 48)           # Ancient gray-green stone
STONE_LIGHT = (70, 75, 70)     # Highlighted stone
MOSS_GREEN = (60, 140, 60)     # Hover color
GOLD = (218, 165, 32)          # Artifact gold
WHITE = (230, 230, 220)        # Aged paper white
BLOOD_RED = (160, 30, 30)      # HP Bar
TEMPLE_BLUE = (50, 100, 180)   # Sanity Bar
KHAKI = (195, 176, 145)        # Explorer clothes
LEATHER = (90, 50, 30)         # Satchel/Boots

# Fonts
pygame.font.init()
TITLE_FONT = pygame.font.SysFont("impact", 56)
TEXT_FONT = pygame.font.SysFont("georgia", 20)
BUTTON_FONT = pygame.font.SysFont("arial", 16, bold=True)