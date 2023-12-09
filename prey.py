from random import choice
from animal import Animal
from random import random


class Prey(Animal):

    def __init__(
        self, x, y, worldGrid, 
        startEnergy=100, 
        minEnergyToSurvive=1, 
        energyLossRate=1, 
        maxDaysToReproduce=4,
        reproductionProbability=0.2,
    ):
        super().__init__(x, y, worldGrid, startEnergy, minEnergyToSurvive, energyLossRate, maxDaysToReproduce, reproductionProbability)
        
        self.worldGrid[x][y].prey = self

    def step(self):
        alive = self.checkAlive()
        if not alive:
            return False, None
        
        self.eatGrass()
        reproduced = self.reproduce() if random() < self.reproductionProbability else None
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
                if neighborPrey.energy > bestCandidateEnergy and neighborPrey.daysToReproduce == 0:
                    candidate = neighborPrey
                    bestCandidateEnergy = neighborPrey.energy

        if candidate:
            emptyCell = None
            for cell in neighboringCells:
                if not cell.predator and not cell.prey:
                    emptyCell = cell
                    break
            
            if emptyCell:
                newPrey = Prey(emptyCell.x, emptyCell.y, self.worldGrid, startEnergy=((self.energy + candidate.energy)/2))
                self.daysToReproduce = self.maxDaysToReproduce
                return newPrey
