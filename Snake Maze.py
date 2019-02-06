import pygame
import random
pygame.init()

screenh = 600
screenw = 600

screen = pygame.display.set_mode((screenh,screenw))

clock = pygame.time.Clock()
fps = 60

squareSize = 40
current = (0,0)
unvisited = []
visited = [current]
global listWalls
listWalls = []
mazeDone = False
grid = [["lrud" for y in range(screenw // squareSize)] for x in range(screenw // squareSize)]

for y in range(screenw // squareSize):
    for x in range(screenw // squareSize):
        unvisited.append((x,y))
unvisited.remove(current)
        
class walls:
    def __init__(self,startPos,endPos):
        self.startPos = startPos
        self.endPos = endPos
        
    def draw(self):
        pygame.draw.line(screen,
                         (0,0,0),
                         self.startPos,
                         self.endPos,
                         2)

class player:
    def __init__(self,x,y, squareSize):
        self.squareSize = squareSize
        self.x = x
        self.y = y
        self.left = False
        self.down = False
        self.up = False
        self.right = False
        self.rect = pygame.Rect(self.x, self.y, squareSize-10, squareSize-10)
    def draw(self):
        pygame.draw.rect(screen,(20,155,10), (self.x,self.y, self.squareSize-10,self.squareSize-10))
        
    def move(self):
        key= pygame.key.get_pressed()
        
        if key[pygame.K_LEFT]:
                self.x -= 5
                self.down = False
                self.up = False
                self.right = False
        if key[pygame.K_RIGHT]:
                self.x += 5
                self.right = True
                self.down = False
                self.up = False
                self.left = False
        if key[pygame.K_UP]:
                self.y -= 5
                self.up = True
                self.left = False
                self.right = False
                self.down = False
        if key[pygame.K_DOWN]:
                self.y += 5
                self.down = True
                self.left = False
                self.right = False
                self.up = False
                
##        if self.left == True:
##            self.x -= self.squareSize
##        if self.right == True:
##            self.x += self.squareSize
##        if self.up == True:
##            self.y -= self.squareSize
##        if self.down == True:
##            self.y += self.squareSize
            


def drawMaze(screen,grid, squareSize, screenw, current):
    global done

#A green square that will be used to draw the maze
    if mazeDone == False:
        pygame.draw.rect(screen,
                     (0,255,0),
                     (current[1]*squareSize, current[0]*squareSize, squareSize,squareSize))

#Drawing the maze   
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if 'l' in cell:
                startPos = (x * squareSize, y * squareSize)
                endPos = (x * squareSize, (y * squareSize) + squareSize)
                wall = walls(startPos, endPos)
                wall.draw()
##                pygame.draw.rect(screen, (255,0,0), (startPos[0], startPos[1], 4,squareSize),1)
                please = pygame.Rect(startPos[0], startPos[1], 4,squareSize)
                listWalls.append(please)
                
            if 'r' in cell:
                startPos = ((x * squareSize) + squareSize, y * squareSize)
                endPos = ((x * squareSize) + squareSize, (y * squareSize) + squareSize)
                wall = walls(startPos, endPos)
                wall.draw()
##                pygame.draw.rect(screen, (255,0,0), (startPos[0], startPos[1], 4,squareSize),1)
                please = pygame.Rect(startPos[0], startPos[1], 4,squareSize)
                listWalls.append(please)
                
            if 'u' in cell:
                startPos = (x * squareSize, y * squareSize)
                endPos = ((x * squareSize) + squareSize, y * squareSize)
                wall = walls(startPos, endPos)
                wall.draw()
##                pygame.draw.rect(screen, (255,0,0), (startPos[0], startPos[1], squareSize,4),1)
                please = pygame.Rect(startPos[0], startPos[1], squareSize,4)
                listWalls.append(please)
                
            if 'd' in cell:
                startPos = (x * squareSize, (y * squareSize) + squareSize)
                endPos = ((x * squareSize) + squareSize, (y * squareSize) + squareSize)
                wall = walls(startPos, endPos)
                wall.draw()
##                pygame.draw.rect(screen, (255,0,0), (startPos[0], startPos[1], squareSize,4),1)
                please = pygame.Rect(startPos[0], startPos[1], squareSize,4)
                listWalls.append(please)

    
def nextMove(grid, unvisited, visited, current, mazeDone):
    possibleChoices = []
    #Check if the cell on its right is unvisited
    if current[0]+1 < len(grid) and (current[0]+1, current[1]) in unvisited:
        possibleChoices.append((current[0] + 1, current[1]))
        
    #Check if the cell on its left is unvisited   
    if current[0]-1 >= 0 and (current[0]-1, current[1]) in unvisited:
        possibleChoices.append((current[0] - 1, current[1]))
        
    #Check if the cell below it is unvisited    
    if current[1]+1 < len(grid) and (current[0], current[1]+1) in unvisited:
        possibleChoices.append((current[0], current[1] + 1))
        
    #Check if the cell on top of it is unvisited    
    if current[1]-1 < len(grid) and (current[0], current[1]-1) in unvisited:
        possibleChoices.append((current[0], current[1] - 1 ))

    #if there are possible moves
    if len(possibleChoices) > 0:
        nextPos = random.choice(possibleChoices)
        #if the next position is in the same row
        if nextPos[0] == current[0]:
            #if the next position is the cell to the right
            if nextPos[1] > current[1]:
                grid[current[0]][current[1]] = grid[current[0]][current[1]].replace('r', '')
                grid[nextPos[0]][nextPos[1]] = grid[nextPos[0]][nextPos[1]].replace('l', '')
            #if the next position is the cell to the left
            else:
                grid[current[0]][current[1]] = grid[current[0]][current[1]].replace('l', '')
                grid[nextPos[0]][nextPos[1]] = grid[nextPos[0]][nextPos[1]].replace('r', '')
                
        #if the next position is in the same col
        if nextPos[1] == current[1]:
            #if the next position is the cell on top
            if nextPos[0] > current[0]:
                grid[current[0]][current[1]] = grid[current[0]][current[1]].replace('d', '')
                grid[nextPos[0]][nextPos[1]] = grid[nextPos[0]][nextPos[1]].replace('u', '')
            #if the next position is the cell below
            else:
                grid[current[0]][current[1]] = grid[current[0]][current[1]].replace('u', '')
                grid[nextPos[0]][nextPos[1]] = grid[nextPos[0]][nextPos[1]].replace('d', '')

                
        current = nextPos
        if current not in visited:
            visited.append(current)
        if current in unvisited:
            unvisited.remove(current)
    else:
        # If we are not in the initial situaltion of only (0, 0) in visited
        if len(visited) > 1:
            visited.pop()      # We remove the last element to go one step back since we are in a dead end
            current = visited[-1]       # We update current to be the new last element


        else:
            mazeDone = True


    return grid, current, visited, unvisited, mazeDone


char = player(5,5,squareSize)
run = True

while run:

    clock.tick(fps)
           
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    screen.fill((255,255,255))
    drawMaze(screen,grid, squareSize, screenw, current)
    
    grid, current, visited, unvisited, mazeDone = nextMove(grid, unvisited, visited, current, mazeDone)
    if mazeDone == True:
        char.draw()
        char.move()
##        for wall in listWalls:
##            print(wall)
##            if wall.colliderect(char.rect):
##                pygame.display.update()
##                print("boom")
    pygame.display.update()
    

pygame.quit()



    


