import pygame
import sys
# My modules
import ItemContainer as ITC
import Item as IT
import RightClickMenu as RCM
import InspectWindow as IW
import Button as BT

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tetris Inventory")

# Create one container
container1 = ITC.ItemContainer("Container 1",6,6,20,20)
container2 = ITC.ItemContainer("Container 2",3,3,480,150)
container1.SetPosition(150,150)
# Create item
item1 = IT.Item(3,3,"backpack.png","Backpack")
item2 = IT.Item(2,2,"armor.png","Armor")
item3 = IT.Item(3,1,"shotgun.png","Shotgun")
item4 = IT.Item(1,1,"pistol.png","Pistol 9mm")
item5 = IT.Item(1,1,"pistol.png","Pistol 9mm")
item6 = IT.Item(2,2,"medkit.png","Medkit")
item7 = IT.Item(1,1,"pistolMag.png","Pistol Ammo")
# Add the items in the container
container1.TryAddItemInCont(item1)
container1.TryAddItemInCont(item4)
container1.TryAddItemInCont(item5)
container2.TryAddItemInCont(item2)
container2.TryAddItemInCont(item3)
container1.TryAddItemInCont(item6)
container2.TryAddItemInCont(item7)

# Test
#button1 = RCM.RightClickMenu.Button(0,0,"Click me")
RCM.RightClickMenu.Init()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check mouse click
            if pygame.mouse.get_pressed()[0]:
                IT.Item.CheckIfCanPlace()
                # Get the mouse position
                mouseX, mouseY = pygame.mouse.get_pos()
                IT.Item.CheckMouseClick(mouseX,mouseY)
                RCM.RightClickMenu.CheckLeftClick(mouseX,mouseY)
                IW.InspectWindow.CheckCloseButton(mouseX,mouseY)
                ITC.ItemContainer.CheckDropAllButton(mouseX,mouseY)
            if pygame.mouse.get_pressed()[2]:
                RCM.RightClickMenu.CheckRightClick(mouseX,mouseY)

        if event.type == pygame.KEYDOWN:
            IT.Item.CheckAllKeyPress(event.key)
            RCM.RightClickMenu.CheckAllKeyPress(event.key)

    # Check item follow mouse
    mouseX, mouseY = pygame.mouse.get_pos()
    IT.Item.ItemFollowMouse(mouseX,mouseY)
    # Check hover item name text
    IT.Item.CheckHoverItemName(mouseX,mouseY)
    # Check item hover glow
    IT.Item.CheckGlowOnHold(mouseX,mouseY)
    # Check hover item white image
    IT.Item.CheckHeldItemWhiteImagePos()
    # Check button hober glow
    BT.Button.CheckGlowOnHold(mouseX,mouseY)

    # Clear the screen
    screen.fill((0, 0, 0))
    
    # Draw the container
    ITC.ItemContainer.Draw(screen)
    IT.Item.Draw(screen)
    RCM.RightClickMenu.Draw(screen)
    IW.InspectWindow.Draw(screen)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()