import pygame
import json
from random import randint
from gridCell import GridCell
from predator import Predator
from prey import Prey


class Model:
    def __init__(self, mapUrl):
        with open(mapUrl, 'r') as file:
            mapJson = json.load(file)

        self.simulationDay = 0
        self.width = len(mapJson[0])
        self.height = len(mapJson)

        self.worldGrid = [
            [GridCell(x, y, mapJson[x][y]) for y in range(self.width)] for x in range(self.height)
        ]

        self.predators = set()
        self.preys = set()

        for _ in range(10):
            self.predators.add(Predator(randint(0, self.width - 1), randint(0, self.height - 1), self.worldGrid))

        for _ in range(20):
            self.preys.add(Prey(randint(0, self.width - 1), randint(0, self.height - 1), self.worldGrid))

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
        blockSize = (min(windowWidth, windowHeight) - max(self.height, self.width)) / max(self.height, self.width)

        for row in range(self.height):
            for col in range(self.width):
                self.worldGrid[row][col].updateGrass()

                posX = (blockSize + 1) * row
                posY = (blockSize + 1) * col
                rect = pygame.Rect(posX, posY, blockSize + 1, blockSize + 1)

                # todo: replace with animating pictures
                if self.worldGrid[row][col].predator:
                    color = '#e63946'
                elif self.worldGrid[row][col].prey:
                    color = '#4361ee'
                elif self.worldGrid[row][col].hasGrass:
                    color = '#606c38'
                else:
                    color = self.worldGrid[row][col].color

                pygame.draw.rect(screen, color, rect, 0)

        pygame.display.flip()
