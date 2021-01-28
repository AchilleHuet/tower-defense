import math
import graphics
import pygame
import levels_data

def damageArea(x, y, radius, damage):
    to_damage = []
    for enemy in levels_data.level.enemies:
        if (enemy.x - x)**2 + (enemy.y - y)**2 <= radius ** 2:
            to_damage.append(enemy)
    for enemy in to_damage:
        enemy.hit(damage)


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
        # deals damage to enemy and resets target if dead
        self.enemy.hit(self.tower.damage)
        self.tower.target = self.enemy.updateTarget()
        self.delete()


class Explosion():

    def __init__(self, x, y, damage, radius):
        levels_data.level.explosions.append(self)
        self.x = x
        self.y = y
        self.damage = damage
        self.max_radius = int(radius)
        self.color = graphics.RED
        self.radius = 3
    
    def explode(self):
        damageArea(self.x, self.y, self.max_radius, self.damage)

    def draw(self, win):
        graphics.draw_transparent_circle(win, self.color, (self.x, self.y), self.max_radius, 75)
        if self.radius < self.max_radius:
            self.radius += 2 # make explosion size shrink every frame
        else:
            self.delete()
    
    def delete(self):
        levels_data.level.explosions.pop(levels_data.level.explosions.index(self))
        del self


class ExplosiveProjectile(Projectile):

    def __init__(self, x, y, enemy, tower, expl_radius, radius, color):
        super().__init__(x, y, enemy, tower, radius, color)
        self.explosion_radius = expl_radius

    def hit(self):
        # create an explosion which damages the enemies
        explosion = Explosion(self.tower.target.x, self.tower.target.y, self.tower.damage, self.explosion_radius)
        explosion.explode()
        # reset tower target if enemy is dead
        self.tower.target = self.enemy.updateTarget()
        self.delete()

