from random import random, choice
import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


class Model:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.worldGrid = [
            [GridCell(x, y) for y in range(width)] for x in range(height)
        ]

        self.predators = [Predator(4, 5, self.worldGrid), Predator(1, 1, self.worldGrid), Predator(1, 4, self.worldGrid)]
        self.preys = [Prey(1, 2, self.worldGrid), Prey(2, 2, self.worldGrid), Prey(3, 3, self.worldGrid)]

    def step(self):
        # todo: asynchronous
        for predator in self.predators:
            reproduced = predator.step()
            if reproduced:
                self.predators.append(reproduced)
        
        for prey in self.preys:
            reproduced = prey.step()
            if reproduced:
                self.preys.append(reproduced)

        # update grass
        for row in range(self.height):
            for col in range(self.width):
                self.worldGrid[row][col].updateGrass()

        # update visualization

        # update graphs


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
    def __init__(self, x, y, grassGrowthProbability=0.3):
        self.x = x
        self.y = y
        self.predator = None
        self.prey = None
        self.grassGrowthProbablity = grassGrowthProbability
        self.hasGrass = False
    
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
    def __init__(self, x, y, worldGrid, startEnergy, minEnergyToSurvive, energyLossRate, daysToReproduce):
        self.x = x
        self.y = y

        self.worldGrid = worldGrid
        self.worldHeight = len(worldGrid)
        self.worldWidth = len(worldGrid[0])

        self.minEnergyToSurvive = minEnergyToSurvive
        self.energyLossRate = energyLossRate
        self.energy = startEnergy
        self.daysToReproduce = daysToReproduce

    def checkAlive(self):
        pass

    def draw(screen):
        pass

    def updateDailyParameters(self):
        if self.daysToReproduce > 0:
            self.daysToReproduce -= 1
        
        self.energy -= self.energyLossRate


class Predator(Animal):
    def __init__(self, x, y, worldGrid, startEnergy=5, minEnergyToSurvive=1, energyLossRate=1, daysToReproduce=5):
        super().__init__(x, y, worldGrid, startEnergy, minEnergyToSurvive, energyLossRate, daysToReproduce)

        self.worldGrid[x][y].predator = self

    def step(self):
        self.energy -= self.energyLossRate
        self.eatPrey()
        reproduced = self.reproduce()
        self.move()
        self.updateDailyParameters()

        return reproduced

    def eatPrey(self):
        pass

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
                return newPredator


class Prey(Animal):
    def __init__(self, x, y, worldGrid, startEnergy=500, minEnergyToSurvive=1, energyLossRate=1, daysToReproduce=5):
        super().__init__(x, y, worldGrid, startEnergy, minEnergyToSurvive, energyLossRate, daysToReproduce)
        
        self.worldGrid[x][y].prey = self

    def step(self):
        self.eatGrass()
        reproduced = self.reproduce()
        self.move()
        self.updateDailyParameters()

        return reproduced

    def eatGrass(self):
        pass

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
            print(self.x, self.y, candidate.x, candidate.y)

            emptyCell = None
            for cell in neighboringCells:
                if not cell.predator and not cell.prey:
                    emptyCell = cell
                    break
            
            if emptyCell:
                print(emptyCell.x, emptyCell.y)
                newPrey = Prey(emptyCell.x, emptyCell.y, self.worldGrid)
                return newPrey


if __name__ == '__main__':
    pygame.init()
    windowWidth = 800
    windowHeight = 800
    screen = pygame.display.set_mode([windowWidth, windowHeight])

    # Create Board object
    model = Model(15, 15)
    # Set background
    screen.fill((255, 255, 255))

    # Draw grid
    model.draw(screen, windowWidth, windowHeight)
        
    running = True

    while running:
        for event in pygame.event.get():   
            if event.type == QUIT:
                running = False
            
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    model.step()
                    model.draw(screen, windowWidth, windowHeight)

    pygame.quit()