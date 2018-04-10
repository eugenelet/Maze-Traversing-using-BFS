from pygame.locals import *
import pygame
from time import sleep
import numpy as np

BLOCK_SIZE = 30
MAZE_X = 15
MAZE_Y = 15

class Player:
    def __init__(self, pos):
        self.x = int(pos[0])
        self.y = int(pos[1])
        self.speed = 1
 
    def moveRight(self, maze):
        if(self.x + self.speed>=MAZE_X):
            return self.y, self.x
        if(maze.maze[self.x + self.speed + self.y*MAZE_X]==1):
            return self.y, self.x
        self.x = self.x + self.speed
        return self.y, self.x
 
    def moveLeft(self, maze):
        if(self.x - self.speed<0):
            return self.y, self.x
        if(maze.maze[self.x - self.speed + self.y*MAZE_X]==1):
            return self.y, self.x
        self.x = self.x - self.speed
        return self.y, self.x
 
    def moveUp(self, maze):
        if(self.y - self.speed<0):
            return self.y, self.x
        if(maze.maze[self.x + (self.y - self.speed)*MAZE_X] == 1):
            return self.y, self.x
        self.y = self.y - self.speed
        return self.y, self.x
 
    def moveDown(self, maze):
        if(self.y + self.speed >= MAZE_Y):
            return self.y, self.x
        if(maze.maze[self.x + (self.y + self.speed)*MAZE_X] == 1):
            return self.y, self.x
        self.y = self.y + self.speed
        return self.y, self.x

    def draw(self,display_surf,image_surf):
        display_surf.blit(image_surf, (self.x * BLOCK_SIZE, self.y * BLOCK_SIZE))


class Reward:
    def __init__(self, pos):
        self.num_reward = len(pos)
        self.x = np.empty([self.num_reward])
        self.y = np.empty([self.num_reward])
        for i, _pos in enumerate(pos):
            self.x[i], self.y[i] = _pos

    def draw(self,display_surf,image_surf):
        for i in range(self.num_reward):
            display_surf.blit(image_surf, (self.x[i] * BLOCK_SIZE, self.y[i] * BLOCK_SIZE))

    def check_reward(self, coor):
        for i in range(self.num_reward):
            if(self.x[i]==coor[1] and self.y[i]==coor[0]):
                self.x = np.delete(self.x, i)
                self.y = np.delete(self.y, i)
                self.num_reward -= 1
                break



class Maze:
    def __init__(self, dir):
       self.M = MAZE_X
       self.N = MAZE_Y
       self.maze = np.genfromtxt(dir, delimiter=',')
       self.maze = self.maze.flatten()
 
    def draw(self,display_surf,image_surf):
       bx = 0
       by = 0
       for i in range(0,self.M*self.N):
           if self.maze[ bx + (by*self.M) ] == 1:
               display_surf.blit(image_surf,( bx * BLOCK_SIZE,
                by * BLOCK_SIZE))
 
           bx = bx + 1
           if bx > self.M-1:
               bx = 0 
               by = by + 1
 
 
class App:
 
    windowWidth = BLOCK_SIZE * MAZE_X
    windowHeight = BLOCK_SIZE * MAZE_Y
    player = 0
 
    def __init__(self, init_dir, maze_dir):
        self._running = True
        self._display_surf = None
        self._player_surf = None
        self._block_surf = None
        init = np.genfromtxt(init_dir, delimiter=',')
        self.player = Player(init[0])
        self.reward = Reward(init[1:])
        self.maze = Maze(maze_dir)
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
 
        pygame.display.set_caption('IC Lab 2018 Mid Term')
        self._running = True
        self._player_surf = pygame.image.load("sprites/" + "player.png").convert()
        self._block_surf = pygame.image.load("sprites/" + "wall.png").convert()
        self._reward_surf = pygame.image.load("sprites/" + "reward.png").convert()
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
 
    def on_loop(self):
        pass
 
    def on_render(self):
        self._display_surf.fill((0,0,0))
        self.player.draw(self._display_surf, self._player_surf)
        self.reward.draw(self._display_surf, self._reward_surf)
        self.maze.draw(self._display_surf, self._block_surf)
        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running and self.reward.num_reward>0):
            sleep(0.05)
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            coor = (0,0)
            if (keys[K_RIGHT]):
                coor = self.player.moveRight(self.maze)

            if (keys[K_LEFT]):
                coor = self.player.moveLeft(self.maze)
 
            if (keys[K_UP]):
                coor = self.player.moveUp(self.maze)
 
            if (keys[K_DOWN]):
                coor = self.player.moveDown(self.maze)
 
            if (keys[K_ESCAPE]):
                self._running = False
            
            self.reward.check_reward(coor)
            self.on_loop()
            self.on_render()

        self.on_cleanup()
 
if __name__ == "__main__" :
    for i in range(5):
        maze_dir = 'maze/' + str(i).zfill(3) + '.txt' 
        init_dir = 'init/' + str(i).zfill(3) + '.txt'
        theApp = App(init_dir, maze_dir)
        theApp.on_execute()
