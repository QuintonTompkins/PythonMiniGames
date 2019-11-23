#Author: Quinton Tompkins


class WumpusPlayerAI():
    def __init__(self):
        #explored tiles will be represented by [[x,y],stench,breeze, deadwumpus]
        self.exploredtiles = []
        #fringe tiles will be represented by [x,y]
        self.fringetiles = []
        #The current path the ai will take
        self.path = []
        self.dx = None
        self.dy = None
        self.wumpuschance = 0
        self.pitchance = 0
        self.dirList = {
            1 : 'left',
            -1: 'right',
            2 : 'up',
            -2: 'down' }
        self.action = 'Walking'
        self.ammo = 0
        
    
    #Reset important variables at the start of a new level
    def newLevelInfo(self, px , py , wumpuscount , pitcount , ammo):
        self.dx = px
        self.dy = py
        self.fringetiles = [[px,py]]
        self.exploredtiles = []
        self.ammo = ammo
        self.wumpuschance = wumpuscount / 100
        self.pitchance = pitcount / 100
    
    
    #Will take current tiles information and return the action and direction to act.
    def requestAction(self, px , py , stench , breeze , deadwumpus):
        if self.dx == px and self.dy == py:
            self.fringetiles.remove([px,py])
            self.addToFringe(px,py)
            self.exploredtiles.append([[px,py],stench,breeze,deadwumpus])
            nexttile = self.calcBestTile()
            self.calcPath(px , py , nexttile)
            
        return self.nextAction([px,py] , stench)
    
    
    #Will calculate a safe path to the destination tile with breadth first search
    def calcPath(self, px , py , nexttile):
        #tilelist has [parent coordinates ,coordinates , has been expanded]
        tilelist = [[None,[px,py],False]]
        
        #found will be set to true when the nexttile is found
        found = False
        while not found:
            newtiles = []
            
            for tile in tilelist:
                if not tile[2]:
                    tile[2] = True
                    checktiles = [[tile[1][0]-1,tile[1][1]],
                                  [tile[1][0]+1,tile[1][1]],
                                  [tile[1][0]  ,tile[1][1]-1],
                                  [tile[1][0]  ,tile[1][1]+1]]
                    
                    for tile2 in checktiles:
                        if tile2[0] > -1 and tile2[0] < 10 and tile2[1] > -1 and tile2[1] < 10:
                            
                            alreadyadded = False
                            for tile4 in tilelist:
                                if tile4[1] == tile2:
                                    alreadyadded = True
                                    break
                                
                            if not alreadyadded:
                                for tile3 in self.exploredtiles:
                                    if tile2 == tile3[0]:
                                        newtiles.append([tile[1],tile3[0],False])
                                        
                                if tile2 == nexttile:
                                    newtiles.append([tile[1],tile2,False])
                                    found = True
                    
            for t in newtiles:
                tilelist.append(t)
        
        #self.path will be stacked with actions which will be popped later
        self.path = [nexttile]
        currenttile = nexttile
        
        #stack movements
        count = 0
        while currenttile != None:   
            count += 1
            for tile in tilelist:
                if tile[1] == currenttile:
                    currenttile = tile[0]
                    if currenttile != None:
                        self.path.append(currenttile)
                    break
                        
        #go ahead and pop the first one, because we are already there.
        self.path.pop()
        
    
    #Calculate the next best tile to explore
    def calcBestTile(self):
        
        tilelist = []
        count = 0
        
        #We are going to look at all the fringe tiles and figure out which one gives us the best chance of survival.
        #The ai will prefer risking a wumpus tile over a pit tile. If the wumpus risk is too high then shoot it first.
        for tile in self.fringetiles:
            tilelist.append([[tile[0],tile[1]],[0,1],[0,1]])
            
            checktiles = [[tile[0]-1,tile[1]],
                          [tile[0]+1,tile[1]],
                          [tile[0]  ,tile[1]-1],
                          [tile[0]  ,tile[1]+1]]
            #check tiles surrounding target fringe tile and check for breezes and stenches to calculate risk
            for tile2 in checktiles:
                if tile2[0] > -1 and tile2[0] < 10 and tile2[1] > -1 and tile2[1] < 10:
                    for tile3 in self.exploredtiles:
                        if tile3[0] == tile2:
                            
                            checktiles2 = [[tile2[0]-1,tile2[1]],
                                          [tile2[0]+1,tile2[1]],
                                          [tile2[0]  ,tile2[1]-1],
                                          [tile2[0]  ,tile2[1]+1]]
                            
                            #chance is a relative risk of a tile.
                            chance = 1
                            #Check how many tiles surrounding each of these tiles could be causing a stench/breeze 
                            #and use that info to calculate the chances this specific fringe tile is the cause.
                            for tile4 in checktiles2:
                                for tile5 in self.exploredtiles:
                                    if tile5[0] == tile4:
                                        chance += 1
                                        break
                                if tile4[0] < 0 or tile4[0] > 9 or tile4[1] < 0 or tile4[1] > 9:
                                    chance += 1
                                    
                            
                            if tile3[1]:
                                tilelist[count][1][0] += chance
                            else:
                                #if any tiles next to it don't have a stench then it can't have a wumpus
                                tilelist[count][1][1] = 0
                            if tile3[2]:
                                #pit has it's risk doubled because we can at least shoot a wumpus
                                tilelist[count][2][0] += chance * 2
                            else:
                                #if any tiles next to it don't have a breeze then it can't have a pit
                                tilelist[count][2][1] = 0
                            break

            count += 1
        
        #Check for which fringe tile has the lowest risk
        besttile = [[0,0],[1000000,1000000]]
        for tile in tilelist:
            danger = [tile[1][0] * tile[1][1] , tile[2][0] * tile[2][1]]
            if besttile[1][0] + besttile[1][1] > danger[0] + danger[1]:
                besttile = [ tile[0] , danger]
                
        #If the wumpus risk is too high then shoot the tile first
        if besttile[1][0] > 2 and self.ammo > 0:
            self.action = 'Shooting'
        else:
            self.action = 'Walking'
            
        self.dx = besttile[0][0]
        self.dy = besttile[0][1]
        return besttile[0]
        
    
    
    
    
    #Will return to the main program the stance and direction the ai would like to go next
    def nextAction(self , currenttile , stench):
        action = 'Walking'
        ls = len(self.path) - 1
        if ls == 0 and self.action == 'Shooting':
            #The stench is gone because it was caused by a wumpus that was already shot
            if not stench:
                self.action = 'Walking'
                nexttile = self.path[ls]
                self.path.pop()
                for tile in self.exploredtiles:
                    if tile[0][0] == nexttile:
                        tile[0][1] = False
                        break
            #Wumpus is still there so shoot it, and then walk into the tile next
            else:
                nexttile = self.path[ls]
                action = 'Shooting'
                self.action = 'Walking'
        else:
            #Walk to the next tile
            nexttile = self.path[ls]
            self.path.pop()
        
        direction = (currenttile[0] - nexttile[0]) * 2 + (currenttile[1] - nexttile[1]) 
        
        return self.dirList.get(direction) , action
    
    
    #add new tiles to fringe
    def addToFringe(self, px , py ):
        checktiles = [[px-1,py],
                      [px+1,py],
                      [px,py-1],
                      [px,py+1]]
        
        for tile in checktiles:
            if tile[0] > -1 and tile[0] < 10 and tile[1] > -1 and tile[1] < 10:
                cf , ce = self.checkFringeAndExplored(tile)
                if not cf and not ce:
                    self.fringetiles.insert(0,tile)
           
    
    #Check if tile is already in the fringe or explored tiles list
    def checkFringeAndExplored(self, tile):
        check1 = False
        check2 = False
        
        for t in self.fringetiles:
            if t == tile:
                check1 = True
                break
        for t in self.exploredtiles:
            if t[0] == tile:
                check2 = True
                break
            
        return check1 , check2
            
            
            
            