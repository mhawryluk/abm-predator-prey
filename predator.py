from random import choice
from animal import Animal
from random import random


class Predator(Animal):
    def __init__(
            self, x, y, worldGrid,
            startEnergy=80,
            minEnergyToSurvive=1,
            energyLossRate=1,
            maxDaysToReproduce=20,
            reproductionProbability=1,
            minEnergyToReproduce=40,
            speed=2,
            radiusOfVision=200,
            maxEnergyToHunt=79,
            maxEnergyToEatPrey=100,
            minEnergyToSeekReproduction=80,
            energyLossPercentAfterReproduction=0.3,
    ):
        super().__init__(x, y, worldGrid, startEnergy, minEnergyToSurvive, energyLossRate, maxDaysToReproduce,
                         reproductionProbability, minEnergyToReproduce, speed, maxEnergyToEatPrey, radiusOfVision, energyLossPercentAfterReproduction)

        self.worldGrid[x][y].predator = self

        self.maxEnergyToHunt = maxEnergyToHunt
        self.maxEnergyToEatPrey = maxEnergyToEatPrey
        self.minEnergyToSeekReproduction = minEnergyToSeekReproduction

    def step(self):
        alive = self.checkAlive()
        if not alive:
            return False, None

        reproduced = self.reproduce() if self.energy > self.minEnergyToReproduce and random() < self.reproductionProbability else None
        self.move()
        self.eatPrey()
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
        closestCellWithPredator = None

        if self.energy < self.maxEnergyToHunt:
            for radius in range(1, self.radiusOfVision + 1):
                neighboringCells = self.worldGrid[self.x][self.y].getNeighboringCells(self.worldGrid, radius)
                cellsWithPrey = list(filter(lambda cell: cell.prey, neighboringCells))
                if cellsWithPrey:
                    closestCellWithPrey = cellsWithPrey[0]
                    break

        if self.energy > self.minEnergyToSeekReproduction:
            for radius in range(1, self.radiusOfVision + 1):
                neighboringCells = self.worldGrid[self.x][self.y].getNeighboringCells(self.worldGrid, radius)
                cellsWithPredator = list(filter(lambda cell: cell.predator, neighboringCells))
                if cellsWithPredator:
                    closestCellWithPredator = cellsWithPredator[0]
                    break

        emptyNeighbors = []
        for radius in range(1, self.speed + 1):
            neighbors = self.worldGrid[self.x][self.y].getNeighboringCells(self.worldGrid, radius)
            emptyNeighbors += list(filter(lambda cell: not cell.predator and not cell.prey and cell.type != 'water', neighbors))

        if emptyNeighbors:
            if closestCellWithPrey:
                move = min(emptyNeighbors, key=lambda cell: abs(cell.x - closestCellWithPrey.x) + abs(cell.y - closestCellWithPrey.y))
            elif closestCellWithPredator:
                move = min(emptyNeighbors, key=lambda cell: abs(cell.x - closestCellWithPredator.x) + abs(cell.y - closestCellWithPredator.y))
            else:
                move = choice(emptyNeighbors)

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
                self.energy *= (1-self.energyLossPercentAfterReproduction)
                candidate.energy *= (1-self.energyLossPercentAfterReproduction)
                return newPredator
