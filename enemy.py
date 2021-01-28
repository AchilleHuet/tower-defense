import pygame

import graphics
from numpy import sign
import levels_data
from random import random


class Enemy():

    path = [(378, 301), (378, 259), (460, 259), (460, 343), (503, 343)]

    types = {
        1: {'type': 'basic', 'color': graphics.GREEN, 'health': 30, 'speed': 40, 'gold value': 10},
        2: {'type': 'tank', 'color': graphics.RED, 'health': 50, 'speed': 30, 'gold value': 12},
        3: {'type': 'fast', 'color': graphics.YELLOW, 'health': 25, 'speed': 55, 'gold value': 10}
    }

    def __init__(self, x, y, typeID):
        self.x = x + 10*random() - 5
        self.y = y + 10*random() - 5
        self.color = Enemy.types[typeID]['color']
        self.radius = 7
        self.typeID = typeID
        self.speed = Enemy.types[typeID]['speed']
        self.health = Enemy.types[typeID]['health']
        self.max_health = self.health
        self.gold_value = Enemy.types[typeID]['gold value']
        self.path = [(x + 10*random() - 5, y + 10*random() - 5) for (x, y) in Enemy.path]
        self.pathTarget = 0
        self.moveDirection = (1, 0)
        self.dead = False

    def move(self, base):
        self.x += self.moveDirection[0] * self.speed * levels_data.level.game_speed
        self.y += self.moveDirection[1] * self.speed * levels_data.level.game_speed
        xToTarget = self.x - self.path[self.pathTarget][0]
        yToTarget = self.y - self.path[self.pathTarget][1]
        if xToTarget * self.moveDirection[0] + yToTarget * self.moveDirection[1] >= 0:
            if self.pathTarget == len(Enemy.path)-1:
                # Enemy has reached the base
                self.attack(base)
            else:
                # Change direction
                self.pathTarget += 1
                xDirection = sign(Enemy.path[self.pathTarget][0] - Enemy.path[self.pathTarget-1][0])
                yDirection = sign(Enemy.path[self.pathTarget][1] - Enemy.path[self.pathTarget-1][1])
                self.moveDirection = (xDirection, yDirection)


    def attack(self, base):
        base.loseHealth(1)
        self.kill()

    def hit(self, damage):
        if not self.dead:
            self.health -= damage
            if self.health <= 0:
                levels_data.level.gold += self.gold_value
                self.kill()

    def updateTarget(self):
        if self.dead:
            return None
        else:
            return self
        
    def kill(self):
        levels_data.level.enemies.pop(levels_data.level.enemies.index(self))
        self.dead = True

    def draw(self, win):
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.rect(win, graphics.GREEN, (int(self.x)-5, int(self.y)-10, 10, 2))
        hp = self.health/self.max_health
        pygame.draw.rect(win, graphics.DEEPRED, (int(self.x-5+10*hp), int(self.y)-10, 10-int(10*hp), 2))
