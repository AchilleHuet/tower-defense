import graphics
from menu import InformationMenu


class Level():

    def __init__(self, grid, starting_gold, waves):
        # self.base = None
        # self.portal = None
        self.grid = grid
        self.starting_gold = starting_gold
        self.gold = starting_gold
        self.waves = waves
        self.speed_modifier = 1
        self.fps = 60
        self.game_speed = self.speed_modifier / self.fps
        self.towers = []
        self.enemies = []
        self.bullets = []
        self.explosions = []
        self.wave_number = 0

    def draw(self, window):
        gold_text = graphics.FONT.render("Gold: " + str(self.gold), 1, graphics.WHITE)
        lives_text = graphics.FONT.render("Lives: " + str(self.grid.base.health), 1, graphics.WHITE)
        next_wave_text = graphics.FONT.render("Next wave: " + str(int(self.grid.portal.wave_timer)), 1, graphics.WHITE)
        wave_number_text = graphics.FONT.render("Wave " + str(self.wave_number), 1, graphics.WHITE)
        window.blit(gold_text, (graphics.WINDOWWIDTH - InformationMenu.width - gold_text.get_width() - 10, 10))
        window.blit(lives_text, (graphics.WINDOWWIDTH - InformationMenu.width - lives_text.get_width() - 10, 30))
        window.blit(wave_number_text, (10, 10))
        window.blit(next_wave_text, (10, 30))
        self.grid.draw(window)
        for tower in self.towers:
            tower.draw(window)
        for explosion in self.explosions:
            explosion.draw(window)
        for enemy in self.enemies:
            enemy.draw(window)
        for bullet in self.bullets:
            bullet.draw(window)
    
    def deleteData(self):
        for tower in self.towers:
            del tower
        for enemy in self.enemies:
            del enemy
        for bullet in self.bullets:
            del bullet
        del self.grid
        del self

    def changeSpeed(self, modifier):
        self.speed_modifier = modifier
        self.game_speed = self.speed_modifier / self.fps

    def changeFPS(self, fps):
        self.fps = fps
        self.game_speed = self.speed_modifier / self.fps

    def reset(self):
        for tower in self.towers:
            del tower
        for enemy in self.enemies:
            del enemy
        for bullet in self.bullets:
            del bullet
        self.grid.reset()
        self.gold = self.starting_gold
        self.towers = []
        self.enemies = []
        self.bullets = []
        self.wave_number = 0
