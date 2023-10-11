from tokenize import String
import pygame

class ItemContainer:

    # Static Members
    grayColor = (40,40,40)
    redColor = (250,128,114)
    tileSize = (50,50)
    gapBetweenTiles = 2
    pygame.font.init()
    tile:pygame.rect.Rect = pygame.Rect(0, 0, tileSize[0], tileSize[1])
        # Text
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

    def GetPos(self):
        return list((int(self.posX),int(self.posY)))
