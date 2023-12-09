from __future__ import annotations
from random import random
import json

from predator import Predator
from prey import Prey

with open('./maps/map-settings.json', 'r') as f:
    mapSettings = json.load(f)


class GridCell:
    def __init__(self, x, y, color, grassGrowthProbability=0.0005, grassEnergy=1):
        self.x = x
        self.y = y
        self.predator: Predator | None = None
        self.prey: Prey | None = None
        self.grassGrowthProbability = grassGrowthProbability
        self.hasGrass = False
        self.grassEnergy = grassEnergy
        self.color = color
        self.type = next(filter(lambda mapType: mapType["color"] == color, mapSettings))["name"]

        match self.type:
            case 'water':
                self.grassGrowthProbability = 0
            case 'deep water':
                self.grassGrowthProbability = 0
            case 'shore':
                self.grassGrowthProbability = 0
            case 'savana':
                pass
            case 'plain':
                pass
            case 'beach':
                pass
            case 'moutain':
                pass
            case 'rock':
                pass
            case 'forest':
                self.grassGrowthProbability = 0.01

    def updateGrass(self):
        if not self.hasGrass and random() < self.grassGrowthProbability:
            self.hasGrass = True

    def updatePredatorParameters(self, predator: Predator):
        match self.type:
            case 'water':
                predator.energyLossRate = 2
            case 'deep water':
                predator.energyLossRate = 3
            case 'shore':
                pass
            case 'savana':
                pass
            case 'plain':
                pass
            case 'beach':
                pass
            case 'moutain':
                pass
            case 'rock':
                pass
            case 'forest':
                pass
    
    def getNeighboringCells(self, worldGrid) -> list[GridCell]:
        worldHeight = len(worldGrid)
        worldWidth = len(worldGrid[0])

        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i != 0 or j != 0) and (0 <= i + self.x < worldHeight) and (0 <= j + self.y < worldWidth):
                    neighbors.append(worldGrid[i + self.x][j + self.y])
        
        return neighbors

