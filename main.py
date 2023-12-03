import pygame
from pygame.locals import (
    K_RIGHT,
    KEYDOWN,
    QUIT,
)
import matplotlib.pyplot as plt
from model import Model


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Predator-Prey Agent Based Simulation')
    
    windowWidth = 800
    windowHeight = 800
    
    screen = pygame.display.set_mode([windowWidth, windowHeight])
    screen.fill((255, 255, 255))

    model = Model(100, 100)
    model.draw(screen, windowWidth, windowHeight)

    time_delay = 200  # 0.2 s
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, time_delay)
    
    plt.ion()
    
    predatorCounts = []
    preyCounts = []
    predatorGraph = plt.plot(predatorCounts, color='#e63946', linewidth=3, label='Predators')[0]
    preyGraph = plt.plot(preyCounts, color='#4361ee', linewidth=3, label='Prey')[0]
    
    xLim = 100
    yLim = 100   
    plt.xlim([0, xLim])
    plt.ylim([0, yLim])
    
    plt.xlabel('day')
    plt.ylabel('count')
    plt.title('Population counts')
    ax = plt.gca()
    ax.set_facecolor('#fefae0')
    plt.legend()
    
    running = True

    while running:
        
        for event in pygame.event.get():   
            if event.type == QUIT:
                running = False
            
            if event.type == timer_event or (event.type == KEYDOWN and event.key == K_RIGHT):
                model.step()

                predatorCount = model.getPredatorCount()
                predatorCounts.append(predatorCount)

                preyCount = model.getPreyCount()
                preyCounts.append(preyCount)

                day = model.simulationDay

                if day > xLim:
                    xLim = 2*day
                    plt.xlim([0, xLim])

                if predatorCount > yLim:
                    yLim = 2*predatorCount
                    plt.ylim([0, yLim])

                if preyCount > yLim:
                    yLim = 2*preyCount
                    plt.ylim([0, yLim])

                model.draw(screen, windowWidth, windowHeight)
                predatorGraph.set_data(list(range(day)), predatorCounts)
                preyGraph.set_data(list(range(day)), preyCounts)
                    
    pygame.quit()
