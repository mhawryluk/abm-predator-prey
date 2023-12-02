from random import choice
from animal import Animal


class Predator(Animal):
    def __init__(self, x, y, worldGrid, startEnergy=50, minEnergyToSurvive=1, energyLossRate=1, maxDaysToReproduce=5):
        super().__init__(x, y, worldGrid, startEnergy, minEnergyToSurvive, energyLossRate, maxDaysToReproduce)

        self.worldGrid[x][y].predator = self

    def step(self):
        alive = self.checkAlive()
        if not alive:
            return False, None
        
        self.energy -= self.energyLossRate
        self.eatPrey()
        reproduced = self.reproduce()
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
                self.daysToReproduce = self.maxDaysToReproduce
                return newPredator