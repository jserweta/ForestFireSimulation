import random
import math
import time
#import numpy as np
import pygame
import csv
from pygame.locals import *

from terrain import TerrainChunk
from firefighter import Firefighter


class MainLoop():

    isFire = False
    forest = [[0] * 20 for i in range(20)]
    #outerBiomes: list = np.arange(400).reshape((20, 20))
    firefighters: list = []
    fieldSizeX = 20
    fieldSizeY = 20
    endangeredLocations: list = []
    wind_direction: int

    WINDOW_HEIGHT = 821
    WINDOW_WIDTH = 821
    MARGIN = 1

    BLACK = (0, 0, 0)
    GREY = (128, 128, 128)
    WHITE = (255, 255, 255)
    GREEN_2 = (0, 255, 0)
    GREEN_1 = (102, 255, 102)
    GREEN_3 = (0, 153, 0)
    RED = (255, 0, 0)

    SCREEN = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
    CLOCK = pygame.time.Clock()

    file = None
    writer = None

    def __init__(self):
        self.file = open('result.csv', 'w', newline='')
        self.writer = csv.writer(self.file)
        headers = ['tick']
        self.wind_direction = random.randint(0,7)
        for i in range(self.fieldSizeX):
            for j in range(self.fieldSizeY):
                self.forest[i][j] = TerrainChunk(i,j)
                headers.append('R' + str(i) + 'C' + str(j))
        for i in range(500):
            self.firefighters.append(Firefighter(i))
        self.writer.writerow(headers)

    def fire_spread_to_one(self, i, j):
        if 0 <= i <= 19 and 0 <= j <= 19:
            chunk = self.forest[i][j]
            self.fire_spread_to_one_min_max(chunk, chunk.fire_risk+1, chunk.fire_risk+2)

    def fire_spread_to_one_min_max(self,chunk, min, max):
            if chunk.fireState == 0:
                chunk.fireState = random.randint(min, max)


    def sprad_fire(self, i, j):
        if i > 0:
            chunk = self.forest[i-1][j]
            self.fire_spread_to_one_min_max(chunk, chunk.fire_risk, chunk.fire_risk +1)
        if i < 19:
            chunk = self.forest[i+1][j]
            self.fire_spread_to_one_min_max(chunk, chunk.fire_risk, chunk.fire_risk +1)
        if j > 0:
            chunk = self.forest[i][j-1]
            self.fire_spread_to_one_min_max(chunk, chunk.fire_risk, chunk.fire_risk+1)
        if j < 19:
            chunk = self.forest[i][j+1]
            self.fire_spread_to_one_min_max(chunk, chunk.fire_risk, chunk.fire_risk+1)

    def fire_spread(self, i, j):
        if self.wind_direction == 0:
            self.fire_spread_to_one(i - 1, j - 1)
            self.fire_spread_to_one(i, j - 1)
            self.fire_spread_to_one(i + 1, j - 1)
        if self.wind_direction == 1:
            self.fire_spread_to_one(i, j - 1)
            self.fire_spread_to_one(i + 1, j - 1)
            self.fire_spread_to_one(i + 1, j)
        if self.wind_direction == 2:
            self.fire_spread_to_one(i + 1, j - 1)
            self.fire_spread_to_one(i + 1, j)
            self.fire_spread_to_one(i + 1, j - 1)
        if self.wind_direction == 3:
            self.fire_spread_to_one(i + 1, j)
            self.fire_spread_to_one(i + 1, j - 1)
            self.fire_spread_to_one(i, j - 1)
        if self.wind_direction == 4:
            self.fire_spread_to_one(i + 1, j - 1)
            self.fire_spread_to_one(i, j - 1)
            self.fire_spread_to_one(i - 1, j - 1)
        if self.wind_direction == 5:
            self.fire_spread_to_one(i, j - 1)
            self.fire_spread_to_one(i - 1, j - 1)
            self.fire_spread_to_one(i - 1, j)
        if self.wind_direction == 6:
            self.fire_spread_to_one(i - 1, j - 1)
            self.fire_spread_to_one(i - 1, j)
            self.fire_spread_to_one(i - 1, j + 1)
        if self.wind_direction == 7:
            self.fire_spread_to_one(i - 1, j)
            self.fire_spread_to_one(i - 1, j + 1)
            self.fire_spread_to_one(i, j - 1)



    def ask_for_firefighter(self, i, j, prevState, state):
        isExpanding = True if prevState < state else False
        if not isExpanding:
            count = random.randint(0, 1)
        else:
            count = random.randint(2, state+2) #2, state*2-3
            self.endangeredLocations.append((i, j))
        firefightersFree = [f for f in self.firefighters if f.state == 'free']
        if count > len(firefightersFree):
            count = len(firefightersFree)
        selectedFirefigters = random.sample(firefightersFree, count)
        for f in selectedFirefigters:
            f.assign(i, j)

    def update_firefifighters(self, i, j, fireState):
        firefightersPresent = [f for f in self.firefighters if f.locX == i and f.locY == j and f.state != 'dead']

        for freeF in firefightersPresent:
            fGoal = freeF.getGoal()
            orderField = self.forest[fGoal[0]][fGoal[1]]
            freeF.update(orderField.fireState)

        firefightersPresent = [f for f in self.firefighters if f.locX == i and f.locY == j  and f.state != 'dead']
        if ((fireState - 1)*2 + 1) < len(firefightersPresent):
            freeFirefighterNum = len(firefightersPresent) - ((fireState - 1)*2 + 1)
            for freeF in firefightersPresent[:freeFirefighterNum]:
                freeF.state = 'free'
                if self.endangeredLocations: 
                    newLocation = self.endangeredLocations.pop(0)
                    freeF.orderX = newLocation[0]
                    freeF.orderY = newLocation[1]
                    
        

    

    def new_fire_state(self, i, j, prevState):
        firefightersPresent = [f for f in self.firefighters if f.locX == i and f.locY == j and f.state != 'dead']
        count = len(firefightersPresent)
        if ((prevState - 1)*2 + 1) <= count:
            return prevState - 1
        if (prevState - 1)*2 == count and prevState != 1:
            return prevState
        return prevState + 1 


    def getColor(self, row, column):
        intensity = self.forest[row][column].fireState
        if intensity == 1: return (255, 176, 176)
        if intensity == 2: return (255, 102, 102)
        if intensity == 3: return (255, 52, 52)
        if intensity == 4: return (255, 0, 0)
        if intensity == 5: return (179, 0, 0)
        if intensity == 6: return (128, 0, 0)
        if intensity == 7: return self.GREY
    
    def send_firefigters_away(self, i, j):
        firefightersPresent = [f for f in self.firefighters if f.locX == i and f.locY == j and f.state != 'dead']
        for f in firefightersPresent:
            f.free()

    def mainLoop(self):
        main_loop = True
        counter = 0

        self.SCREEN.fill(self.BLACK)

        while main_loop:
            if not self.isFire:
                self.isFire = True
                random_i = random.randint(0, 19)
                random_j = random.randint(0, 19)
                self.forest[random_i][random_j].fireState = self.forest[random_i][random_j].fire_risk + 2
                pygame.init()
                font = pygame.font.SysFont('Arial', 12)
                fontBusy = pygame.font.SysFont('Arial', 20)
            else:
                print(counter)
                counter += 1
                a = pygame.event.get()

                pygame.display.flip()

                for chunk in [c for line in self.forest for c in line if c.fireState > 0]:
                    #fireGod = random.randint(0,40)
                    #ffPresence = 0  #Write function about firefighters
                    #rngResult = ((chunk.fuel/100000.0) + ((math.sqrt(chunk.fireState - ffPresence))/10.0)) * 30
                    prevState = chunk.fireState
                    if prevState == 7:
                        self.send_firefigters_away(chunk.locX, chunk.locY)
                        continue
                    newState = self.new_fire_state(chunk.locX, chunk.locY, prevState)
                    chunk.fireState = newState
                    if newState == 7 or newState == 0:
                        self.send_firefigters_away(chunk.locX, chunk.locY)
                        continue
                    self.update_firefifighters(chunk.locX, chunk.locY, chunk.fireState)

                    if (newState >= prevState):
                        self.ask_for_firefighter(chunk.locX, chunk.locY, prevState, chunk.fireState)

                    
                    # if rngResult < 3:
                    #     chunk.fireState -= 1
                    # if rngResult > 30 and chunk.fireState < 100:
                    #     chunk.fireState += 1

                    if chunk.fireState >= 4:
                        self.fire_spread(chunk.locX, chunk.locY)

                    #chunk.fuel -= chunk.fireState

                    # print(chunk.fireState)
                    # print(rngResult)

                    #if chunk.fuel <= 0 or chunk.fireState <= 0:

                WIDTH = 40
                HEIGHT = 40

                tickResult = [counter]
                for row in range(20):
                    for column in range(20):
                        if self.forest[row][column].fire_risk == 0:
                            color = self.GREEN_1
                        if self.forest[row][column].fire_risk == 1:
                            color = self.GREEN_2
                        if self.forest[row][column].fire_risk == 2:
                            color = self.GREEN_3

                        data = self.forest[row][column].fireState
                        if data != 0:
                            color = self.getColor(row, column)
                        tickResult.append(data)
                        ffPresence = len([f for f in self.firefighters if f.locX == row and f.locY == column and f.state == 'busy'])
                        ffPresenceDead = len([f for f in self.firefighters if f.locX == row and f.locY == column and f.state == 'dead'])
                        ffPresenceMoving = len([f for f in self.firefighters if f.locX == row and f.locY == column and f.state == 'moving'])
                        text = fontBusy.render(str(ffPresence), True, self.BLACK)
                        if ffPresenceDead > 0:
                            textD = font.render("D" + str(ffPresenceDead), True, self.BLACK)
                        else:
                            textD = font.render(" ", True, self.BLACK)

                        if ffPresenceMoving > 0:
                            textM = font.render("M" + str(ffPresenceMoving), True, self.BLACK)
                        else:
                            textM = font.render(" ", True, self.BLACK)


                        #else:
                        #    text = font.render('', True, self.BLACK)
                        chunk = pygame.Rect((self.MARGIN + WIDTH) * column + self.MARGIN,
                            (self.MARGIN + HEIGHT) * row + self.MARGIN,
                                WIDTH,
                                HEIGHT)
                        textRect = text.get_rect()
                        textRect.center = chunk.center

                        textRectD = textD.get_rect()
                        textRectD.bottomleft = chunk.bottomleft

                        textRectM = textM.get_rect()
                        textRectM.bottomright = chunk.bottomright

                        pygame.draw.rect(self.SCREEN, color,chunk)
                        self.SCREEN.blit(text, textRect)
                        self.SCREEN.blit(textM, textRectM)
                        self.SCREEN.blit(textD, textRectD)

                self.writer.writerow(tickResult)

                for event in a:
                    if event.type == pygame.QUIT:
                        main_loop = False
                        self.file.close()
                        pygame.quit()

                fireStates = [item.fireState for sublist in self.forest for item in sublist]

                if all(elem == 0 or elem == 7 for elem in fireStates):
                    print("end")
                    main_loop = False
                    self.file.close()
                else:
                    time.sleep(1)

loop = MainLoop()
loop.mainLoop()
