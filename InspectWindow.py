import pygame
import Button

class InspectWindow:
    inspectedItemImage = None
    scaledImage = None
    windowTransparentImage = None
    sizeX = None
    sizeY = None
    posX = None
    posY = None
    grayColor = (40,40,40)
    #
    closeButton = Button.Button(0,0,"X")

    @staticmethod
    def OpenInspect(item):
        InspectWindow.inspectedItemImage = item.image
        InspectWindow.sizeX = int(item.image.get_rect().width * 2)
        InspectWindow.sizeY = int(item.image.get_rect().height * 2)
        windowSizeX, windowSizeY = pygame.display.get_surface().get_size()
        InspectWindow.posX = (windowSizeX//2) - (InspectWindow.sizeX//2)
        InspectWindow.posY = (windowSizeY//2) - (InspectWindow.sizeY//2)
        #InspectWindow.windowTransparentImage = pygame.Rect(InspectWindow.posX,InspectWindow.posY,InspectWindow.sizeX,InspectWindow.sizeY)
        InspectWindow.windowTransparentImage = pygame.Surface((InspectWindow.sizeX+40,InspectWindow.sizeY+40))
        InspectWindow.windowTransparentImage.set_alpha(200)
        InspectWindow.windowTransparentImage.fill(InspectWindow.grayColor)

        # Use the pygame.transform.scale() function to scale the image
        InspectWindow.scaledImage = pygame.transform.scale(InspectWindow.inspectedItemImage, (InspectWindow.sizeX, InspectWindow.sizeY))
        # Set the right position of the button to the right upper corner
        posX = InspectWindow.posX + InspectWindow.sizeX - InspectWindow.closeButton.rect.width
        posY = InspectWindow.posY
        InspectWindow.closeButton.SetPosition(posX+20,posY-20)

    def CheckCloseButton(mouseX,mouseY):
        if InspectWindow.closeButton.rect.collidepoint(mouseX,mouseY) and InspectWindow.inspectedItemImage is not None:
            InspectWindow.CloseInspect()

    @staticmethod
    def CloseInspect():
        InspectWindow.inspectedItemImage= None

    @staticmethod
    def Draw(screen):
        if InspectWindow.inspectedItemImage is not None:
            screen.blit(InspectWindow.windowTransparentImage,(InspectWindow.posX-20,InspectWindow.posY-20))
            screen.blit(InspectWindow.scaledImage,(InspectWindow.posX,InspectWindow.posY))
            Button.Button.DrawButton(screen,InspectWindow.closeButton)