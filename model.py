from random import random, choice, randint
import pygame
from pygame.locals import (
    K_RIGHT,
    KEYDOWN,
    QUIT,
)
import matplotlib.pyplot as plt
import numpy as np


class Model:
    def __init__(self, width, height):
        self.simulationDay = 0
        self.width = width
        self.height = height
        self.worldGrid = [
            [GridCell(x, y) for y in range(width)] for x in range(height)
        ]

        self.predators = set()
        self.preys = set()

        for _ in range(10):
            self.predators.add(Predator(randint(0, self.width-1), randint(0, self.height-1), self.worldGrid))
        
        for _ in range(20):
            self.preys.add(Prey(randint(0, self.width-1), randint(0, self.height-1), self.worldGrid))
    
    def getPredatorCount(self):
        return len(self.predators)

    def getPreyCount(self):
        return len(self.preys)


    def step(self):
        # todo: asynchronous
        self.simulationDay += 1
        
        for predator in list(self.predators):
            alive, reproduced = predator.step()
            if not alive:
                self.predators.remove(predator)
                self.worldGrid[predator.x][predator.y].predator = None

            if reproduced:
                self.predators.add(reproduced)
        
        for prey in list(self.preys):
            alive, reproduced = prey.step()
            if not alive:
                self.preys.remove(prey)
                self.worldGrid[prey.x][prey.y].prey = None

            if reproduced:
                self.preys.add(reproduced)

        # update grass
        for row in range(self.height):
            for col in range(self.width):
                self.worldGrid[row][col].updateGrass()


    def draw(self, screen, windowWidth, windowHeight):
        blockSize = (min(windowWidth, windowHeight)-max(self.height, self.width))/max(self.height, self.width)

        for row in range(self.height):
            for col in range(self.width):
                self.worldGrid[row][col].updateGrass()

                posX = (blockSize+1) * row
                posY = (blockSize+1) * col
                rect = pygame.Rect(posX, posY, blockSize, blockSize)

                # todo: replace with animating pictures
                color='#fefae0'
                if self.worldGrid[row][col].predator:
                    color = '#e63946'
                elif self.worldGrid[row][col].prey:
                    color = '#4361ee'
                elif self.worldGrid[row][col].hasGrass:
                    color = '#606c38'

                pygame.draw.rect(screen, color, rect, 0)


        pygame.display.flip()


class GridCell:
    def __init__(self, x, y, grassGrowthProbability=0.0005, grassEnergy=1):
        self.x = x
        self.y = y
        self.predator = None
        self.prey = None
        self.grassGrowthProbablity = grassGrowthProbability
        self.hasGrass = False
        self.grassEnergy = grassEnergy
    
    def updateGrass(self):
        if not self.hasGrass and random() < self.grassGrowthProbablity:
            self.hasGrass = True
    
    def getNeighboringCells(self, worldGrid):
        worldHeight = len(worldGrid)
        worldWidth = len(worldGrid[0])

        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i != 0 or j != 0) and (0 <= i + self.x < worldHeight) and (0 <= j + self.y < worldWidth):
                    neighbors.append(worldGrid[i + self.x][j + self.y])
        
        return neighbors


class Animal:
    def __init__(self, x, y, worldGrid, startEnergy, minEnergyToSurvive, energyLossRate, maxDaysToReproduce):
        self.x = x
        self.y = y

        self.worldGrid = worldGrid
        self.worldHeight = len(worldGrid)
        self.worldWidth = len(worldGrid[0])

        self.minEnergyToSurvive = minEnergyToSurvive
        self.energyLossRate = energyLossRate
        self.energy = startEnergy
        self.daysToReproduce = maxDaysToReproduce
        self.maxDaysToReproduce = maxDaysToReproduce

    def checkAlive(self):
        return self.energy > 0

    def updateDailyParameters(self):
        if self.daysToReproduce > 0:
            self.daysToReproduce -= 1
        
        self.energy -= self.energyLossRate


class Predator(Animal):
    def __init__(self, x, y, worldGrid, startEnergy=50, minEnergyToSurvive=1, energyLossRate=1, maxDaysToReproduce=5):
        super().__init__(x, y, worldGrid, startEnergy, minEnergyToSurvive, energyLossRate, maxDaysToReproduce)

        self.worldGrid[x][y].predator = self

    def step(self):
        alive = self.checkAlive()
        if not alive:
            return False, None
        
        self.energy -= self.energyLossRate
        self.eatPrey()
        reproduced = self.reproduce()
        self.move()
        self.updateDailyParameters()

        return alive, reproduced

    def eatPrey(self):
        neighbors = self.worldGrid[self.x][self.y].getNeighboringCells(self.worldGrid)
        prey = list(filter(lambda cell: cell.prey, neighbors))

        if prey:
            weakestPrey = min(prey, key=lambda p: p.prey.energy).prey
            self.energy += weakestPrey.energy
            weakestPrey.energy = 0


    def move(self):
        neighbors = self.worldGrid[self.x][self.y].getNeighboringCells(self.worldGrid)
        emptyNeighbors = list(filter(lambda cell: not cell.predator and not cell.prey, neighbors))
        
        if emptyNeighbors:
            randomMove = choice(emptyNeighbors)
            self.worldGrid[self.x][self.y].predator = None
            self.x = randomMove.x
            self.y = randomMove.y
            self.worldGrid[self.x][self.y].predator = self

    def reproduce(self):
        if self.daysToReproduce > 0:
            return
        
        candidate = None
        bestCandidateEnergy = -1

        neighboringCells = self.worldGrid[self.x][self.y].getNeighboringCells(self.worldGrid)

        for cell in neighboringCells:
            if neighborPredator := cell.predator:
                if neighborPredator.energy > bestCandidateEnergy:
                    candidate = neighborPredator
                    bestCandidateEnergy = neighborPredator.energy

        if candidate:
            emptyCell = None
            for cell in neighboringCells:
                if not cell.predator and not cell.prey:
                    emptyCell = cell
                    break
            
            if emptyCell:
                newPredator = Predator(emptyCell.x, emptyCell.y, self.worldGrid)
                self.daysToReproduce = self.maxDaysToReproduce
                return newPredator


