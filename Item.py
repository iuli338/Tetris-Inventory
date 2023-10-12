import pygame
import ItemContainer

class Item:

    # Static members
    allItemsVector:list = []
    theHeldItem = None
    rotatedStateWhenPiked = None
    heldItemWhiteImage = None
    heldItemWhiteImagePos = [0,0]
    heldItemWhiteImageVisible = False

    # Hover item name
    pygame.font.init()
    font = pygame.font.Font(None, 26)
    whiteColor = (255, 255, 255) 
    hoverItemText = None

    # Colors
    lightGrayColor = (120,120,120,128)
    hoverColor = (200,200,200,128)
    limePastelColor = (209, 254, 184)

    def __init__(self,itemSizeX,itemSizeY,imagePath,itemName):
        self.itemSizeX = itemSizeX
        self.itemSizeY = itemSizeY
        self.rotated = False
        self.sizeX = (itemSizeX * ItemContainer.ItemContainer.tileSize[0]) + (ItemContainer.ItemContainer.gapBetweenTiles * itemSizeX-1)
        self.sizeY = (itemSizeY * ItemContainer.ItemContainer.tileSize[1]) + (ItemContainer.ItemContainer.gapBetweenTiles * itemSizeY-1)
        self.rect:pygame.rect.Rect = pygame.Rect(0, 0, self.sizeX, self.sizeY)
        self.transparentImage:pygame.surface.Surface = pygame.Surface((self.sizeX,self.sizeY))
        self.transparentImage.set_alpha(128)
        self.transparentImage.fill(Item.lightGrayColor)
        self.lastValidPositon = [0,0]
        self.itemName = itemName
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
        # Draw the hover item white image
        if (Item.theHeldItem is not None) and (Item.heldItemWhiteImageVisible == True):
            screen.blit(Item.heldItemWhiteImage,(Item.heldItemWhiteImagePos[0],Item.heldItemWhiteImagePos[1]))
        # Draw all the items
        for item in Item.allItemsVector:
            #pygame.draw.rect(screen,Item.lightGrayColor,item.rect)
            screen.blit(item.transparentImage,(item.rect.x,item.rect.y))
            if item.image is not None:
                if item.rotated == False:    
                    screen.blit(item.image,(item.rect.x,item.rect.y))
                else:
                    rotatedImage = pygame.transform.rotate(item.image, -90)
                    screen.blit(rotatedImage,(item.rect.x,item.rect.y))

        if Item.hoverItemText is not None and Item.theHeldItem is None:
            x, y = pygame.mouse.get_pos()
            screen.blit(Item.hoverItemText,(x+10,y+20))

    def RotateHeldItem():
        # Swap the X and Y
        temp = Item.theHeldItem.itemSizeX
        Item.theHeldItem.itemSizeX = Item.theHeldItem.itemSizeY
        Item.theHeldItem.itemSizeY = temp
        del temp
        sizeX = (Item.theHeldItem.itemSizeX * ItemContainer.ItemContainer.tileSize[0]) + (ItemContainer.ItemContainer.gapBetweenTiles * Item.theHeldItem.itemSizeX-1)
        sizeY = (Item.theHeldItem.itemSizeY * ItemContainer.ItemContainer.tileSize[1]) + (ItemContainer.ItemContainer.gapBetweenTiles * Item.theHeldItem.itemSizeY-1)
        Item.theHeldItem.sizeX = sizeX
        Item.theHeldItem.sizeY = sizeY
        Item.theHeldItem.rect = pygame.Rect(0, 0, sizeX, sizeY)
        Item.theHeldItem.transparentImage = pygame.Surface((Item.theHeldItem.sizeX,Item.theHeldItem.sizeY))
        Item.theHeldItem.transparentImage.set_alpha(128)
        Item.theHeldItem.transparentImage.fill(Item.lightGrayColor)
        Item.theHeldItem.rotated = ~Item.theHeldItem.rotated
        # Update the white image
        Item.heldItemWhiteImage = pygame.Surface((Item.theHeldItem.sizeX,Item.theHeldItem.sizeY))
        Item.heldItemWhiteImage.set_alpha(60)
        Item.heldItemWhiteImage.fill(Item.limePastelColor)

    def CheckMouseClick(mouseX,mouseY):
        for item in Item.allItemsVector:
            if item.rect.collidepoint(mouseX, mouseY):
                if Item.theHeldItem is item:
                    # Check if the items was rotated but not placed
                    if Item.theHeldItem.rotated != Item.rotatedStateWhenPiked:
                        Item.RotateHeldItem()
                    Item.theHeldItem.rect.x = Item.theHeldItem.lastValidPositon[0]
                    Item.theHeldItem.rect.y = Item.theHeldItem.lastValidPositon[1]
                    Item.theHeldItem = None
                    return
                else:
                    if Item.theHeldItem is None:
                        # Remove the element from its current position
                        Item.allItemsVector.remove(item)
                        # Insert it at the beginning of the list for it to be on top of all items
                        Item.allItemsVector.append(item)
                        Item.theHeldItem = item
                        Item.rotatedStateWhenPiked = item.rotated
                        # Set the hover item white image
                        Item.heldItemWhiteImage = pygame.Surface((Item.theHeldItem.sizeX,Item.theHeldItem.sizeY))
                        Item.heldItemWhiteImage.set_alpha(60)
                        Item.heldItemWhiteImage.fill(Item.limePastelColor)
                        return

    def CheckHeldItemWhiteImagePos():
        if Item.theHeldItem is None:
            return
        for container in ItemContainer.ItemContainer.allContainersVector:
            if container.zone.collidepoint(Item.theHeldItem.rect.x+25,Item.theHeldItem.rect.y+25):
                for tile in container.tilesVector:
                    if tile.collidepoint(Item.theHeldItem.rect.x+25,Item.theHeldItem.rect.y+25):
                        # The held item white image will go to the tiles position
                        Item.heldItemWhiteImagePos[0] = tile.x
                        Item.heldItemWhiteImagePos[1] = tile.y
                        heldItemWhiteImageRect = Item.heldItemWhiteImage.get_rect()
                        heldItemWhiteImageRect.x = tile.x
                        heldItemWhiteImageRect.y = tile.y
                        # It will check if it doesn't touch any red tiles
                        for redTile in container.redTilesVector:
                            if redTile.colliderect(heldItemWhiteImageRect):
                                Item.heldItemWhiteImageVisible = False
                                return
                        # Then will check if it doesn't touch any items
                        for item in Item.allItemsVector:
                            if (item.rect.colliderect(heldItemWhiteImageRect)) and (item is not Item.theHeldItem):
                                Item.heldItemWhiteImageVisible = False
                                return
                        # If everything goes right the visibility is set to True
                        Item.heldItemWhiteImageVisible = True
                        return
            Item.heldItemWhiteImageVisible = False

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
        print ("<< Incercare de plasare cu clickul >>")
        print ("- Exista macar un container si exista un HeldItem")        
        for container in ItemContainer.ItemContainer.allContainersVector:
            if container.zone.collidepoint(Item.theHeldItem.rect.x+25,Item.theHeldItem.rect.y+25):
                for tile in container.tilesVector:
                    if tile.collidepoint(Item.theHeldItem.rect.x+25,Item.theHeldItem.rect.y+25):
                        print("- HeldItem s-a atins de un tile de al unui container")
                        # If touches any item it can't be placed
                        Item.theHeldItem.rect.x = tile.x
                        Item.theHeldItem.rect.y = tile.y
                        # It touches red tile it can't be placed
                        for redTile in container.redTilesVector:
                            if redTile.colliderect(Item.theHeldItem.rect):
                                print("- HeldItem s-a atins de un red tile")
                                Item.theHeldItem.rect.x = Item.theHeldItem.lastValidPositon[0]
                                Item.theHeldItem.rect.y = Item.theHeldItem.lastValidPositon[1]
                                return
                        for item in Item.allItemsVector:
                            if item.rect.colliderect(Item.theHeldItem.rect) and item is not Item.theHeldItem:
                                print("- HeldItem s-a atins de un alt item deci nu poate fi plasat")
                                Item.theHeldItem.rect.x = Item.theHeldItem.lastValidPositon[0]
                                Item.theHeldItem.rect.y = Item.theHeldItem.lastValidPositon[1]
                                return
                        # If it doesn't touch any items it will be placed in the container
                        print ("- Item plasat cu succes")
                        Item.rotatedStateWhenPiked = Item.theHeldItem.rotated
                        Item.theHeldItem.rect.x = tile.x
                        Item.theHeldItem.rect.y = tile.y
                        Item.theHeldItem.lastValidPositon[0] = tile.x
                        Item.theHeldItem.lastValidPositon[1] = tile.y
                        return
        print ("- Itemul nu poate fi plasat")

    def CheckHoverItemName(mouseX,mouseY):
        for item in Item.allItemsVector:
            if item.rect.collidepoint(mouseX,mouseY):
                # Text
                Item.hoverItemText = Item.font.render(item.itemName, True, Item.whiteColor)
                return
        Item.hoverItemText = None

    def CheckGlowOnHold(mouseX,mouseY):
        if Item.theHeldItem is not None:
            if Item.theHeldItem.rect.collidepoint(mouseX,mouseY):
                Item.theHeldItem.transparentImage.fill(Item.whiteColor)
            else:
                Item.theHeldItem.transparentImage.fill(Item.lightGrayColor)
            return
        for item in Item.allItemsVector:
            if item.rect.collidepoint(mouseX,mouseY):
                item.transparentImage.fill(Item.whiteColor)
            else:
                item.transparentImage.fill(Item.lightGrayColor)

    def CheckRPress():
        if (Item.theHeldItem is not None) and (Item.theHeldItem.itemSizeX != Item.theHeldItem.itemSizeY):
            Item.RotateHeldItem()

    def CheckESCPress():
        if Item.theHeldItem is not None:
            # Check if the items was rotated but not placed
            if Item.theHeldItem.rotated != Item.rotatedStateWhenPiked:
                Item.RotateHeldItem()
            Item.theHeldItem.rect.x = Item.theHeldItem.lastValidPositon[0]
            Item.theHeldItem.rect.y = Item.theHeldItem.lastValidPositon[1]
            Item.theHeldItem = None

    def CheckAllKeyPress(key):
        if key == pygame.K_r:
            Item.CheckRPress()
        if key == pygame.K_ESCAPE:
            Item.CheckESCPress()



