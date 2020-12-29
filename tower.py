import pygame
import graphics
from projectile import Projectile
import levels_data

class Tower():

    towers = []

    towerData = {
                1: {'type': 'basic', 'color': graphics.BLUE, 'baseDamage': 10, 'baseRange': 75, 'baseBulletSpeed': 8, 'baseCost': 40},
                2: {'type': 'sniper', 'color': graphics.GREEN, 'baseDamage': 20, 'baseRange': 120, 'baseBulletSpeed': 20, 'baseCost': 90}
                }
    
    def __init__(self, x, y, typeID = 0):
        levels_data.level.towers.append(self)
        self.x = x
        self.y = y        
        self.typeID = typeID
        self.type = Tower.towerData[typeID]["type"]
        self.color = Tower.towerData[typeID]["color"]
        self.damage = Tower.towerData[typeID]["baseDamage"]
        self.range = Tower.towerData[typeID]["baseRange"]
        self.bulletSpeed = Tower.towerData[typeID]["baseBulletSpeed"]
        self.upgradeCost = int(Tower.towerData[typeID]["baseCost"] * 1.5)
        self.level = 1
        self.radius = 15
        self.shootingCooldown = 10
        self.shootingTimer = 0
        self.showRange = True
        self.target = None

    def upgrade(self):
        if levels_data.level.gold >= self.upgradeCost:
            levels_data.level.gold -= self.upgradeCost
            self.level += 1
            self.damage = self.damage * 1.3
            self.range = self.range * 1.1
            self.upgradeCost = int(self.upgradeCost * 1.5)

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        if self.showRange:
            pygame.draw.circle(win, self.color, (self.x, self.y), int(self.range), 1)
    
    def isInRange(self, enemy): 
        # check if coordinates exist (in case the enemy has been deleted) beforehand
        return enemy.x and (enemy.x - self.x)**2 + (enemy.y - self.y)**2 <= self.range ** 2

    def shoot(self):
        # creates a new bullet aimed at the tower's current target
        if self.shootingTimer == 0:
            if self.target:
                if self.target.dead:
                    self.target = None
                elif not self.isInRange(self.target):
                    self.target = None
                else:
                    Projectile(self.x, self.y, self.target, self)
                    self.shootingTimer = self.shootingCooldown
        else:
            self.shootingTimer -= 1