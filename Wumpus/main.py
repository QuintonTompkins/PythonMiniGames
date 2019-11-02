#Author: Quinton Tompkins

import pygame
import readSettings
import Button as btn
import Level as lvl

def main():
    pygame.init()
    
    #set up window size
    display = pygame.display.set_mode(readSettings.getDispWH('Settings.xml'))
    #set window title
    pygame.display.set_caption('Wumpus World')
    #set window icon
    icon = pygame.image.load('images//wumpus_icon.png')
    pygame.display.set_icon(icon)
    
    
    clock = pygame.time.Clock()
    
    #Indicates game is running
    running = True
    #Indicates current room
    room = 'MainMenu'
    #Indicates that the game is changing rooms
    changingRoom = True
    #The background color
    bgcolor = (50,50,50)
    #indicates the mouse clicked somewhere
    mouseclicked = False
    #indicates that an object has moved and the background should redraw
    movement = False
    #Indicates the ai is going to play
    aicontrolled = False

    #Game loop
    while running:
        
        #------------------------------------------------------------
        #Main Menu loop
        #------------------------------------------------------------
        while room == 'MainMenu':
            #$$$$$$$$ Initialize Main Menu variables $$$$$$$$
            if changingRoom:
                playButton = btn.Button(image='images//play_button.png',x=100,y=100)
                aiButton   = btn.Button(image='images//ai_button.png',  x=100,y=200)
                exitButton = btn.Button(image='images//exit_button.png',x=100,y=300)
                #Create background
                #This only needs to be done once unless another sprite moves locations
                display.fill(bgcolor)
                aicontrolled = False
                changingRoom = False
            
            #$$$$$$$$ Draw everything $$$$$$$$
            #Create background
            #This only needs to be done once unless another sprite moves locations
            if movement:
                display.fill(bgcolor)
                movement = False
            
            #display buttons
            playButton.draw(display)
            aiButton.draw(display)
            exitButton.draw(display)
            
            
            #$$$$$$$$ Event check loop $$$$$$$$
            for event in pygame.event.get():
                
                #Escape button is pressed
                if event.type == pygame.QUIT:
                    running = False
                    room = 'None'
                
                #Left mouse button is released
                if event.type == pygame.MOUSEBUTTONUP:
                    mouseclicked = False
                    
                    #Get mouse cordinates
                    x , y = pygame.mouse.get_pos()
                    
                    #Check which button was pressed and act on it
                    if playButton.unclick(x , y):
                        changingRoom = True
                        room = 'GameRoom'
                    
                    elif aiButton.unclick(x , y):
                        changingRoom = True
                        aicontrolled = True
                        room = 'GameRoom'
                        
                    elif exitButton.unclick(x , y):
                        running = False
                        room = 'None'
                
                #Left mouse button is held down
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseclicked = True
            
            
            #$$$$$$$$ Check if button is being hovered by mouse when clicked $$$$$$$$
            if mouseclicked:
                #Get mouse cordinates
                x , y = pygame.mouse.get_pos()
                
                #Check if button is hovered and darken it if it is
                playButton.clicked(x , y)
                aiButton.clicked(x , y)
                exitButton.clicked(x , y)
                
            #$$$$$$$$ If changing rooms then clean up memory, else draw $$$$$$$$
            if changingRoom:
                del playButton , exitButton , aiButton
            else:
                #Update image
                pygame.display.update()
                #frame rate
                clock.tick(60)
        
        
        #------------------------------------------------------------
        #Game Room loop
        #------------------------------------------------------------
        while room == 'GameRoom':
            #$$$$$$$$ Initialize Main Menu variables $$$$$$$$
            if changingRoom:
                backButton = btn.Button(image='images//back_button.png',x=650,y=25)
                winButton = btn.Button(image='images//next_level_button.png',x=200,y=250)
                
                #Create tile image
                tile = pygame.image.load('images//tile.png')
                m = pygame.mask.from_surface(tile, 0)
                shader = pygame.Surface((tile.get_size()), masks=m).convert_alpha()
                shader.fill((150,150,150))
                darktile = tile.copy()
                darktile.blit(shader, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
                del m , shader
                
                #create tile map and get ammo
                level = lvl.Level()
                
                #initialize player stance
                playeraction = 'Walking'
                playeralive = True
                
                #initialize player image and variables
                player = pygame.image.load('images//player.png')
                for i in range(0,10):
                    for k in range(0,10):
                        if level.tiles[k][i][0] == 1:
                           px = i
                           py = k 
                
                #initialize images for other objects
                objects = [ pygame.image.load('images//wumpus_alive.png') , 
                           pygame.image.load('images//pit.png') , 
                           pygame.image.load('images//ladder.png'),
                           pygame.image.load('images//wumpus_dead.png')]
                
                #create text font object
                font = pygame.font.Font('freesansbold.ttf', 20)
                
                #set movement to True to refresh screen
                movement = True
                
                #Check if player or ai is playing and create appropriate buttons
                if aicontrolled:
                    pass
                else:
                    walkButton  = btn.Button(image='images//walk_button.png', x=650,y=290)
                    shootButton = btn.Button(image='images//shoot_button.png',x=650,y=350)
                    
                    upButton    = btn.Button(image='images//up_button.png',   x=675,y=425)
                    downButton  = btn.Button(image='images//down_button.png', x=675,y=525)
                    leftButton  = btn.Button(image='images//left_button.png', x=625,y=475)
                    rightButton = btn.Button(image='images//right_button.png',x=725,y=475)
                
                #Create background
                #This only needs to be done once unless another sprite moves locations
                display.fill(bgcolor)
                changingRoom = False
            
            #$$$$$$$$ Draw everything $$$$$$$$
            #Create background
            #This only needs to be done once unless another sprite moves locations
            if movement:
                display.fill(bgcolor)
                infotext = 'Level: ' + str(level.level) 
                text = font.render(infotext, True, (255, 255, 255)) 
                display.blit(text,(615,90))
                
                infotext = 'Ammo: ' + str(level.ammo) 
                text = font.render(infotext, True, (255, 255, 255)) 
                display.blit(text,(615,120))
                
                infotext = 'Stance: ' + playeraction
                text = font.render(infotext, True, (255, 255, 255)) 
                display.blit(text,(615,150))
                
                infotext = 'Alive: ' + str(playeralive)
                text = font.render(infotext, True, (255, 255, 255)) 
                display.blit(text,(615,180))
                
                infotext = 'Stench: ' + str(level.checkStench(px,py))
                text = font.render(infotext, True, (255, 255, 255)) 
                display.blit(text,(615,210))
                
                infotext = 'Breeze: ' + str(level.checkBreeze(px,py))
                text = font.render(infotext, True, (255, 255, 255)) 
                display.blit(text,(615,240))
                
                #display tiles
                for i in range(0,10):
                    for k in range(0,10):
                        if level.tiles[k][i][1] == 1:
                            display.blit(tile , (i * 50 + 50, k * 50 + 50))
                            if level.tiles[k][i][0] > 1:
                                display.blit(objects[level.tiles[k][i][0] - 2] , (i * 50 + 50, k * 50 + 50))
                        else:
                            display.blit(darktile , (i * 50 + 50, k * 50 + 50))
                    
                display.blit(player,(50 + px * 50,50 + py * 50))
                
                movement = False
            
            #display buttons
            backButton.draw(display)
            
            if level.tiles[py][px][0] == 4:
                winButton.draw(display)
            
            if aicontrolled == False:
                walkButton.draw(display)
                shootButton.draw(display)
                
                upButton.draw(display)
                downButton.draw(display)
                leftButton.draw(display)
                rightButton.draw(display)
            
            
            #$$$$$$$$ Event check loop $$$$$$$$
            for event in pygame.event.get():
                
                #Escape button is pressed
                if event.type == pygame.QUIT:
                    running = False
                    room = 'None'
                
                #Left mouse button is released
                if event.type == pygame.MOUSEBUTTONUP:
                    mouseclicked = False
                    
                    #Get mouse cordinates
                    x , y = pygame.mouse.get_pos()
                    
                    #Check which button was pressed and act on it
                    if backButton.unclick(x , y):
                        changingRoom = True
                        room = 'MainMenu'
                        
                    if level.tiles[py][px][0] == 4 and winButton.unclick(x , y):
                        if level.checkForNextLevel():
                            level.nextLevel()
                            if level.checkForNextLevel() == False:
                                winButton = btn.Button(image='images//win_button.png',x=200,y=250)
                        else:
                            changingRoom = True
                            room = 'MainMenu'
                            
                        for i in range(0,10):
                            for k in range(0,10):
                                if level.tiles[k][i][0] == 1:
                                   px = i
                                   py = k 
                        movement = True
                        
                    if aicontrolled == False and playeralive:
                        #Player control buttons
                        if walkButton.unclick(x , y):
                            playeraction = 'Walking'
                            movement = True
                        
                        if shootButton.unclick(x , y):
                            playeraction = 'Shooting'
                            movement = True
                        
                        #Arrow buttons
                        if upButton.unclick(x , y):
                            if playeraction == 'Walking' and py > 0:
                                py -= 1
                                level.tiles[py][px][1] = 1
                                movement = True
                            elif playeraction == 'Shooting' and level.ammo > 0:
                                level.ammo -= 1
                                if level.tiles[py - 1][px][0] == 2:
                                    level.tiles[py - 1][px][0] = 5
                                movement = True
                        
                        if downButton.unclick(x , y):
                            if playeraction == 'Walking' and py < 9:
                                py += 1
                                level.tiles[py][px][1] = 1
                                movement = True
                            elif playeraction == 'Shooting' and level.ammo > 0:
                                level.ammo -= 1
                                if level.tiles[py + 1][px][0] == 2:
                                    level.tiles[py + 1][px][0] = 5
                                movement = True
                        
                        if leftButton.unclick(x , y):
                            if playeraction == 'Walking' and px > 0:
                                px -= 1
                                level.tiles[py][px][1] = 1
                                movement = True
                            elif playeraction == 'Shooting' and level.ammo > 0:
                                level.ammo -= 1
                                if level.tiles[py][px - 1][0] == 2:
                                    level.tiles[py][px - 1][0] = 5
                                movement = True
                        
                        if rightButton.unclick(x , y):
                            if playeraction == 'Walking' and px < 9:
                                px += 1
                                level.tiles[py][px][1] = 1
                                movement = True
                            elif playeraction == 'Shooting' and level.ammo > 0:
                                level.ammo -= 1
                                if level.tiles[py][px + 1][0] == 2:
                                    level.tiles[py][px + 1][0] = 5
                                movement = True
                
                #Left mouse button is held down
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseclicked = True
            
            
            #$$$$$$$$ Check player state if player moved $$$$$$$$
            if movement:
                if level.tiles[py][px][0] == 2 or level.tiles[py][px][0] == 3:
                    playeralive = False
                
                    
            #$$$$$$$$ Check if button is being hovered by mouse when clicked $$$$$$$$
            if mouseclicked:
                #Get mouse cordinates
                x , y = pygame.mouse.get_pos()
                
                #Check if button is hovered and darken it if it is
                backButton.clicked(x , y)
                
                if level.tiles[py][px][0] == 4:
                    winButton.clicked(x , y)
                
                if aicontrolled == False and playeralive:
                    walkButton.clicked(x , y)
                    shootButton.clicked(x , y)
                    
                    upButton.clicked(x , y)
                    downButton.clicked(x , y)
                    leftButton.clicked(x , y)
                    rightButton.clicked(x , y)
                
            #$$$$$$$$ If changing rooms then clean up memory, else draw $$$$$$$$
            if changingRoom:
                del backButton, tile , darktile , level , winButton
                if aicontrolled == False:
                    del upButton, downButton, leftButton, rightButton, walkButton, shootButton
                    
            else:
                #Update image
                pygame.display.update()
                #frame rate
                clock.tick(60)

    
    #Close the game and exit
    pygame.quit()
    
    
if __name__ == '__main__':
    main()
