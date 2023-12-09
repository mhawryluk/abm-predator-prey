import pygame
import json
from random import randint, random
from gridCell import GridCell
from predator import Predator
from prey import Prey
from queue import PriorityQueue


class Task:
    def __init__(self, func, priority, *args):
        self.func = func
        self.priority = priority
        self.args = args

    def __lt__(self, other):
        return self.priority < other.priority

    def __gt__(self, other):
        return self.priority > other.priority

    def __eq__(self, other):
        return self.priority > other.priority

    def __call__(self):
        self.func(*self.args)

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

        self.simulationQueue = PriorityQueue()

    def getPredatorCount(self):
        return len(self.predators)

    def getPreyCount(self):
        return len(self.preys)

    def simulatePredator(self, predator: Predator):
        alive, reproduced = predator.step()
        if not alive:
            self.predators.remove(predator)
            self.worldGrid[predator.x][predator.y].predator = None

        if reproduced:
            self.predators.add(reproduced)

    def simulatePrey(self, prey: Prey):
        alive, reproduced = prey.step()
        if not alive:
            self.preys.remove(prey)
            self.worldGrid[prey.x][prey.y].prey = None

        if reproduced:
            self.preys.add(reproduced)

    def step(self):
        if self.simulationQueue.empty():
            self.simulationDay += 1

            for predator in list(self.predators):
                self.simulationQueue.put(Task(self.simulatePredator, self.simulationDay + random(), predator))

            for prey in list(self.preys):
                self.simulationQueue.put(Task(self.simulatePrey, self.simulationDay + random(), prey))

            for row in range(self.height):
                for col in range(self.width):
                    self.simulationQueue.put(Task(lambda r, c: self.worldGrid[r][c].updateGrass(), self.simulationDay + random(), row, col))
        else:
            self.simulationQueue.get()()

    def draw(self, screen, windowWidth, windowHeight):
        blockSize = (min(windowWidth, windowHeight) - max(self.height, self.width)) / max(self.height, self.width)

        for row in range(self.height):
            for col in range(self.width):

                posX = (blockSize + 1) * row
                posY = (blockSize + 1) * col
                rect = pygame.Rect(posX, posY, blockSize + 1, blockSize + 1)

                if self.worldGrid[row][col].predator:
                    color = '#f72634'
                elif self.worldGrid[row][col].prey:
                    color = '#a713f6'
                elif self.worldGrid[row][col].hasGrass:
                    color = '#606c38'
                else:
                    color = self.worldGrid[row][col].color

                pygame.draw.rect(screen, color, rect, 0)

        pygame.display.flip()
