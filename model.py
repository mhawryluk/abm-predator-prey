import pygame
import pygame.freetype
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

        for _ in range(15):
            self.predators.add(
                Predator(randint(40, 60),
                         randint(20, 30),
                         self.worldGrid)
            )

        for _ in range(10):
            self.predators.add(
                Predator(randint(30, 60),
                         randint(150, 170),
                         self.worldGrid)
            )

        for _ in range(15):
            self.predators.add(
                Predator(randint(170, 190),
                         randint(90, 110),
                         self.worldGrid)
            )

        for _ in range(20):
            self.preys.add(
                Prey(randint(10, 30), randint(10, 30), self.worldGrid)
            )

        for _ in range(30):
            self.preys.add(
                Prey(randint(65, 80), randint(40, 60), self.worldGrid)
            )

        for _ in range(20):
            self.preys.add(
                Prey(randint(165, 180), randint(40, 60), self.worldGrid)
            )

        for _ in range(30):
            self.preys.add(
                Prey(randint(45, 65), randint(140, 160), self.worldGrid)
            )

        for _ in range(20):
            self.preys.add(
                Prey(randint(20, 40), randint(90, 110), self.worldGrid)
            )

        self.simulationQueue = PriorityQueue()
        self.font = pygame.freetype.SysFont('sans', 16)

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

    def simulateGrass(self):
        for row in range(self.height):
            for col in range(self.width):
                if self.worldGrid[row][col].type != 'water':
                    self.worldGrid[row][col].updateGrass()

    def step(self):
        if self.simulationQueue.empty():
            self.simulationDay += 1

            for predator in list(self.predators):
                self.simulationQueue.put(Task(self.simulatePredator, self.simulationDay + random(), predator))

            for prey in list(self.preys):
                self.simulationQueue.put(Task(self.simulatePrey, self.simulationDay + random(), prey))

            self.simulationQueue.put(
                Task(self.simulateGrass, self.simulationDay + random()))
        else:
            self.simulationQueue.get()()

    def draw(self, screen, windowWidth, windowHeight):
        blockSize = (min(windowWidth, windowHeight) - max(self.height, self.width)) / max(self.height, self.width) + 1

        for row in range(self.height):
            for col in range(self.width):

                posX = blockSize * row
                posY = blockSize * col
                rect = pygame.Rect(posX, posY, blockSize, blockSize)

                if self.worldGrid[row][col].predator:
                    color = '#f72634'
                elif self.worldGrid[row][col].prey:
                    color = '#a713f6'
                elif self.worldGrid[row][col].hasGrass:
                    color = '#606c38'
                else:
                    color = self.worldGrid[row][col].color

                pygame.draw.rect(screen, color, rect, 0)

        mousePosition = pygame.mouse.get_pos()
        cellX = int(mousePosition[0] // blockSize)
        cellY = int(mousePosition[1] // blockSize)

        if 0 <= cellX < self.height and 0 <= cellY < self.width:
            cell = self.worldGrid[cellX][cellY]
            info = []
            if cell.predator:
                info = cell.predator.getInfo()
            elif cell.prey:
                info = cell.prey.getInfo()

            for i, infoLine in enumerate(info):
                self.font.render_to(screen, (mousePosition[0], mousePosition[1] + i * 14), '   ' + infoLine + '   ', '#000000',
                                    '#86BBD8')

        pygame.display.flip()
