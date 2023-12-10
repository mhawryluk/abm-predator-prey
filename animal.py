

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
        radiusOfVision,
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
        self.radiusOfVision = radiusOfVision

    def checkAlive(self):
        return self.energy >= self.minEnergyToSurvive

    def updateDailyParameters(self):
        if self.daysToReproduce > 0:
            self.daysToReproduce -= 1
        
        self.energy -= self.energyLossRate

    def getInfo(self):
        return [
            f'energy: {self.energy}',
            f'energyLossRate: {self.energyLossRate}',
            f'minEnergyToSurvive: {self.minEnergyToSurvive}',
            f'daysToReproduce: {self.daysToReproduce}',
            f'speed: {self.speed}',
            f'maxEnergy: {self.maxEnergy}',
            f'minEnergyToReproduce: {self.minEnergyToReproduce}',
            f'reproductionProbability: {self.reproductionProbability}',
            f'radiusOfVision: {self.radiusOfVision}',
        ]
