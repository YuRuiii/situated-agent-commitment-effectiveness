import random
import numpy as np
from enum import Enum
from dijkstra import Dijkstra
random.seed(0)
np.random.seed(0)

AGENT = 1
OBSTACLE = 2
HOLE = 3

class Hole:
    def __init__(self, pos, gestation, lifetime):
        self.pos = pos
        self.gestation = gestation
        self.lifetime = lifetime
        
class Obstacle:
    def __init__(self, pos):
        self.pos = pos

class Grid:
    def __init__(self, args):
        self.size = args.grid_size
        self.grid = np.zeros([self.size, self.size], int)
        self.obstacles = [self._set_obstacle(mode='random') for _ in range(args.n_obstacle)] if not args.obstacles else [self._set_obstacle(pos) for pos in args.obstacles]
        self.waiting_holes = [self._gen_hole(args.gest_range, args.lt_range) for _ in range(args.n_hole)]
        self.alive_holes = []
        self.time = 0
        self._set_holes()
    
    def _set_obstacle(self, pos=None, mode='random'):
        """
        Returns:
            Obstacle: an Obstacle object with a random position
        """
        assert pos is None or (isinstance(pos, tuple) and len(pos) == 2), f'Invalid position {pos}'
        assert mode in ['random', 'fixed'], f'Invalid mode {mode}'
        if mode == 'random':
            pos = (random.randint(0, self.size-1), random.randint(0, self.size-1))
            # print(f'self.grid[{pos}] is {self.grid[pos]}')
            while self.grid[pos] != 0:
                pos = (random.randint(0, self.size-1), random.randint(0, self.size-1))
        elif mode == 'fixed':
            pass
        self.grid[pos] = OBSTACLE
        return Obstacle(pos)
    
    def _gen_hole(self, gest_range, lt_range):
        """Generate holes to appear in the grid in the game
        
        Args:
            gest_range (tuple): range of gestation of holes
            lt_range (tuple): range of lifetime of holes
            
        Returns:
            Hole: a Hole object with a random position, gestation and lifetime
        """
        pos = (random.randint(0, self.size-1), random.randint(0, self.size-1))
        # print(f'self.grid[{pos}] is {self.grid[pos]}')
        while self.grid[pos] != 0:
            pos = (random.randint(0, self.size-1), random.randint(0, self.size-1))
        lifetime = random.randint(lt_range[0], lt_range[1])
        gestation = random.randint(gest_range[0], gest_range[1])
        return Hole(pos, gestation, lifetime)
    
    def _set_holes(self):
        """Set alive and waiting holes in the grid according to the current time
        """
        for hole in self.waiting_holes:
            if hole not in self.alive_holes and hole.gestation <= self.time <= hole.gestation + hole.lifetime:
                self.grid[hole.pos] = HOLE
                self.alive_holes.append(hole)
                self.waiting_holes.remove(hole)
        for hole in self.alive_holes:
            if self.time > hole.gestation + hole.lifetime:
                self.grid[hole.pos] = 0
                self.alive_holes.remove(hole)
    
    def update(self):
        self.time += 1
        self._set_holes()
    
class Agent:
    def __init__(self, args):
        self.pos = (args.grid_size//2, args.grid_size//2)
        self.gamma = args.gamma
        self.agent_planning_time = args.agent_planning_time
        self.degree_of_commitment = args.degree_of_commitment
        self.boldness = args.boldness
        self.reaction_strategy = args.reaction_strategy
        self.grid = Grid(args)
        self.hole_pic = self.grid.alive_holes
        self.target = None
        self.score = 0
        self.max_iter = args.max_iter
        self.history = []
        
        assert self.reaction_strategy in ['blind', 'disappear', 'new_hole', 'nearer_hole'], f'Invalid reaction strategy {self.reaction_strategy}'
    
    def run(self):
        for hole in self.grid.waiting_holes:
            print(f'hole: {hole.pos}, {hole.gestation}, {hole.lifetime}')
        for obstacle in self.grid.obstacles:
            print(f'obstacle: {obstacle.pos}')
        iter_num = 0
        while iter_num <= self.max_iter:
            # 1. if target is not set, randomly choose a hole
            # print(not self.target, not self.hole_pic)
            if not self.target and self.hole_pic:
                self.target = random.choice(self.hole_pic)
            # print(iter_num, self.pos, self.target.pos if self.target else None)
            
            # 2. find the optimal path to the target, move `boldness` steps
            if self.target:
                path = Dijkstra(self.grid, self.pos, self.target.pos).path
                if not path:
                    self.target = None
                    continue
                # print(path)
                # assert 0
                for i in range(min(self.boldness, len(path)-1)):
                    self._step(path[i+1])
                    self.grid.update()
                    iter_num += 1
                    print(iter_num, self.pos, self.target.pos if self.target else None)
                self.target = None
                print(self.score)
                continue
            else:
                self.grid.update()
                iter_num += 1        
        print(self.score)
            
    def _step(self, pos):
        self.pos = pos
        for hole in self.grid.alive_holes:
            if self.pos == hole.pos:
                self.score += 1
                self.grid.alive_holes.remove(hole)
        # if self.pos in self.grid.alive_holes:
        #     self.score += 1
            
        self.hole_pic = self.grid.alive_holes
        self.grid.update()
        self._save_history()
        
    def _save_history(self):
        pic = self.grid.grid.copy()
        pic[self.pos] = AGENT
        self.history.append(pic)
        
        
        
        
            
            
            
        
        
        
        




    
    
    
        
    
    
    
        
        