from pygame.locals import *
import pygame
from time import sleep
import numpy as np
from collections import deque
import argparse

BLOCK_SIZE = 30
MAZE_X = 15
MAZE_Y = 15

# For backtrack
LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4
START = 5

class Player:
    def __init__(self, pos):
        self.x = int(pos[0])
        self.y = int(pos[1])
        self.speed = 1
 
    def currentPos(self):
        return self.y, self.x
 
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
                return True



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
        global maze_num
        if args.vis:
            if self.on_init() == False:
                self._running = False
 
        coor = self.player.currentPos()
        coor_queue = deque([])
        visited = np.zeros([MAZE_Y, MAZE_X])
        backtrack = np.zeros([MAZE_Y, MAZE_X])

        path = [] # Stores shortest path to reward
        path.append((self.player.x, self.player.y))

        backtrack[self.player.y, self.player.x] = START
        visited[self.player.y, self.player.x] = 1
        while( self.reward.num_reward > 0 ):

            if args.vis:
                sleep(0.05)

            new_coor = self.player.moveRight(self.maze)
            if(new_coor!=coor):
                self.player.moveLeft(self.maze)
                if(visited[new_coor]!=1):
                    coor_queue.appendleft(new_coor)
                    backtrack[new_coor] = LEFT
                    visited[new_coor] = 1

            new_coor = self.player.moveLeft(self.maze)
            if(new_coor != coor):
                self.player.moveRight(self.maze)
                if(visited[new_coor]!=1):
                    coor_queue.appendleft(new_coor)
                    backtrack[new_coor] = RIGHT
                    visited[new_coor] = 1
        
            new_coor = self.player.moveUp(self.maze)
            if(new_coor != coor):
                self.player.moveDown(self.maze)
                if(visited[new_coor]!=1):
                    coor_queue.appendleft(new_coor)
                    backtrack[new_coor] = DOWN
                    visited[new_coor] = 1
    
            new_coor = self.player.moveDown(self.maze)
            if(new_coor != coor):
                self.player.moveUp(self.maze)
                if(visited[new_coor]!=1):
                    coor_queue.appendleft(new_coor)
                    backtrack[new_coor] = UP
                    visited[new_coor] = 1

            self.player.y, self.player.x = coor_queue[-1]
            coor = self.player.currentPos()
            coor_queue.pop()

            if( self.reward.check_reward(coor) ):
                visited = np.zeros([MAZE_Y, MAZE_X])
                coor_queue = deque([])
                coor_tmp = coor

                _path = deque([])
                while(backtrack[coor] != START):
                    if args.vis:
	                    sleep(0.05)
                    _path.appendleft((coor[1],coor[0]))
                    direction = backtrack[coor]
                    if direction == LEFT:
                        coor = self.player.moveLeft(self.maze)
                    if direction == RIGHT:
                        coor = self.player.moveRight(self.maze)
                    if direction == UP:
                        coor = self.player.moveUp(self.maze)
                    if direction == DOWN:
                        coor = self.player.moveDown(self.maze)

                    # Update display
                    if args.vis:
                        self.on_loop()
                        self.on_render()
                
                path.extend(list(_path))


                # Store shortest path to first reward and terminate game

                # Reinitialize for next BFS (remove the break above)
                coor = coor_tmp
                self.player.y, self.player.x = coor
                visited = np.zeros([MAZE_Y, MAZE_X])
                backtrack = np.zeros([MAZE_Y, MAZE_X])
                visited[coor] = 1
                backtrack[coor] = START

            if args.vis:
                self.on_loop()
                self.on_render()
        self.on_cleanup()
        f = open('ans/' + str(maze_num).zfill(3) + '.txt', 'wb')
        np.savetxt(f, path, delimiter=',', fmt='%s')
        f.close()
 
if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument('--vis', const=True, nargs='?', type=bool,
                        default=False, help='Visualize formation of maze')
    args = parser.parse_args()

    for i in range(5):
        print i
        maze_num = i
        maze_dir = 'maze/' + str(i).zfill(3) + '.txt' 
        init_dir = 'init/' + str(i).zfill(3) + '.txt'
        theApp = App(init_dir, maze_dir)
        theApp.on_execute()
