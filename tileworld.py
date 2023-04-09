import random
import numpy as np
from enum import Enum
from dijkstra import Dijkstra
random.seed(0)
np.random.seed(0)

class OBJ(Enum):
    agent = 1
    obstacle = 2
    hole = 3
    

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
        self.obstacles = [self._set_obstacle(mode='random') for _ in range(self.n_obstacles)] if not args.obstacles else [self._set_obstacle(pos) for pos in args.obstacles]
        self.waiting_hole = [self._gen_hole(args.gest_range, args.lt_range) for _ in range(self.n_holes)]
        self.alive_hole = []
        self._set_hole()
        self.time = 0
    
    def _set_obstacle(self, pos=None, mode='random'):
        """
        Returns:
            Obstacle: an Obstacle object with a random position
        """
        assert pos is None or (isinstance(pos, tuple) and len(pos) == 2), f'Invalid position {pos}'
        assert mode in ['random', 'fixed'], f'Invalid mode {mode}'
        if mode == 'random':
            pos = (random.randint(0, self.size-1), random.randint(0, self.size-1))
            while self.grid[pos] != 0:
                pos = (random.randint(0, self.size-1), random.randint(0, self.size-1))
        elif mode == 'fixed':
            pass
        self.grid[pos] = OBJ.obstacle
        return Obstacle(pos)
    
    def _gen_hole(self, gest_range, lt_range):
        """Generate holes to appear in the grid in the game
        
        Args:
            gest_range (tuple): range of gestation of holes
            lt_range (tuple): range of lifetime of holes
            
        Returns:
            Hole: a Hole object with a random position, gestation and lifetime
        """
        pos = [random.randint(0, self.size-1), random.randint(0, self.size-1)]
        while self.grid[pos] != 0:
            pos = [random.randint(0, self.size-1), random.randint(0, self.size-1)]
        lifetime = random.randint(lt_range)
        gestation = random.randint(gest_range)
        return Hole(pos, gestation, lifetime)
    
    def _set_holes(self):
        for hole in self.waiting_hole:
            if hole not in self.alive_hole and hole.gestation <= self.time <= hole.gestation + hole.lifetime:
                self.grid[hole.pos] = OBJ.hole
                self.alive_hole.append(hole)
                self.waiting_hole.remove(hole)
        for hole in self.alive_hole:
            if self.time > hole.gestation + hole.lifetime:
                self.grid[hole.pos] = 0
                self.alive_hole.remove(hole)
    
    def update(self):
        self.time += 1
        self._set_holes()
    
class Agent:
    def __init__(self, args):
        self.pos = [args.grid_size//2, args.grid_size//2]
        self.gamma = args.gamma
        self.agent_planning_time = args.agent_planning_time
        self.degree_of_commitment = args.degree_of_commitment
        self.boldness = args.boldness
        self.reaction_strategy = args.reaction_strategy
        self.grid = Grid(args)
        self.hole_pic = self.Grid.holes
        self.target = None
        self.score = 0
        self.max_iter = args.max_iter
        self.history = []
        
        assert self.reaction_strategy in ['blind', 'disappear', 'new_hole', 'nearer_hole'], f'Invalid reaction strategy {self.reaction_strategy}'
    
    def run(self):
        iter_num = 0
        while iter_num <= self.max_iter:
            # 1. if target is not set, randomly choose a hole
            if not self.target:
                self.target = random.choice(self.hole_pic)
                
            # 2. find the optimal path to the target, move `boldness` steps
            path = Dijkstra(self.agent, self.target).path
            
            for i in range(self.boldness):
                self._step(path[i+1])
                self.grid.update()
                iter_num += 1
        print(self.score)
            
    def _step(self, pos):
        self.pos = pos
        if self.pos in self.grid.alive_hole:
            self.score += 1
        self.grid.update()
        self._save_history()
        
    def _save_history(self):
        pic = self.grid.grid.copy()
        pic[self.pos] = OBJ.agent
        self.history.append(pic)
        
        
        
        
            
            
            
        
        
        
        




    
    
    
        
    
    
    
        
        