import math
import graphics
import pygame
import levels_data

class Projectile():

    def __init__(self, x, y, enemy, tower, radius = 2, color = graphics.BLACK):
        levels_data.level.bullets.append(self)
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.enemy = enemy
        self.tower = tower
        self.speed = self.tower.bulletSpeed

    def move(self):
        directionX = self.enemy.x - self.x
        directionY = self.enemy.y - self.y
        directionXNorm = directionX / math.sqrt(directionX ** 2 + directionY ** 2)
        directionYNorm = directionY / math.sqrt(directionX ** 2 + directionY ** 2)
        self.x += directionXNorm * self.speed * levels_data.level.game_speed
        self.y += directionYNorm * self.speed * levels_data.level.game_speed

    def draw(self, win):
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.radius)

    def delete(self):
        levels_data.level.bullets.pop(levels_data.level.bullets.index(self))

    def hit(self):
        self.tower.target = self.enemy.hit(self.tower.damage)
        self.delete()