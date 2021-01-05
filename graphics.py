import pygame
pygame.init() # initialize pygame for creating fonts

WHITE = (255, 255, 255)
LIGHTGRAY = (150, 150, 150)
GRAY = (80, 80, 80)
BLACK = (0, 0, 0)

LIGHTBLUE = (210, 210, 255)
BLUE = (150, 150, 255)
DEEPBLUE = (0, 0, 255)

LIGHTGREEN = (210, 255, 210)
GREEN = (150, 255, 150)
DEEPGREEN = (0, 255, 0)

LIGHTRED = (255, 210, 210)
RED = (255, 150, 150)
DEEPRED = (255, 0, 0)

LIGHTYELLOW = (255, 255, 210)
YELLOW = (255, 255, 150)
DEEPYELLOW = (255, 255, 0)

PURPLE = (144, 28, 232)

LIGHTBROWN = (176, 144, 100)

FONT = pygame.font.SysFont('consolas', 15, True)
TITLEFONT = pygame.font.SysFont('consolas', 20, True)

WINDOWWIDTH = 1000
WINDOWHEIGHT = 600

BOXWIDTH = 40
BOXHEIGHT = 40
MARGIN = 1

def draw_transparent_circle(screen, color, center, radius, alpha):
    surf = pygame.Surface((radius*2, radius*2), )
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    surf.set_alpha(alpha)
    screen.blit(surf, (center[0]-radius, center[1]-radius))