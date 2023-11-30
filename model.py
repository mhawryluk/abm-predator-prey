from random import random
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
            [GridCell(x, y) for x in range(width)] for y in range(height)
        ]

        self.predators = [Predator(4, 5, self.worldGrid), Predator(1, 1, self.worldGrid), Predator(1, 4, self.worldGrid)]
        self.preys = [Prey(1, 1, self.worldGrid), Prey(2, 2, self.worldGrid), Prey(3, 3, self.worldGrid)]

    def step(self):
        # todo: asynchronous
        for predator in self.predators:
            predator.step()
        
        for prey in self.preys:
            prey.move()

        # update grass
        for row in range(self.height):
            for col in range(self.width):
                self.worldGrid[row][col].updateGrass()

        # update visualization

        # update graphs

    def draw(self, screen, windowWidth, windowHeight):
        blockSize = (min(windowWidth, windowWidth)-max(self.height, self.width))/max(self.height, self.width)

        for row in range(self.height):
            for col in range(self.width):
                self.worldGrid[row][col].updateGrass()

                posX = (blockSize+1) * row
                posY = (blockSize+1) * col
                rect = pygame.Rect(posX, posY, blockSize, blockSize)

                # todo: replace with animating pictures
                color='#fefae0'
                if isinstance(self.worldGrid[row][col].animal, Predator):
                    color = '#e63946'
                elif isinstance(self.worldGrid[row][col].animal, Prey):
                    color = '#4361ee'
                elif self.worldGrid[row][col].hasGrass:
                    color = '#606c38'

                pygame.draw.rect(screen, color, rect, 0)


        pygame.display.flip()


class GridCell:
    def __init__(self, x, y, grassGrowthProbability=0.3):
        self.x = x
        self.y = y
        self.animal = None
        self.grassGrowthProbablity = grassGrowthProbability
        self.hasGrass = False
    
    def updateGrass(self):
        if not self.hasGrass and random() < self.grassGrowthProbablity:
            self.hasGrass = True

class Animal:
    def __init__(self, x, y, worldGrid, startEnergy=5, minEnergyToSurvive=1, energyLossRate=1):
        self.x = x
        self.y = y

        self.worldGrid = worldGrid
        self.worldHeight = len(worldGrid)
        self.worldWidth = len(worldGrid[0])

        self.minEnergyToSurvive = minEnergyToSurvive
        self.energyLossRate = energyLossRate
        self.energy = startEnergy

        self.worldGrid[x][y].animal = self
    
    def reproduce(self):
        pass

    def checkAlive(self):
        pass

    def draw(screen):
        pass


class Predator(Animal):
    def step(self):
        self.energy -= self.energyLossRate
        self.eatPrey()
        self.move()

    def eatPrey(self):
        pass

    def move(self):
        pass


class Prey(Animal):
    def step(self):
        self.energy -= self.energyLossRate
        self.eatGrass()
        self.avoidPredator()
        self.move()

    def eatGrass(self):
        pass

    def move(self):
        # look for grass, if found move there
        pass


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

    time_delay = 200 # 0.2 s
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, time_delay)

    while running:
        for event in pygame.event.get():   
            if event.type == QUIT:
                running = False
            
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    model.step()
                    model.draw(screen, windowWidth, windowHeight)

            # if event.type == timer_event:
            #     board.iteration()
            #     board.drawGrid(screen, w_width, w_height)

    pygame.quit()