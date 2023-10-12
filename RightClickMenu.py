import pygame
import Item

class RightClickMenu:
    # Static members
    pygame.font.init()
    font = pygame.font.Font(None, 26)
    whiteColor = (255, 255, 255)
    grayColor = (40,40,40)
    lightGrayColor = (120,120,120)
    #
    MenuButtonsVector = []
    InspectButton = None
    DropButton = None
    #
    isMenuVisible = False
    #
    clickedItem = None

    class Button:
        backImage = None
        text = None
        textObj = None
        allButtonsVector = []

        def __init__(self,posX,posY,text):
            self.text = text
            self.posX = posX
            self.posY = posY
            #
            self.textObj = RightClickMenu.font.render(self.text, True, RightClickMenu.whiteColor)
            sizeX, sizeY = self.textObj.get_size()
            # BackImage
            self.backImage = pygame.Surface((sizeX+10,sizeY+10))
            self.backImage.set_alpha(128)
            self.backImage.fill(RightClickMenu.grayColor)
            #
            self.rect = pygame.Rect(self.posX, self.posY, sizeX+10, sizeY+10)
            RightClickMenu.Button.allButtonsVector.append(self)

        def Draw(screen):
           if RightClickMenu.isMenuVisible == False:
               return
           for button in RightClickMenu.Button.allButtonsVector:
               screen.blit(button.backImage,(button.posX,button.posY))
               screen.blit(button.textObj,(button.posX+5, button.posY+5))

        def CheckGlowOnHold(mouseX,mouseY):
            for button in RightClickMenu.Button.allButtonsVector:
                if button.rect.collidepoint(mouseX, mouseY):
                    button.backImage.set_alpha(200)
                    button.backImage.fill(RightClickMenu.lightGrayColor)
                else:
                    button.backImage.set_alpha(200)
                    button.backImage.fill(RightClickMenu.grayColor)

    def Init():
        RightClickMenu.InspectButton = RightClickMenu.Button(0,0,"Inspect")
        RightClickMenu.DropButton = RightClickMenu.Button(0,50,"Drop")
        RightClickMenu.MenuButtonsVector.append(RightClickMenu.InspectButton)
        RightClickMenu.MenuButtonsVector.append(RightClickMenu.DropButton)
        
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