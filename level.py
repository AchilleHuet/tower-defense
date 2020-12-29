import pygame

import graphics
from menu import InformationMenu


class Level():

    def __init__(self, grid, startingGold, waves=[]):
        # self.base = None
        # self.portal = None
        self.grid = grid
        self.gold = startingGold
        self.waves = waves
        self.towers = []
        self.enemies = []
        self.bullets = []
        self.waveNumber = 0

    def draw(self, window):
        gold_text = graphics.FONT.render("Gold: " + str(self.gold), 1, graphics.WHITE)
        next_wave_text = graphics.FONT.render("Next wave: " + str(self.grid.portal.waveTimer//20), 1, graphics.WHITE)
        wave_number_text = graphics.FONT.render("Wave " + str(self.waveNumber), 1, graphics.WHITE)
        window.blit(gold_text, (graphics.WINDOWWIDTH - InformationMenu.width - gold_text.get_width() - 10, 10))
        window.blit(wave_number_text, (graphics.WINDOWWIDTH - InformationMenu.width - wave_number_text.get_width() - 10, 30))
        window.blit(next_wave_text, (graphics.WINDOWWIDTH - InformationMenu.width - next_wave_text.get_width() - 10, 50))
        self.grid.draw(window)
        for tow in self.towers:
            tow.draw(window)
        for enemy in self.enemies:
            enemy.draw(window)
        for bullet in self.bullets:
            bullet.draw(window)
    
    def deleteData(self):
        for tow in self.towers:
            del tow
        for enemy in self.enemies:
            del enemy
        for bullet in self.bullets:
            del bullet
        del self.grid
        del self