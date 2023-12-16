import pygame
from pygame.locals import (
    K_RIGHT,
    KEYDOWN,
    QUIT,
    K_SPACE,
)
import matplotlib.pyplot as plt
from model import Model


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Predator-Prey Agent Based Simulation')
    
    windowWidth = 800
    windowHeight = 800
    
    screen = pygame.display.set_mode([windowWidth, windowHeight])
    screen.fill((0, 0, 0))

    model = Model('./maps/map-200x200-1.json')
    model.draw(screen, windowWidth, windowHeight)

    time_delay = 100  # 0.2 s
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, time_delay)
    
    plt.ion()
    
    predatorCounts = []
    preyCounts = []
    predatorGraph = plt.plot(predatorCounts, color='#f72634', linewidth=3, label='Predators')[0]
    preyGraph = plt.plot(preyCounts, color='#a713f6', linewidth=3, label='Prey')[0]
    
    xLim = 100
    yLim = 100   
    plt.xlim([0, xLim])
    plt.ylim([0, yLim])
    
    plt.xlabel('day')
    plt.ylabel('count')
    plt.title('Population counts')
    ax = plt.gca()
    ax.set_facecolor('#86BBD8')
    plt.legend()
    
    running = True
    paused = False

    day = 0

    while running:
        for event in pygame.event.get():   
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN and event.key == K_SPACE:
                paused = not paused
            if event.type == timer_event or (event.type == KEYDOWN and event.key == K_RIGHT):
                if not paused:
                    for _ in range(87):
                        model.step()

                    if model.simulationDay > day:
                        day = model.simulationDay

                        predatorCount = model.getPredatorCount()
                        predatorCounts.append(predatorCount)

                        preyCount = model.getPreyCount()
                        preyCounts.append(preyCount)

                        if predatorCount == 0 and preyCount == 0:
                            paused = True

                        if day > xLim:
                            xLim = 2*day
                            plt.xlim([0, xLim])

                        if predatorCount > yLim:
                            yLim = 2*predatorCount
                            plt.ylim([0, yLim])

                        if preyCount > yLim:
                            yLim = 2*preyCount
                            plt.ylim([0, yLim])

                        predatorGraph.set_data(list(range(len(predatorCounts))), predatorCounts)
                        preyGraph.set_data(list(range(len(preyCounts))), preyCounts)

                model.draw(screen, windowWidth, windowHeight)
                    
    pygame.quit()
