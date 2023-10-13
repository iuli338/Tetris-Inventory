import pygame

class Button:
        backImage = None
        text = None
        textObj = None
        allButtonsVector = []
        #
        pygame.font.init()
        font = pygame.font.Font(None, 26)
        whiteColor = (255, 255, 255)
        grayColor = (40,40,40)
        lightGrayColor = (120,120,120)

        def __init__(self,posX,posY,text):
            self.text = text
            self.posX = posX
            self.posY = posY
            #
            self.textObj = Button.font.render(self.text, True, Button.whiteColor)
            sizeX, sizeY = self.textObj.get_size()
            # BackImage
            self.backImage = pygame.Surface((sizeX+10,sizeY+10))
            self.backImage.set_alpha(128)
            self.backImage.fill(Button.grayColor)
            #
            self.rect = pygame.Rect(self.posX, self.posY, sizeX+10, sizeY+10)
            Button.allButtonsVector.append(self)

        @staticmethod
        def DrawButton(screen,button):
            screen.blit(button.backImage,(button.posX,button.posY))
            screen.blit(button.textObj,(button.posX+5, button.posY+5))

        @staticmethod
        def CheckGlowOnHold(mouseX,mouseY):
            for button in Button.allButtonsVector:
                if button.rect.collidepoint(mouseX, mouseY):
                    button.backImage.set_alpha(200)
                    button.backImage.fill(Button.lightGrayColor)
                else:
                    button.backImage.set_alpha(200)
                    button.backImage.fill(Button.grayColor)

        def SetPosition(self,newX,newY):
            self.posX = newX
            self.posY = newY
            self.rect.x = newX
            self.rect.y = newY

