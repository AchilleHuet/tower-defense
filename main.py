import pygame

import graphics
import levels_data
import menu

pygame.init()


# Window setup
win = pygame.display.set_mode((graphics.WINDOWWIDTH, graphics.WINDOWHEIGHT))
pygame.display.set_caption("Tower Defense")

# Grid setup
grid = levels_data.level.grid

def redrawGameWindow():
    pygame.draw.rect(win, graphics.BLACK, (0, 0, graphics.WINDOWWIDTH, graphics.WINDOWHEIGHT))
    levels_data.level.draw(win)
    for menu_ in menu.menus:
        menu_.draw(win)
    pygame.display.update()


# Main Loop
clock = pygame.time.Clock()
RUN = True
while RUN:

    clock.tick(levels_data.level.fps)

    #spawn waves alternating between tight and spread out
    waveType = (levels_data.level.waveNumber % 2 == 1)
    levels_data.level.grid.portal.spawnWave(10, 0, tightWave=waveType)
    levels_data.level.grid.portal.spawnEnemy()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False

        # check if the player presses a key
        elif event.type == pygame.KEYDOWN:
            # if the key is escape, deselect current box
            if event.key == pygame.K_ESCAPE:
                if grid.activeBox:
                    grid.activeBox.deactivate()
                    grid.activeBox = None
                    menu.towerInformationMenu.visible = False
                    menu.newTowerMenu.visible = True

            # # Testing configuration
            # elif event.key == pygame.K_e:
            #     levels_data.level.grid.portal.spawnWave(10, 0, tightWave=True)
            # elif event.key == pygame.K_r:
            #     levels_data.level.grid.portal.spawnWave(10, 0, tightWave=False)
            elif event.key == pygame.K_t:
                levels_data.level.changeFPS(1)
            # # if there is a selected box, check if there is player input to update it
            # elif grid.activeBox:
            #     if event.unicode in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            #         grid.activeBox.addTower(int(event.unicode))
            #         menu.towerInformationMenu.updateInfo(grid.activeBox)
            #     elif event.key == pygame.K_BACKSPACE:
            #         grid.activeBox.removeTower()
            #         menu.towerInformationMenu.updateInfo(grid.activeBox)


        # select a box if the user clicks on it
        elif event.type == pygame.MOUSEBUTTONDOWN:
            position = event.pos
            box = grid.getBox(position)
            if box:
                grid.activeBox = box.activate(grid.activeBox)
                if grid.activeBox:
                    if grid.activeBox.tower:
                        menu.newTowerMenu.visible = False
                        menu.towerInformationMenu.visible = True
                        menu.towerInformationMenu.updateInfo(grid.activeBox)
                    else:
                        menu.newTowerMenu.visible = True
                        menu.towerInformationMenu.visible = False
            else:
                for info_menu in menu.menus:
                    if info_menu.visible:
                        for button in info_menu.buttons:
                            if button.isHovered(position):
                                button.activate()

        elif event.type == pygame.MOUSEBUTTONUP:
            position = event.pos
            for info_menu in menu.menus:
                if info_menu.visible:
                    for button in info_menu.buttons:
                        if button.active:
                            button.deactivate()
                            if button.isHovered(position):
                                button.click(grid.activeBox)

    for enemy in levels_data.level.enemies:
        enemy.move(levels_data.level.grid.base)

    for tower in levels_data.level.towers:
        if not tower.target:
            # assign a target to towers that don't have one
            for enemy in levels_data.level.enemies:
                # enemies appear in the same order in the list and on screen
                if tower.isInRange(enemy):
                    tower.target = enemy
                    break
        tower.shoot()

    for bullet in levels_data.level.bullets:
        bullet.move()
        if (bullet.enemy.x - bullet.x)**2 + (bullet.enemy.y - bullet.y)**2 < (bullet.radius + bullet.enemy.radius)**2:
            bullet.hit()

    redrawGameWindow()

pygame.quit()

# delete remaining objects
levels_data.level.deleteData()

print("Done")
