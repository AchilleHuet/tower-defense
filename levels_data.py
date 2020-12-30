import graphics
from grid import Grid
from level import Level
from menu import InformationMenu

# Level 1
gridWidth = 6
gridHeight = 3

gridX = (graphics.WINDOWWIDTH - InformationMenu.width - (graphics.BOXWIDTH + graphics.MARGIN) * gridWidth)//2
gridY = (graphics.WINDOWHEIGHT - (graphics.BOXHEIGHT + graphics.MARGIN) * gridHeight)//2

startGrid = [[0, 2, 1, 1, 1, 2],
             [3, 1, 1, 2, 1, 2],
             [0, 2, 2, 2, 1, 4]]

level1_grid = Grid(gridX, gridY, gridWidth, gridHeight, graphics.BOXWIDTH, graphics.BOXHEIGHT, graphics.MARGIN, startGrid)


level = Level(level1_grid, 100) # level 1
