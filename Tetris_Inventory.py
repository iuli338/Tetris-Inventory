import pygame
import sys
# My modules
import ItemContainer as ITC
import Item as IT

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tetris Inventory")

# Create one container
container1 = ITC.ItemContainer("Container 1",6,6,20,20)
container2 = ITC.ItemContainer("Container 2",3,3,550,200)
container1.SetPosition(150,200)
# Create item
item1 = IT.Item(3,3,"backpack.png","Backpack")
item2 = IT.Item(2,2,"armor.png","Armor")
item3 = IT.Item(3,1,"shotgun.png","Shotgun")
item4 = IT.Item(1,1,"pistol.png","Pistol 9mm")

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

    # Check item follow mouse
    mouseX, mouseY = pygame.mouse.get_pos()
    IT.Item.ItemFollowMouse(mouseX,mouseY)

    # Check hover item name text
    IT.Item.CheckHoverItemName(mouseX,mouseY)

    # Clear the screen
    screen.fill((0, 0, 0))
    
    # Draw the container
    ITC.ItemContainer.Draw(screen)
    IT.Item.Draw(screen)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()