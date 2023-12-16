from random import choice
from animal import Animal
from random import random
from math import floor


class Prey(Animal):

    def __init__(
        self, x, y, worldGrid, 
        startEnergy=50,
        minEnergyToSurvive=1, 
        energyLossRate=1, 
        maxDaysToReproduce=10,
        reproductionProbability=0.3,
        minEnergyToReproduce=20,
        speed=1.75,
        maxEnergy=100,
        radiusOfVision=40,
    ):
        super().__init__(x, y, worldGrid, startEnergy, minEnergyToSurvive, energyLossRate, maxDaysToReproduce, reproductionProbability, minEnergyToReproduce, speed, maxEnergy, radiusOfVision)
        
        self.worldGrid[x][y].prey = self

    def step(self):
        alive = self.checkAlive()
        if not alive:
            return False, None
        
        self.eatGrass()
        reproduced = self.reproduce() if self.energy > self.minEnergyToReproduce and random() < self.reproductionProbability else None
        self.move()
        self.updateDailyParameters()

        return alive, reproduced

    def eatGrass(self):
        cell = self.worldGrid[self.x][self.y]
        if cell.hasGrass:
            self.energy += cell.grassEnergy
            cell.hasGrass = False

    def move(self):
        cellsWithPredators = []
        cellsWithGrass = []

        for radius in range(1, self.radiusOfVision + 1):
            cells = self.worldGrid[self.x][self.y].getNeighboringCells(self.worldGrid, radius)
            cellsWithPredators += list(filter(lambda cell: cell.predator, cells))
            cellsWithGrass += list(filter(lambda cell: cell.hasGrass, cells))

        emptyNeighbors = []

        speed = floor(self.speed) + 1*(random() < self.speed - floor(self.speed))
        for radius in range(1, speed + 1):
            neighbors = self.worldGrid[self.x][self.y].getNeighboringCells(self.worldGrid, radius)
            emptyNeighbors += list(filter(lambda cell: not cell.predator and not cell.prey and cell.type != 'water', neighbors))

        if emptyNeighbors:
            if cellsWithPredators:
                averagePredatorX = sum(map(lambda cell: cell.x, cellsWithPredators)) / len(cellsWithPredators)
                averagePredatorY = sum(map(lambda cell: cell.y, cellsWithPredators)) / len(cellsWithPredators)

                emptyNeighbors.sort(key=lambda cell: abs(cell.x - averagePredatorX) + abs(cell.y - averagePredatorY))
                move = emptyNeighbors[-1]
            elif cellsWithGrass:
                averageGrassX = sum(map(lambda cell: cell.x, cellsWithGrass)) / len(cellsWithGrass)
                averageGrassY = sum(map(lambda cell: cell.y, cellsWithGrass)) / len(cellsWithGrass)

                emptyNeighbors.sort(key=lambda cell: abs(cell.x - averageGrassX) + abs(cell.y - averageGrassY))
                move = emptyNeighbors[0]
            else:
                move = choice(emptyNeighbors)

            self.worldGrid[self.x][self.y].prey = None
            self.x = move.x
            self.y = move.y
            self.worldGrid[self.x][self.y].prey = self

    def reproduce(self):
        if self.daysToReproduce > 0:
            return
        
        candidate = None
        bestCandidateEnergy = -1

        neighboringCells = self.worldGrid[self.x][self.y].getNeighboringCells(self.worldGrid)

        for cell in neighboringCells:
            if neighborPrey := cell.prey:
                if neighborPrey.energy > bestCandidateEnergy and neighborPrey.daysToReproduce == 0:
                    candidate = neighborPrey
                    bestCandidateEnergy = neighborPrey.energy

        if candidate:
            emptyCell = None
            for cell in neighboringCells:
                if not cell.predator and not cell.prey and cell.type != 'water':
                    emptyCell = cell
                    break
            
            if emptyCell:
                newPrey = Prey(emptyCell.x, emptyCell.y, self.worldGrid, startEnergy=((self.energy + candidate.energy)/2))
                self.daysToReproduce = self.maxDaysToReproduce
                return newPrey
