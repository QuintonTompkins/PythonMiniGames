#Author: Quinton Tompkins

import pygame

class Button():
    def __init__(self, image, x, y):
        #Create the default button image
        self.image = pygame.image.load(image)
        
        #Get the cordinates to calculate if the mouse is over the button
        self.x = x
        self.y = y
        width , height = self.image.get_rect().size
        self.x2 = x + width
        self.y2 = y + height
        
        #this boolean indicates if the button has the mouse over it
        self.hovered = False
        
        #This creates the tinted button for when the player is clicking on it
        m = pygame.mask.from_surface(self.image, 0)
        shader = pygame.Surface((self.image.get_size()), masks=m).convert_alpha()
        shader.fill((215,215,215))
        self.darkimage = self.image.copy()
        self.darkimage.blit(shader, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
        
        
        
    def draw(self, display):
        if self.hovered:
            display.blit(self.darkimage , (self.x , self.y))
        else:
            display.blit(self.image , (self.x , self.y))
        
        
    def unclick(self,x,y):
        self.hovered = False
        if x > self.x and x < self.x2 and y > self.y and y < self.y2:
            return True
        else:
            return False
        
        
    def clicked(self,x,y):
        if x > self.x and x < self.x2 and y > self.y and y < self.y2:
            self.hovered = True
            return True
        else:
            self.hovered = False
            return False