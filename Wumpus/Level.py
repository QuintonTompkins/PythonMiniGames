#Author: Quinton Tompkins

import json

class Level():
    def __init__(self):
        self.level = 1
        filename = 'levels//level-' + str(self.level) + '.json'
        try:
            with open(filename) as json_file:
                data = json.load(json_file)
                
            # 0 is an empty tile
            # 1 is the player's tile
            # 2 is a wumpus tile
            # 3 is a pit tile
            # 4 is a ladder tile
            # 5 is a dead wumpus tile
            #The second 0 or 1 indicates whether the tile has been explored.
            self.tiles = data['level']['tiles'] 
            
            self.ammo  = data['level']['ammo']
        except:
            pass
        
    def checkForNextLevel(self):
        try:
            open('levels//level-' + str(self.level + 1) + '.json')
            return True
        except:
            return False
    
    def nextLevel(self):
        self.level += 1
        filename = 'levels//level-' + str(self.level) + '.json'
        try:
            with open(filename) as json_file:
                data = json.load(json_file)
                
            # 0 is an empty tile
            # 1 is the player's tile
            # 2 is a wumpus tile
            # 3 is a pit tile
            # 4 is a ladder tile
            # 5 is a dead wumpus tile
            #The second 0 or 1 indicates whether the tile has been explored.
            self.tiles = data['level']['tiles']
            
            self.ammo  = data['level']['ammo']
        except:
            pass
        
    def checkStench(self, x, y):
        if x > 0 and self.tiles[y][x - 1][0] == 2:
            return True
        if x < 9 and self.tiles[y][x + 1][0] == 2:
            return True
        if y > 0 and self.tiles[y - 1][x][0] == 2:
            return True
        if y < 9 and self.tiles[y + 1][x][0] == 2:
            return True
        
        return False
    
    def checkBreeze(self, x, y):
        if x > 0 and self.tiles[y][x - 1][0] == 3:
            return True
        if x < 9 and self.tiles[y][x + 1][0] == 3:
            return True
        if y > 0 and self.tiles[y - 1][x][0] == 3:
            return True
        if y < 9 and self.tiles[y + 1][x][0] == 3:
            return True
        
        return False
            
    def aiInfo(self):
        px = 0
        py = 0
        wumpuscount = 0
        pitcount = 0
        
        for y in range(10):
            for x in range(10):
                if self.tiles[y][x][0] == 1:
                    px = x
                    py = y
                elif self.tiles[y][x][0] == 2:
                    wumpuscount += 1
                elif self.tiles[y][x][0] == 3:
                    pitcount += 1
        
        
        
        return px , py , wumpuscount , pitcount , self.ammo
            
    
    
    
    
    
    
        