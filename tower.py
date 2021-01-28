import pygame
import graphics
from projectile import Projectile, ExplosiveProjectile
import levels_data


TOWER_DATA = {
    1: {'type': 'basic', 'color': graphics.BLUE, 'baseDamage': 10, 'baseRange': 75, 'baseBulletSpeed': 150, 'baseCost': 40, 'shooting cd': 0.5},
    2: {'type': 'sniper', 'color': graphics.GREEN, 'baseDamage': 20, 'baseRange': 120, 'baseBulletSpeed': 350, 'baseCost': 70, 'shooting cd': 1.2},
    3: {'type': 'splash', 'color': graphics.RED, 'baseDamage': 16, 'baseRange': 60, 'baseBulletSpeed': 100, 'baseCost': 70, 'shooting cd': 1}
    }


def newTower(x, y, tower_type):
    if tower_type in [1, 2]:
        return Tower(x, y, tower_type)
    elif tower_type == 3:
        return SplashTower(x, y, tower_type)
    else:
        return None


class Tower():
    
    def __init__(self, x, y, typeID):
        levels_data.level.towers.append(self)
        self.x = x
        self.y = y        
        self.typeID = typeID
        self.type = TOWER_DATA[typeID]["type"]
        self.color = TOWER_DATA[typeID]["color"]
        self.damage = TOWER_DATA[typeID]["baseDamage"]
        self.range = TOWER_DATA[typeID]["baseRange"]
        self.bulletSpeed = TOWER_DATA[typeID]["baseBulletSpeed"]
        self.goldValue = TOWER_DATA[typeID]["baseCost"]
        self.upgradeCost = int(self.goldValue * 1.5)
        self.sellValue = int(self.goldValue * 0.5)
        self.level = 1
        self.radius = 15
        self.shootingCooldown = TOWER_DATA[typeID]["shooting cd"]
        self.shootingTimer = 0.01 # set to non-zero so that bullets aren't created instantaneously on tower creation
        self.showRange = True
        self.target = None

    def upgrade(self):
        if levels_data.level.gold >= self.upgradeCost:
            levels_data.level.gold -= self.upgradeCost
            self.level += 1
            self.damage = self.damage * 1.3
            self.range = self.range * 1.1
            self.goldValue += self.upgradeCost
            self.sellValue = int(self.goldValue * 0.5)
            self.upgradeCost = int(self.upgradeCost * 1.5)

    def sell(self):
        levels_data.level.gold += self.sellValue
        levels_data.level.towers.pop(levels_data.level.towers.index(self))
        del self


    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        if self.showRange:
            graphics.draw_transparent_circle(win, self.color, (self.x, self.y), int(self.range), 75)
            pygame.draw.circle(win, self.color, (self.x, self.y), int(self.range), width=1)

    
    def isInRange(self, enemy): 
        # check if coordinates exist (in case the enemy has been deleted) beforehand
        return enemy.x and (enemy.x - self.x)**2 + (enemy.y - self.y)**2 <= self.range ** 2

    def shoot(self):
        # creates a new bullet aimed at the tower's current target
        if self.shootingTimer <= 0:
            if self.target:
                if self.target.dead or not self.isInRange(self.target):
                    self.target = None
                else:
                    Projectile(self.x, self.y, self.target, self)
                    self.shootingTimer = self.shootingCooldown
        else:
            self.shootingTimer -= 1 * levels_data.level.game_speed

class FreezingTower(Tower):
    pass


class SplashTower(Tower):

    def __init__(self, x, y, tower_type):
        super().__init__(x, y, tower_type)
        self.explosion_radius = 40

    def shoot(self):
        # creates a new explosive bullet aimed at the tower's current target
        if self.shootingTimer <= 0:
            if self.target:
                if self.target.dead or not self.isInRange(self.target):
                    self.target = None
                else:
                    ExplosiveProjectile(self.x, self.y, self.target, self, self.explosion_radius, 3, graphics.RED)
                    self.shootingTimer = self.shootingCooldown
        else:
            self.shootingTimer -= 1 * levels_data.level.game_speed
