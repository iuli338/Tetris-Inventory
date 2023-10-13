import pygame
import Item
from Interface2 import OpenInspect
from Interface2 import GetInspectedItemImage
import Button

class RightClickMenu:
    # Static members
    MenuButtonsVector = []
    InspectButton = None
    DropButton = None
    #
    isMenuVisible = False
    #
    clickedItem = None

    @staticmethod
    def Init():
        RightClickMenu.InspectButton = Button.Button(0,0,"Inspect")
        RightClickMenu.DropButton = Button.Button(0,50,"Drop")
        RightClickMenu.MenuButtonsVector.append(RightClickMenu.InspectButton)
        RightClickMenu.MenuButtonsVector.append(RightClickMenu.DropButton)
        
    def Draw(screen):
        if RightClickMenu.isMenuVisible == False:
            return
        Button.Button.DrawButton(screen,RightClickMenu.InspectButton)
        Button.Button.DrawButton(screen,RightClickMenu.DropButton)

    def SetPosition(newPosX,newPosY):
        Yincrement = 0
        for button in RightClickMenu.MenuButtonsVector:
            button.rect.x = newPosX
            button.rect.y = newPosY + Yincrement
            button.posX = newPosX
            button.posY = newPosY + Yincrement
            #
            sizeX, sizeY = button.textObj.get_size()
            Yincrement += sizeY + 10 + 2

    def CheckRightClick(mouseX,mouseY):
        if Item.Item.theHeldItem is not None:
            return
        if GetInspectedItemImage() is not None:
            return

        for item in Item.Item.allItemsVector:
            if item.rect.collidepoint(mouseX, mouseY):
                RightClickMenu.clickedItem = item
                RightClickMenu.isMenuVisible = True
                RightClickMenu.SetPosition(mouseX+10,mouseY+20)
                return
        RightClickMenu.clickedItem = None
        RightClickMenu.isMenuVisible = False

    def CloseMenu():
        RightClickMenu.isMenuVisible = False
        RightClickMenu.clickedItem = None

    def CheckESCPress():
        RightClickMenu.CloseMenu()

    def CheckAllKeyPress(key):
        if key == pygame.K_ESCAPE:
            RightClickMenu.CheckESCPress()

    def CheckLeftClick(mouseX,mouseY):
        if RightClickMenu.isMenuVisible == False:
            return
        # Inspect button
        if RightClickMenu.InspectButton.rect.collidepoint(mouseX, mouseY):
            OpenInspect(RightClickMenu.clickedItem)
            RightClickMenu.CloseMenu()
