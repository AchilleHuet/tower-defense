import pygame

import graphics
from numpy import sign
import levels_data


class Enemy():

    path = [(378, 301), (378, 259), (460, 259), (460, 343), (503, 343)]

    def __init__(self, x, y, typeID):
        self.x = x
        self.y = y
        self.color = graphics.GREEN
        self.radius = 7
        self.typeID = typeID
        self.speed = 40
        self.health = 30
        self.max_health = self.health
        self.value = 10
        self.pathTarget = 0
        self.moveDirection = (1, 0)
        self.dead = False

    def move(self, base):
        self.x += self.moveDirection[0] * self.speed * levels_data.level.game_speed
        self.y += self.moveDirection[1] * self.speed * levels_data.level.game_speed
        xToTarget = self.x - Enemy.path[self.pathTarget][0]
        yToTarget = self.y - Enemy.path[self.pathTarget][1]
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
        if self.dead:
            return None
        else:
            self.health -= damage
            if self.health <= 0:
                levels_data.level.gold += self.value
                self.kill()
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
        pygame.draw.rect(win, graphics.RED, (int(self.x-5+10*hp), int(self.y)-10, 10-int(10*hp), 2))
