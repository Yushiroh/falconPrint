import pygame
import sys
import threading
import os
from time import sleep

APPWIDTH, APPHEIGHT = 800, 480
FPS = 60
pygame.init()
pygame.display.set_caption("Final System")
sensorActivated = False
timerTickState = False


#COLORS
Black = (0,0,0)
White = (255, 255, 255)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((APPWIDTH, APPHEIGHT))
        self.clock = pygame.time.Clock()

        self.stateManager = stateManager('scene1')
        self.scene1 = scene1(self.screen, self.stateManager)
        self.scene2 = scene2(self.screen, self.stateManager)
        
        self.states = {'scene1': self.scene1, 'scene2': self.scene2, 'scene3': self.scene3
                        , 'scene4': self.scene4, 'scene5': self.scene5, 'scene6': self.scene6, 'scene7': self.scene7}

    def run(self):
        while True:
            mouse = pygame.mouse.get_pos()
            clicker = pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            self.states[self.stateManager.getState()].run(mouse,clicker)

            #print(mouse)
            #print(counter)

            pygame.display.update()
            self.clock.tick(FPS)

class scene1:
    def __init__(self, display, stateManager):
        self.display = display
        self.stateManager = stateManager

    def run(self, mouse, clicker):
       pass

class scene2:
    def __init__(self, display, stateManager):
        self.display = display
        self.stateManager = stateManager
        self.clock = pygame.time.Clock()

    def run(self, mouse, clicker):
        pass
  

class stateManager:
    def __init__(self, currentScene):
        self.currentScene = currentScene
    
    def getState(self):
        return self.currentScene
    
    def setState(self, state):
        self.currentScene = state

if __name__ == '__main__':
    game = Game()
    game.run()