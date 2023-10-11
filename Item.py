import pygame
import ItemContainer

class Item:

    # Static members
    allItemsVector:list = []
    theHeldItem = None

    # Colors
    lightGrayColor = (120,120,120,50)

    def __init__(self,itemSizeX,itemSizeY,imagePath):
        self.itemSizeX = itemSizeX
        self.itemSizeY = itemSizeY
        self.sizeX = (itemSizeX * ItemContainer.ItemContainer.tileSize[0]) + (ItemContainer.ItemContainer.gapBetweenTiles * itemSizeX-1)
        self.sizeY = (itemSizeY * ItemContainer.ItemContainer.tileSize[1]) + (ItemContainer.ItemContainer.gapBetweenTiles * itemSizeY-1)
        self.rect:pygame.rect.Rect = pygame.Rect(0, 0, self.sizeX, self.sizeY)
        self.lastValidPositon = [0,0]
        # Load the item image
        try:
            # Load the image
            self.image = pygame.image.load(imagePath)
        except pygame.error as e:
            print("Failed to load the image:", e)
            self.image = None
        # Addes this instance to the vector
        Item.allItemsVector.append(self)

    def Draw(screen:pygame.surface.Surface):
        if len(Item.allItemsVector) == 0:
            return
        for item in Item.allItemsVector:
            pygame.draw.rect(screen,Item.lightGrayColor,item.rect)
            if item.image is not None:
                screen.blit(item.image,(item.rect.x,item.rect.y))

    def CheckMouseClick(mouseX,mouseY):
        for item in Item.allItemsVector:
            if item.rect.collidepoint(mouseX, mouseY):
                if Item.theHeldItem is item:
                    Item.theHeldItem.rect.x = Item.theHeldItem.lastValidPositon[0]
                    Item.theHeldItem.rect.y = Item.theHeldItem.lastValidPositon[1]
                    Item.theHeldItem = None
                    return
                else:
                    if Item.theHeldItem is None:
                        # Remove the element from its current position
                        Item.allItemsVector.remove(item)
                        # Insert it at the beginning of the list
                        Item.allItemsVector.append(item)
                        Item.theHeldItem = item
                        return

    def ItemFollowMouse(mouseX,mouseY):
        if Item.theHeldItem is None:
            return
        Item.theHeldItem.rect.x = mouseX - int(Item.theHeldItem.rect.width//2)
        Item.theHeldItem.rect.y = mouseY - int(Item.theHeldItem.rect.height//2)

    def CheckIfCanPlace():
        if len(ItemContainer.ItemContainer.allContainersVector) == 0:
            return
        if Item.theHeldItem is None:
            return
        print ("Exista macar un container si exista un HeldItem")
        for container in ItemContainer.ItemContainer.allContainersVector:
            for tile in container.tilesVector:
                if tile.collidepoint(Item.theHeldItem.rect.x+25,Item.theHeldItem.rect.y+25):
                    print("HeldItem s-a atins de un tile de al unui container")
                    # If touches any item it can't be placed
                    Item.theHeldItem.rect.x = tile.x
                    Item.theHeldItem.rect.y = tile.y
                    # It touches red tile it can't be placed
                    for container in ItemContainer.ItemContainer.allContainersVector:
                        for redTile in container.redTilesVector:
                            if redTile.colliderect(Item.theHeldItem.rect):
                                print("HeldItem s-a atins de un red tile")
                                Item.theHeldItem.rect.x = Item.theHeldItem.lastValidPositon[0]
                                Item.theHeldItem.rect.y = Item.theHeldItem.lastValidPositon[1]
                                return
                    for item in Item.allItemsVector:
                        if item.rect.colliderect(Item.theHeldItem.rect) and item is not Item.theHeldItem:
                            print("HeldItem s-a atins de un alt item deci nu poate fi plasat")
                            Item.theHeldItem.rect.x = Item.theHeldItem.lastValidPositon[0]
                            Item.theHeldItem.rect.y = Item.theHeldItem.lastValidPositon[1]
                            return
                    # If it doesn't touch any items it will be placed in the container
                    Item.theHeldItem.rect.x = tile.x
                    Item.theHeldItem.rect.y = tile.y
                    Item.theHeldItem.lastValidPositon[0] = tile.x
                    Item.theHeldItem.lastValidPositon[1] = tile.y
                    return

