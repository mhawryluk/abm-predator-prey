from random import choice
from animal import Animal
from random import random


class Predator(Animal):
    def __init__(
            self, x, y, worldGrid,
            startEnergy=200,
            minEnergyToSurvive=1,
            energyLossRate=1,
            maxDaysToReproduce=5,
            reproductionProbability=0.8,
            minEnergyToReproduce=20,
    ):
        super().__init__(x, y, worldGrid, startEnergy, minEnergyToSurvive, energyLossRate, maxDaysToReproduce,
                         reproductionProbability, minEnergyToReproduce)

        self.worldGrid[x][y].predator = self

    def step(self):
        alive = self.checkAlive()
        if not alive:
            return False, None

        self.eatPrey()
        reproduced = self.reproduce() if self.energy > self.minEnergyToReproduce and random() < self.reproductionProbability else None
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
                if neighborPredator.energy > bestCandidateEnergy and neighborPredator.daysToReproduce == 0:
                    candidate = neighborPredator
                    bestCandidateEnergy = neighborPredator.energy

        if candidate:
            emptyCell = None
            for cell in neighboringCells:
                if not cell.predator and not cell.prey:
                    emptyCell = cell
                    break

            if emptyCell:
                newPredator = Predator(emptyCell.x, emptyCell.y, self.worldGrid, startEnergy=(self.energy + candidate.energy)/2)
                self.daysToReproduce = self.maxDaysToReproduce
                candidate.daysToReproduce = candidate.maxDaysToReproduce
                return newPredator