class Prey(Animal):

    def __init__(self, x, y, worldGrid, startEnergy=100, minEnergyToSurvive=1, energyLossRate=1, maxDaysToReproduce=4):
        super().__init__(x, y, worldGrid, startEnergy, minEnergyToSurvive, energyLossRate, maxDaysToReproduce)
        
        self.worldGrid[x][y].prey = self

    def step(self):
        alive = self.checkAlive()
        if not alive:
            return False, None
        
        self.eatGrass()
        reproduced = self.reproduce()
        self.move()
        self.updateDailyParameters()

        return alive, reproduced

    def eatGrass(self):
        cell = self.worldGrid[self.x][self.y]
        if cell.hasGrass:
            self.energy += cell.grassEnergy
            cell.hasGrass = False

    def move(self):
        # look for grass, if found move there
        # avoid predators

        neighbors = self.worldGrid[self.x][self.y].getNeighboringCells(self.worldGrid)
        emptyNeighbors = list(filter(lambda cell: not cell.predator and not cell.prey, neighbors))
        
        if emptyNeighbors:
            randomMove = choice(emptyNeighbors)
            self.worldGrid[self.x][self.y].prey = None
            self.x = randomMove.x
            self.y = randomMove.y
            self.worldGrid[self.x][self.y].prey = self

    def reproduce(self):
        if self.daysToReproduce > 0:
            return
        
        candidate = None
        bestCandidateEnergy = -1

        neighboringCells = self.worldGrid[self.x][self.y].getNeighboringCells(self.worldGrid)

        for cell in neighboringCells:
            if neighborPrey := cell.prey:
                if neighborPrey.energy > bestCandidateEnergy:
                    candidate = neighborPrey
                    bestCandidateEnergy = neighborPrey.energy

        if candidate:
            emptyCell = None
            for cell in neighboringCells:
                if not cell.predator and not cell.prey:
                    emptyCell = cell
                    break
            
            if emptyCell:
                newPrey = Prey(emptyCell.x, emptyCell.y, self.worldGrid)
                self.daysToReproduce = self.maxDaysToReproduce
                return newPrey


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Predator-Prey Agent Based Simulation')
    
    windowWidth = 800
    windowHeight = 800
    
    screen = pygame.display.set_mode([windowWidth, windowHeight])
    screen.fill((255, 255, 255))

    model = Model(100, 100)
    model.draw(screen, windowWidth, windowHeight)

    time_delay = 200 # 0.2 s
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, time_delay)
    
    plt.ion()
    
    predatorCounts = []
    preyCounts = []
    predatorGraph = plt.plot(predatorCounts, color='#e63946', linewidth=3, label='Predators')[0]
    preyGraph = plt.plot(preyCounts, color='#4361ee', linewidth=3, label='Prey')[0]
    
    xLim = 100
    yLim = 100   
    plt.xlim([0, xLim])
    plt.ylim([0, yLim])
    
    plt.xlabel('day')
    plt.ylabel('count')
    plt.title('Population counts')
    ax = plt.gca()
    ax.set_facecolor('#fefae0')
    plt.legend()
    
    running = True

    while running:
        
        for event in pygame.event.get():   
            if event.type == QUIT:
                running = False
            
            if event.type == timer_event or (event.type == KEYDOWN and event.key == K_RIGHT):
                    model.step()
                    
                    predatorCount = model.getPredatorCount()
                    predatorCounts.append(predatorCount)
                    
                    preyCount = model.getPreyCount()
                    preyCounts.append(preyCount)
                    
                    day = model.simulationDay
                    
                    if day > xLim:
                        xLim = 2*day
                        plt.xlim([0, xLim])
                    
                    if predatorCount > yLim:
                        yLim = 2*predatorCount
                        plt.ylim([0, yLim])
                    
                    if preyCount > yLim:
                        yLim = 2*preyCount
                        plt.ylim([0, yLim])
                    
                    model.draw(screen, windowWidth, windowHeight)
                    predatorGraph.set_data(list(range(day)), predatorCounts)
                    preyGraph.set_data(list(range(day)), preyCounts)
                    
    pygame.quit()