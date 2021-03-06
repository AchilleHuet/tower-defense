import pygame

import graphics
import enemy
from tower import newTower
import levels_data


class Grid():
    
    def __init__(self, x, y, boxWidth, boxHeight, margin, layout):
        self.x = x
        self.y = y
        self.width = len(layout[0])
        self.height = len(layout)
        self.margin = margin
        self.boxWidth = boxWidth
        self.boxHeight = boxHeight
        self.portal = None
        self.base = None
        self.layout = layout
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
    
    def reset(self):
        self.portal = None
        self.base = None
        self.boxes = [[Box(self, i, j, self.boxWidth, self.boxHeight, self.layout[i][j]) for j in range(self.width)] for i in range(self.height)]
        self.activeBox = None


class Box():

    # dictionary of the types of boxes and their base graphics
    boxTypes = {0: {"type": "empty", "color": graphics.BLACK},
                1: {"type": "path", "color": graphics.LIGHTBROWN},
                2: {"type": "tower", "color": graphics.GRAY},
                3: {"type": "portal", "color": graphics.PURPLE},
                4: {"type": "base", "color": graphics.DEEPRED}}

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
        """Adds a tower of type typeID to the box"""
        self.tower = newTower(self.xTower, self.yTower, typeID)

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
        self.enemies_to_spawn = 0
        self.spawn_cooldown = 0.5 # default cooldown between enemies
        self.wave_cooldown = 15 # default cooldown between waves
        self.spawn_timer = 0
        self.wave_timer = 10 # active timer => 10 seconds before 1st wave
        self.enemy_type = None # type of enemy to spawn

    def spawnEnemy(self):
        if self.spawn_timer <= 0:
            if self.enemies_to_spawn > 0:
                self.spawn_timer = self.spawn_cooldown
                new_enemy = enemy.Enemy(self.x, self.y, self.enemy_type)
                levels_data.level.enemies.append(new_enemy)
                self.enemies_to_spawn -= 1
        else:
            self.spawn_timer -= 1 * levels_data.level.game_speed

    def spawnWave(self, number, enemy_type, tightWave):
        """
        spawn a number of enemies over several frames, spaced out according to wave type
        """
        if self.wave_timer <= 0:
            levels_data.level.wave_number += 1
            self.wave_timer = self.wave_cooldown
            self.enemies_to_spawn = number
            self.spawn_cooldown = 0.15 if tightWave else 0.5
            self.enemy_type = enemy_type
        else:
            self.wave_timer -= 1 * levels_data.level.game_speed

    def nextWave(self):
        if self.enemies_to_spawn == 0 and self.spawn_timer <= 0:
            self.wave_timer = 0 # start the next wave


class Base():

    def __init__(self, x, y, health):
        self.x = x
        self.y = y
        self.health = health

    def loseHealth(self, damage):
        if self.health > damage:
            self.health -= damage
        else:
            self.health = 0
            print("You died !")