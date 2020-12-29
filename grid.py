import pygame

import graphics
import enemy
from tower import Tower
import levels_data


class Grid():
    
    def __init__(self, x, y, width, height, boxWidth, boxHeight, margin, layout):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.margin = margin
        self.boxWidth = boxWidth
        self.boxHeight = boxHeight
        self.portal = None
        self.base = None
        self.boxes = [[Box(self, i, j, boxWidth, boxHeight, layout[i][j]) for j in range(self.width)] for i in range(self.height)]
        self.activeBox = None

    def getBox(self, pos):
        """
        Returns the box object at the given screen coordinates
        """
        x, y = pos
        j = (x - self.margin - self.x) / (self.boxWidth + self.margin)
        i = (y - self.margin - self.y) / (self.boxHeight + self.margin)
        if (0 <= i <= self.height) and (0 <= j <= self.width):
            return self.boxes[int(i)][int(j)]
        else:
            return None
    
    def draw(self, window):
        for line in self.boxes:
            for box in line:
                box.draw(window)


class Box():

    # dictionary of the types of boxes and their base graphics
    boxTypes = {0: {"type": "empty", "color": graphics.BLACK},
                1: {"type": "path", "color": graphics.LIGHTBROWN},
                2: {"type": "tower", "color": graphics.GRAY},
                3: {"type": "portal", "color": graphics.PURPLE},
                4: {"type": "base", "color": graphics.RED}}

    def __init__(self, grid, i, j, width, height, boxType):
        self.grid = grid
        self.i = i
        self.j = j
        self.width = width
        self.height = height
        self.x = self.grid.x + self.grid.margin + self.j*(self.width + self.grid.margin) 
        self.y = self.grid.y + self.grid.margin + self.i*(self.height + self.grid.margin)
        self.boxType = boxType
        self.color = Box.boxTypes[boxType]["color"]
        self.value = Box.boxTypes[boxType]["type"]
        if self.value == "tower":
            self.xTower = self.x + self.width//2
            self.yTower = self.y + self.height//2
            self.tower = None
        elif self.value == "portal":
            self.portal = Portal(self.x + self.width//2, self.y + self.height//2)
            self.grid.portal = self.portal
        elif self.value == "base":
            self.base = Base(self.x + self.width//2, self.y + self.height//2, health = 10)
            self.grid.base = self.base

    def addTower(self, typeID):
        """
        Updates the tower property of the box
        """
        self.tower = Tower(self.xTower, self.yTower, int(typeID))

    def removeTower(self):
        self.tower = None

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        
    def deactivate(self):
        self.color = graphics.GRAY
        if self.tower:
            self.tower.showRange = False

    def activate(self, activeBox):
        if activeBox:
            activeBox.deactivate()
        if self.value == "tower":
            self.color = graphics.LIGHTGREEN
            if self.tower:
                self.tower.showRange = True
            return self
        return None
        

class Portal():

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.enemiesToSpawn = 0
        self.spawnCooldown = 3
        self.waveCooldown = 300
        self.spawnTimer = 0
        self.waveTimer = 200 # 10 seconds before 1st wave
        self.enemyType = None

    def spawnEnemy(self):
        if self.spawnTimer == 0:
            if self.enemiesToSpawn > 0:
                self.spawnTimer = self.spawnCooldown
                new_enemy = enemy.Enemy(self.x, self.y, self.enemyType)
                levels_data.level.enemies.append(new_enemy)
                self.enemiesToSpawn -= 1
        else:
            self.spawnTimer -= 1
        if self.waveTimer > 0:
            self.waveTimer -= 1

    def spawnWave(self, number, enemyType, tightWave):
        """
        spawn a number of enemies over several frames, spaced out according to wave type
        """
        if self.waveTimer == 0:
            levels_data.level.waveNumber += 1
            self.waveTimer = self.waveCooldown
            self.enemiesToSpawn = number
            self.spawnCooldown = 3 if tightWave else 10
            self.enemyType = enemyType
        else:
            self.waveTimer -= 1


class Base():

    def __init__(self, x, y, health):
        self.x = x
        self.y = y
        self.health = health