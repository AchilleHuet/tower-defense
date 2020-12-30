import pygame
import graphics
from tower import Tower
import levels_data


class Menu():

    def __init__(self, x, y, width, height, title, color = graphics.GRAY, textColor = graphics.WHITE, visible = False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title
        self.textColor = textColor
        self.text = graphics.TITLEFONT.render(title, 1, self.textColor)
        self.xText = self.x + (self.width - self.text.get_width()) //2
        self.yText = self.y + 10
        self.buttons = []
        self.texts = []
        self.color = color
        self.visible = visible

    def draw(self, win):
        """
        Draws the menu and all of its buttons if they are meant to be visible
        """
        if self.visible:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
            win.blit(self.text, (self.xText, self.yText))
            for button in self.buttons:
                button.draw(win)
            for text in self.texts:
                text.draw(win)

    def addButton(self, button):
        """
        Adds a button to the menu
        """
        button.x += self.x
        button.y += self.y
        button.xText += self.x
        button.yText += self.y
        self.buttons.append(button)
        button.menu = self

    def addText(self, text):
        """
        Adds a textbox to the menu
        """
        text.x += self.x
        text.y += self.y
        self.texts.append(text)
        text.menu = self

    def isHovered(self, pos):
        """
        Returns a boolean indicating whether the mouse is on the selected button
        """
        x, y = pos
        if x > self.x and x < self.x + self.width:
            if y > self.y and y < self.y + self.height:
                return True
        return False

    def toggle(self):
        self.visible = not self.visible
    
    def makeVisible(self):
        self.visible = True

    def makeInvisible(self):
        self.visible = False

    def update(self):
        pass


class Button():

    def __init__(self, x, y, width, height, text, color=graphics.BLUE, textColor=graphics.BLACK):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        # used to change the color of the button when active
        self.activeColor = (max(self.color[0] - 50, 0),
                            max(self.color[1] - 50, 0),
                            max(self.color[2] - 50, 0))
        self.textColor = textColor
        self.text = graphics.FONT.render(text, 1, self.textColor)
        self.xText = self.x + (self.width - self.text.get_width()) //2
        self.yText = self.y + (self.height - self.text.get_height()) //2
        self.active = False
        self.menu = None

    def draw(self, win):
        """
        Draws the button on the screen
        """
        # change the color of the button if the button is active
        if self.active:
            pygame.draw.rect(win, self.activeColor, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        win.blit(self.text, (self.xText, self.yText))

    def isHovered(self, pos):
        """
        Returns a boolean indicating whether the mouse is on the selected button
        """
        x, y = pos
        if x > self.x and x < self.x + self.width:
            if y > self.y and y < self.y + self.height:
                return True
        return False

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def click(self, box):
        pass


class ExitButton(Button):

    def click(self, box):
        self.menu.makeInvisible()


class UpgradeButton(Button):

    def click(self, box):
        if box:
            box.tower.upgrade()
            self.menu.updateInfo(box)

class SellButton(Button):

    def click(self, box):
        if box:
            box.tower.sell()
            box.removeTower()
            self.menu.makeInvisible()
            newTowerMenu.makeVisible()

class NewTowerButton(Button):

    width = 40
    height = 40

    def __init__(self, x, y, towerType):
        self.towerType = towerType
        self.cost = Tower.towerData[towerType]["baseCost"]
        super().__init__(x, y, NewTowerButton.width, NewTowerButton.height, text=str(self.cost), color=Tower.towerData[towerType]["color"])

    def click(self, box):
        # add tower if non-existant, remove gold and show the information menu
        if box and not box.tower and levels_data.level.gold >= self.cost:
            box.addTower(self.towerType)
            levels_data.level.gold -= self.cost
            newTowerMenu.makeInvisible()
            towerInformationMenu.updateInfo(box)
            towerInformationMenu.makeVisible()



class Text():

    def __init__(self, x, y, text, color):
        self.x = x
        self.y = y
        self.color = color
        self.text = graphics.FONT.render(text, 1, self.color)
        self.menu = None

    def draw(self, win):
        """
        Adds the text on the screen
        """
        win.blit(self.text, (self.x, self.y))
 
    def updateText(self, newText):
        self.text = graphics.FONT.render(newText, 1, self.color)


class InformationMenu(Menu):

    width = 200

    def __init__(self, windowWidth, windowHeight):
        super().__init__(x=windowWidth - InformationMenu.width,
                         y=0,
                         width=InformationMenu.width,
                         height=windowHeight,
                         title="Information",
                         visible=False)


class TowerInformationMenu(InformationMenu):

    def __init__(self, windowWidth, windowHeight):
        super().__init__(windowWidth, windowHeight)
        self.levelInfo = Text(20, 40, "", graphics.WHITE)
        self.typeInfo = Text(20, 70, "", graphics.WHITE)
        self.damageInfo = Text(20, 100, "", graphics.WHITE)
        self.rangeInfo = Text(20, 130, "", graphics.WHITE)
        self.upgradeInfo = Text(20, 160, "", graphics.WHITE)
        self.sellInfo = Text(20, 190, "", graphics.WHITE)
        self.addText(self.levelInfo)
        self.addText(self.typeInfo)
        self.addText(self.damageInfo)
        self.addText(self.rangeInfo)
        self.addText(self.upgradeInfo)
        self.addText(self.sellInfo)
        upgradeButton = UpgradeButton((self.width - 100)//2, 230, 100, 30, "Upgrade")
        sellButton = SellButton((self.width - 100)//2, 270, 100, 30, "Sell", color=graphics.RED)
        self.addButton(upgradeButton)
        self.addButton(sellButton)


    def updateInfo(self, box):
        if box and box.tower:
            self.levelInfo.updateText("Tower level: {}".format(int(box.tower.level)))
            self.typeInfo.updateText("Tower type: {}".format(box.tower.type))
            self.damageInfo.updateText("Tower damage: {}".format(int(box.tower.damage)))
            self.rangeInfo.updateText("Tower range: {}".format(int(box.tower.range)))
            self.upgradeInfo.updateText("Upgrade cost: {}".format(int(box.tower.upgradeCost)))
            self.sellInfo.updateText("Sell value: {}".format(int(box.tower.sellValue)))
            box.showRange = True
        else:
            self.levelInfo.updateText("")
            self.typeInfo.updateText("")
            self.damageInfo.updateText("")
            self.rangeInfo.updateText("")
            self.upgradeInfo.updateText("")
            self.sellInfo.updateText("")


class NewTowerMenu(InformationMenu):

    width = 200
    def __init__(self, windowWidth, windowHeight):
        super().__init__(windowWidth, windowHeight)
        newTower1Button = NewTowerButton(20, 60, 1)
        newTower2Button = NewTowerButton(80, 60, 2)
        self.addButton(newTower1Button)
        self.addButton(newTower2Button)
        self.makeVisible()


class PausePlayButton(Button):

    def click(self, box):
        if levels_data.level.speed_modifier == 0:
            levels_data.level.changeSpeed(1)
            self.text = self.text = graphics.FONT.render("||", 1, self.textColor)            
        else:
            levels_data.level.changeSpeed(0)
            self.text = graphics.FONT.render("|>", 1, self.textColor)

class SpeedManagerButton(Button):

    def click(self, box):
        if levels_data.level.speed_modifier == 1:
            levels_data.level.changeSpeed(2)
            self.text = self.text = graphics.FONT.render(">>", 1, self.textColor)
            self.xText = self.x + (self.width - self.text.get_width()) //2
            self.yText = self.y + (self.height - self.text.get_height()) //2
        elif levels_data.level.speed_modifier == 2:
            levels_data.level.changeSpeed(3)
            self.text = self.text = graphics.FONT.render(">>>", 1, self.textColor)
            self.xText = self.x + (self.width - self.text.get_width()) //2
            self.yText = self.y + (self.height - self.text.get_height()) //2
        else:
            levels_data.level.changeSpeed(1)
            self.text = graphics.FONT.render(">", 1, self.textColor)
            self.xText = self.x + (self.width - self.text.get_width()) //2
            self.yText = self.y + (self.height - self.text.get_height()) //2

class OptionsButton(Button):

    def click(self, box):
        optionsMenu.makeVisible()


class SpeedManagerMenu(Menu):

    height = 70

    def __init__(self, windowWidth, windowHeight):
        super().__init__(x=0,
                         y=windowHeight - SpeedManagerMenu.height,
                         width=windowWidth - InformationMenu.width,
                         height=SpeedManagerMenu.height,
                         title="",
                         color = graphics.BLACK,
                         visible=True)
        pause_button = PausePlayButton(10, 10, 50, 50, "||")
        speed_manager_button = SpeedManagerButton(70, 10, 50, 50, ">")
        options_button = OptionsButton(self.width - 80, 10, 70, 50, "Options")
        self.addButton(pause_button)
        self.addButton(speed_manager_button)
        self.addButton(options_button)


class ResumeButton(Button):

    def click(self, box):
        self.menu.makeInvisible()
        levels_data.level.changeSpeed(1)

class RestartButton(Button):

    def click(self, box):
        self.menu.makeInvisible()
        levels_data.level.changeSpeed(1)
        levels_data.level.reset()



class OptionsMenu(Menu):

    width = 400
    height = 400

    def __init__(self, windowWidth, windowHeight):
        super().__init__(x=(windowWidth - OptionsMenu.width)//2,
                         y=(windowHeight - OptionsMenu.height)//2,
                         width=OptionsMenu.width,
                         height=OptionsMenu.height,
                         title="Options",
                         color = graphics.GRAY,
                         visible=False)
        resume_button = ResumeButton(100, 150, 200, 50, 'Resume')
        restart_button = RestartButton(100, 220, 200, 50, 'Restart')
        self.addButton(resume_button)
        self.addButton(restart_button)

    def makeVisible(self):
        levels_data.level.changeSpeed(0)
        self.visible = True


# Information menu setup
menus = []
towerInformationMenu = TowerInformationMenu(graphics.WINDOWWIDTH, graphics.WINDOWHEIGHT)
newTowerMenu = NewTowerMenu(graphics.WINDOWWIDTH, graphics.WINDOWHEIGHT)
speedManagerMenu = SpeedManagerMenu(graphics.WINDOWWIDTH, graphics.WINDOWHEIGHT)
optionsMenu = OptionsMenu(graphics.WINDOWWIDTH, graphics.WINDOWHEIGHT)
menus.append(towerInformationMenu)
menus.append(newTowerMenu)
menus.append(speedManagerMenu)
menus.append(optionsMenu)
