import pygame
import random
import math
from collections import deque
#import getFPS

pygame.init()
clock = pygame.time.Clock()

screenXsize = 250 # Sim size
screenYsize = 250
displayWindowX = 700 # Display size
displayWindowY = 700

screenSize = (displayWindowX, displayWindowY)
simulationSize = (screenXsize, screenYsize)
scalingFactor = screenSize[0] // simulationSize[0]  # Should be 6 in this case

displaySurface = pygame.display.set_mode(screenSize) # DisplaySurface determines the size of the window
screen = pygame.Surface(simulationSize) # screen handles the actual sim

backgroundColor = (0, 0, 0)

screen.fill(backgroundColor) 
pygame.display.set_caption("Slime Mold Sim")
pygame.display.update()

pi = math.pi

agentCount = 250
trailSize = 1
trailEvaporationRate = 0.03
#agentTrails = []


class Agent:
    def __init__(self, x: float, y: float, angle: float):
        self.x = x # x position
        self.y = y # y position
        self.angle = angle       # (angle of movement)
        self.trails = deque()
        

    def update(self):
        # X wall bounce
        if self.x < 0:
            self.angle = random.uniform(pi * 1.5, pi * 2.5)
        if self.x > screenYsize:
            self.angle = random.uniform(pi * .5, pi * 1.5)
        

        # Y wall bounce
        if self.y < 0:
            self.angle = random.uniform(0, pi)
        if self.y > screenXsize:
            self.angle = random.uniform(pi, 2 * pi)

        
        # Forward movement
        self.x += round(math.cos(self.angle), 2)
        self.y += round(math.sin(self.angle), 2)
        self.trails.append((self.x, self.y, 1.0))

    def trailEvaporation(self):
        
        newTrails = []
        #surface = pygame.Surface((screenXsize, screenYsize), pygame.SRCALPHA)

        for x, y, trailIntensity in self.trails:
            newTrailIntensity = round(trailIntensity - trailEvaporationRate, 2)
            if newTrailIntensity > 0:
                newTrails.append((x, y, newTrailIntensity))
                colorValue = int(newTrailIntensity * 255)
                pygame.draw.rect(screen, (colorValue, colorValue, colorValue), (x, y, trailSize, trailSize))
        
        self.trails = deque(newTrails)
        #screen.blit(surface, (0, 0))
        
        # i = 0
        # while i < (len(agentTrails)):
        #     print(f'agentTrails = {len(agentTrails)}')
            
        #     agentTrails[i] = (agentTrails[i][0], agentTrails[i][1], round(agentTrails[i][2] - trailEvaporationRate, 2))
        #     colorValue = agentTrails[i][2]
        #     pygame.draw.rect(screen, (colorValue * 255, colorValue * 255, colorValue * 255), (agentTrails[i][0], agentTrails[i][1], trailSize, trailSize)) 
        #     if agentTrails[i][2] == 0:
        #         agentTrails.pop(i)
        #     else:
        #         i += 1

    def drawAgent(self):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, trailSize, trailSize))



class FPS:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Verdana", 20)
        self.text = self.font.render(str(self.clock.get_fps()), True, (150, 150, 255))

    def render(self, display):
        self.text = self.font.render(str(round(self.clock.get_fps(), 1)), True, (150, 150, 255))
        display.blit(self.text, (10, 10))


def main():

    running = True
    #fps = getFPS.FPS()
    fps = FPS()


    agents = []
    for i in range(agentCount):
        agent = Agent(
            screenXsize / 2, # Spawns all agents in the middle of the screen
            screenYsize / 2, # ^
            (random.uniform(0, 2 * math.pi)) # Starts all agents looking in a random direction
        )
        agents.append(agent)
    
    while running:

        for event in pygame.event.get():             
            if event.type == pygame.QUIT: 
                running = False

        fps.clock.tick(60) # 60 FPS
        screen.fill(backgroundColor)
        


        for agent in agents: 
            agent.update()
            agent.drawAgent()
            agent.trailEvaporation()

        scaledSurface = pygame.transform.scale(screen, screenSize)
        displaySurface.blit(scaledSurface, (0, 0))
        fps.render(displaySurface)
        pygame.display.update()

if __name__ == "__main__":
    main()
