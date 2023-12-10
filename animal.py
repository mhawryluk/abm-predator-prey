

class Animal:
    def __init__(
        self, x, y, worldGrid, 
        startEnergy, 
        minEnergyToSurvive, 
        energyLossRate, 
        maxDaysToReproduce,
        reproductionProbability,
        minEnergyToReproduce,
        speed,
        maxEnergy,
    ):
        self.x = x
        self.y = y

        self.worldGrid = worldGrid
        self.worldHeight = len(worldGrid)
        self.worldWidth = len(worldGrid[0])

        self.minEnergyToSurvive = minEnergyToSurvive
        self.energyLossRate = energyLossRate
        self.energy = startEnergy
        self.daysToReproduce = maxDaysToReproduce
        self.maxDaysToReproduce = maxDaysToReproduce
        self.reproductionProbability = reproductionProbability
        self.minEnergyToReproduce = minEnergyToReproduce
        self.speed = speed
        self.maxEnergy = maxEnergy

    def checkAlive(self):
        return self.energy >= self.minEnergyToSurvive

    def updateDailyParameters(self):
        if self.daysToReproduce > 0:
            self.daysToReproduce -= 1
        
        self.energy -= self.energyLossRate
