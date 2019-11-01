#Author: Quinton Tompkins

import pygame
import readSettings
import Button as btn

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
                backButton = btn.Button(image='images//back_button.png',x=650,y=50)
                
                #Check if player or ai is playing and create appropriate buttons
                if aicontrolled:
                    pass
                else:
                    walkButton  = btn.Button(image='images//walk_button.png', x=650,y=150)
                    shootButton = btn.Button(image='images//shoot_button.png',x=650,y=250)
                    
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
                movement = False
            
            #display buttons
            backButton.draw(display)
            
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
                        
                    if aicontrolled == False:
                        if walkButton.unclick(x , y):
                            pass
                        
                        if shootButton.unclick(x , y):
                            pass
                        
                        
                        if upButton.unclick(x , y):
                            pass
                        
                        if downButton.unclick(x , y):
                            pass
                        
                        if leftButton.unclick(x , y):
                            pass
                        
                        if rightButton.unclick(x , y):
                            pass
                
                #Left mouse button is held down
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseclicked = True
            
            
            #$$$$$$$$ Check if button is being hovered by mouse when clicked $$$$$$$$
            if mouseclicked:
                #Get mouse cordinates
                x , y = pygame.mouse.get_pos()
                
                #Check if button is hovered and darken it if it is
                backButton.clicked(x , y)
                
                if aicontrolled == False:
                    walkButton.clicked(x , y)
                    shootButton.clicked(x , y)
                    
                    upButton.clicked(x , y)
                    downButton.clicked(x , y)
                    leftButton.clicked(x , y)
                    rightButton.clicked(x , y)
                
            #$$$$$$$$ If changing rooms then clean up memory, else draw $$$$$$$$
            if changingRoom:
                del backButton
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
