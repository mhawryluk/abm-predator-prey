from __future__ import annotations
from random import random
import json

from predator import Predator
from prey import Prey

with open('./maps/map-settings-2.json', 'r') as f:
    mapSettings = json.load(f)


class GridCell:
    def __init__(self, x, y, color, grassGrowthProbability=0.0008, grassEnergy=10):
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
                self.grassGrowthProbability = 0
            case 'moutain':
                self.grassGrowthProbability = 0
            case 'rock':
                self.grassGrowthProbability = 0
            case 'forest':
                self.grassGrowthProbability = 0.003

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
    
    def getNeighboringCells(self, worldGrid, radius=1) -> list[GridCell]:
        worldHeight = len(worldGrid)
        worldWidth = len(worldGrid[0])

        neighbors = []
        neighbors.append(worldGrid
                         [(radius * (-radius) + self.x + worldHeight) % worldHeight]
                         [(radius * (-radius) + self.y + worldWidth) % worldWidth])
        neighbors.append(worldGrid
                         [(radius * radius + self.x + worldHeight) % worldHeight]
                         [(radius * radius + self.y + worldWidth) % worldWidth])

        neighbors.append(worldGrid
                         [(radius * (-radius) + self.x + worldHeight) % worldHeight]
                         [(radius * radius + self.y + worldWidth) % worldWidth])
        neighbors.append(worldGrid
                         [(radius * radius + self.x + worldHeight) % worldHeight]
                         [(radius * (-radius) + self.y + worldWidth) % worldWidth])

        for i in range(-radius+1, radius):
                neighbors.append(worldGrid
                                 [(radius*i + self.x + worldHeight) % worldHeight]
                                 [(radius*(-radius) + self.y + worldWidth) % worldWidth])
                neighbors.append(worldGrid
                                 [(radius * i + self.x + worldHeight) % worldHeight]
                                 [(radius * radius + self.y + worldWidth) % worldWidth])

                neighbors.append(worldGrid
                                 [(radius * (-radius) + self.x + worldHeight) % worldHeight]
                                 [(radius * i + self.y + worldWidth) % worldWidth])
                neighbors.append(worldGrid
                                 [(radius * radius + self.x + worldHeight) % worldHeight]
                                 [(radius * i + self.y + worldWidth) % worldWidth])
        
        return neighbors

