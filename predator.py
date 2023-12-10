from random import choice
from animal import Animal
from random import random


class Predator(Animal):
    def __init__(
            self, x, y, worldGrid,
            startEnergy=50,
            minEnergyToSurvive=1,
            energyLossRate=1,
            maxDaysToReproduce=10,
            reproductionProbability=0.2,
            minEnergyToReproduce=40,
            speed=2,
            radiusOfVision=20,
            maxEnergyToHunt=51,
            maxEnergyToEatPrey=200,
    ):
        super().__init__(x, y, worldGrid, startEnergy, minEnergyToSurvive, energyLossRate, maxDaysToReproduce,
                         reproductionProbability, minEnergyToReproduce, speed, maxEnergyToEatPrey, radiusOfVision)

        self.worldGrid[x][y].predator = self

        self.maxEnergyToHunt = maxEnergyToHunt
        self.maxEnergyToEatPrey = maxEnergyToEatPrey

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
        if self.energy >= self.maxEnergyToEatPrey:
            return

        neighbors = self.worldGrid[self.x][self.y].getNeighboringCells(self.worldGrid)
        prey = list(filter(lambda cell: cell.prey, neighbors))

        if prey:
            weakestPrey = min(prey, key=lambda p: p.prey.energy).prey
            self.energy += weakestPrey.energy
            weakestPrey.energy = 0

    def move(self):
        closestCellWithPrey = None
        if self.energy < self.maxEnergyToHunt:
            for radius in range(1, self.radiusOfVision + 1):
                cells = self.worldGrid[self.x][self.y].getNeighboringCells(self.worldGrid, radius)
                cellsWithPrey = list(filter(lambda cell: cell.prey, cells))
                if cellsWithPrey:
                    closestCellWithPrey = cellsWithPrey[0]
                    break

        emptyNeighbors = []
        for radius in range(1, self.speed + 1):
            neighbors = self.worldGrid[self.x][self.y].getNeighboringCells(self.worldGrid, radius)
            emptyNeighbors += list(filter(lambda cell: not cell.predator and not cell.prey and cell.type != 'water', neighbors))

        if emptyNeighbors:
            if closestCellWithPrey is None:
                move = choice(emptyNeighbors)
            else:
                emptyNeighbors.sort(key=lambda cell: abs(cell.x - closestCellWithPrey.x) + abs(cell.y - closestCellWithPrey.y))
                move = emptyNeighbors[0]

            self.worldGrid[self.x][self.y].predator = None
            self.x = move.x
            self.y = move.y
            self.worldGrid[self.x][self.y].predator = self
            self.worldGrid[self.x][self.y].updatePredatorParameters(self)


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
                if not cell.predator and not cell.prey and cell.type != 'water':
                    emptyCell = cell
                    break

            if emptyCell:
                newPredator = Predator(emptyCell.x, emptyCell.y, self.worldGrid, startEnergy=(self.energy + candidate.energy)/2)
                self.daysToReproduce = self.maxDaysToReproduce
                candidate.daysToReproduce = candidate.maxDaysToReproduce
                return newPredator
