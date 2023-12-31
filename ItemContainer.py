import pygame
import Item
from Button import Button
from Interface3 import GetIfRightClickMenuVisible

class ItemContainer:

    # Static Members
    grayColor = (40,40,40)
    redColor = (250,128,114)
    tileSize = (50,50)
    gapBetweenTiles = 2
    tile:pygame.rect.Rect = pygame.Rect(0, 0, tileSize[0], tileSize[1])
        # Text
    pygame.font.init()
    font = pygame.font.Font(None, 30)
    whiteColor = (255, 255, 255)
        #
    allContainersVector:list = []
        #
    redTile:pygame.rect.Rect = pygame.Rect(0, 0, tileSize[0], tileSize[1])

    def __init__(self,name:str,sizeX:int,sizeY:int,posX:float,posY:float) -> None:
        self.sizeX =  sizeX
        self.sizeY = sizeY
        self.posX = posX
        self.posY = posY
        self.tilesVector = []
        self.redTilesVector:list = []
        self.name = name
        zoneSizeX = (sizeX * ItemContainer.tileSize[0]) + (ItemContainer.gapBetweenTiles * sizeX-1)
        zoneSizeY = (sizeY * ItemContainer.tileSize[1]) + (ItemContainer.gapBetweenTiles * sizeY-1)
        self.zone = pygame.Rect(posX,posY,zoneSizeX,zoneSizeY)
        # Iterate and set each tile their correct position to form an 2D array
        for i in range(sizeY):
            for j in range(sizeX):
                tile:pygame.rect.Rect = ItemContainer.tile.copy()
                tile.x = posX + (j * (ItemContainer.tileSize[0] + ItemContainer.gapBetweenTiles))
                tile.y = posY + (i * (ItemContainer.tileSize[1] + ItemContainer.gapBetweenTiles))
                self.tilesVector.append(tile)
        # Generating red zone
        for i in range(sizeY+2):
            for j in range(sizeX+2):
                if i == 0 or i == sizeX+2 - 1 or j == 0 or j == sizeY+2 - 1:
                    redTile:pygame.rect.Rect = ItemContainer.redTile.copy()
                    redTile.x = (posX - (ItemContainer.tileSize[0] + ItemContainer.gapBetweenTiles)) + (j * (ItemContainer.tileSize[0] + ItemContainer.gapBetweenTiles))
                    redTile.y = (posY - (ItemContainer.tileSize[1] + ItemContainer.gapBetweenTiles)) + (i * (ItemContainer.tileSize[1] + ItemContainer.gapBetweenTiles))
                    self.redTilesVector.append(redTile)
        # Text
        self.text = ItemContainer.font.render(name, True, ItemContainer.whiteColor)
        #
        ItemContainer.allContainersVector.append(self)
        # Drop All button
        self.dropAllButton:Button = Button(self.posX,self.posY + zoneSizeY + 10,"[Drop all]")

    def Draw(screen:pygame.surface.Surface):
        if len(ItemContainer.allContainersVector) == 0:
            return
        for container in ItemContainer.allContainersVector:
            # Iterate and draw all the tiles from the vector
            for tile in container.tilesVector:
                pygame.draw.rect(screen,ItemContainer.grayColor,tile)
            # Draw the red tiles
            #for redTile in container.redTilesVector:
            #   pygame.draw.rect(screen,ItemContainer.redColor,redTile)
            # Draw the text
            screen.blit(container.text, (container.posX, container.posY - 30))
            # Draw the zone
            #pygame.draw.rect(screen,ItemContainer.grayColor,container.zone)
            # Draw drop all button
            Button.DrawButton(screen,container.dropAllButton)

    def SetPosition(self,newPosX:float,newPosY:float):
        self.posX = newPosX
        self.posY = newPosY
        index = 0
        for i in range(self.sizeY):
            for j in range(self.sizeX):
                tile = self.tilesVector[index]
                tile.x = self.posX + (j * (ItemContainer.tileSize[0] + ItemContainer.gapBetweenTiles))
                tile.y = self.posY + (i * (ItemContainer.tileSize[1] + ItemContainer.gapBetweenTiles))
                index += 1
        # Move the red tiles
        self.redTilesVector.clear()
        for i in range(self.sizeY+2):
            for j in range(self.sizeX+2):
                if i == 0 or i == self.sizeX+2 - 1 or j == 0 or j == self.sizeY+2 - 1:
                    redTile:pygame.rect.Rect = ItemContainer.redTile.copy()
                    redTile.x = (self.posX - (ItemContainer.tileSize[0] + ItemContainer.gapBetweenTiles)) + (j * (ItemContainer.tileSize[0] + ItemContainer.gapBetweenTiles))
                    redTile.y = (self.posY - (ItemContainer.tileSize[1] + ItemContainer.gapBetweenTiles)) + (i * (ItemContainer.tileSize[1] + ItemContainer.gapBetweenTiles))
                    self.redTilesVector.append(redTile)
        # Move the zone
        self.zone.x = newPosX
        self.zone.y = newPosY
        # Move the drop all button
        zoneSizeY = (self.sizeY * ItemContainer.tileSize[1]) + (ItemContainer.gapBetweenTiles * self.sizeY-1)
        self.dropAllButton.SetPosition(self.posX,self.posY + zoneSizeY + 10)

    def GetPos(self):
        return list((int(self.posX),int(self.posY)))

    def TryAddItemInCont (self,itemToAdd:Item.Item):
        print ("<< Incercare de plasare prin comanda >>")
        if len(ItemContainer.allContainersVector) == 0:
            return
        for tile in self.tilesVector:
            itemToAdd.rect.x = tile.x
            itemToAdd.rect.y = tile.y
            # It touches red tile it can't be placed
            touchesRedTile = False
            touchesOtherItems = False
            for redTile in self.redTilesVector:
                if redTile.colliderect(itemToAdd.rect):
                    #print("- HeldItem s-a atins de un red tile")
                    itemToAdd.rect.x = 0
                    itemToAdd.rect.y = 0
                    touchesRedTile = True
                    break
            # If touches any item it can't be placed
            for item in Item.Item.allItemsVector:
                if item.rect.colliderect(itemToAdd.rect) and item is not itemToAdd:
                    #print("- HeldItem s-a atins de un alt item deci nu poate fi plasat")
                    itemToAdd.rect.x = 0
                    itemToAdd.rect.y = 0
                    touchesOtherItems = True
                    break
            # If it doesn't touch any item or red tile it will be placed in the container
            if (touchesRedTile == False and touchesOtherItems == False):
                itemToAdd.rect.x = tile.x
                itemToAdd.rect.y = tile.y
                itemToAdd.lastValidPositon[0] = tile.x
                itemToAdd.lastValidPositon[1] = tile.y
                itemToAdd.inWichContainer = self
                print ("Itemul [" + itemToAdd.itemName + "] a fost adaugat in containerul [" + self.name + "].")
                return
        print ("Itemul nu a putut fi introdus in container.")

    def CheckDropAllButton(mouseX,mouseY):
        if len(Item.Item.allItemsVector) == 0:
            return
        if GetIfRightClickMenuVisible() == True:
            return
        containerToCheck:ItemContainer = None
        for container in ItemContainer.allContainersVector:
            if container.dropAllButton.rect.collidepoint(mouseX,mouseY):
                containerToCheck = container
                break;
        if containerToCheck is None:
            return
        print("<< Incercare de sterge a tuturor itemelor dintr-un container >>")
        for item in Item.Item.allItemsVector:
            if item.inWichContainer is containerToCheck:
                item.DropItem()
        print (f"[Au fost sterse toate itemele din containerul {containerToCheck.name}]")

