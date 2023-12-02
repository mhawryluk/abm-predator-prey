from random import random


class GridCell:
    def __init__(self, x, y, grassGrowthProbability=0.0005, grassEnergy=1):
        self.x = x
        self.y = y
        self.predator = None
        self.prey = None
        self.grassGrowthProbablity = grassGrowthProbability
        self.hasGrass = False
        self.grassEnergy = grassEnergy
    
    def updateGrass(self):
        if not self.hasGrass and random() < self.grassGrowthProbablity:
            self.hasGrass = True
    
    def getNeighboringCells(self, worldGrid):
        worldHeight = len(worldGrid)
        worldWidth = len(worldGrid[0])

        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i != 0 or j != 0) and (0 <= i + self.x < worldHeight) and (0 <= j + self.y < worldWidth):
                    neighbors.append(worldGrid[i + self.x][j + self.y])
        
        return neighbors

