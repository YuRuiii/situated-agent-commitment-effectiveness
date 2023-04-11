import math
import copy
import random
import numpy as np
from enum import Enum
from dijkstra import Dijkstra

AGENT = 1
OBSTACLE = 2
HOLE = 3

class Hole:
    def __init__(self, pos, score, start_time, end_time):
        self.pos = pos
        self.score = score
        self.start_time = start_time
        self.end_time = end_time
        
class Obstacle:
    def __init__(self, pos):
        self.pos = pos

class Grid:
    def __init__(self, args):
        self.size = args.grid_size
        self.grid = np.zeros([self.size, self.size], int)
        self.max_time = args.max_time
        self.obstacles = [self._set_obstacle(mode='random') for _ in range(args.n_obstacle)] if not args.obstacles else [self._set_obstacle(pos) for pos in args.obstacles]
        self.waiting_holes = self._gen_holes(args.score_range, args.gest_range, args.lt_range)
        self.max_time = max([hole.end_time for hole in self.waiting_holes])
        # print(args.max_time, self.max_time)
        # for hole in self.waiting_holes:
        #     print(f'hole: {hole.pos}, {hole.start_time}, {hole.end_time}')
        # assert 0
        self.n_holes = len(self.waiting_holes)
        self.total_scores = sum([hole.score for hole in self.waiting_holes])
        self.alive_holes = []
        self.dead_holes = []
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
    
    def _gen_holes(self, score_range, gest_range, lt_range):
        """Generate holes to appear in the grid in the game
        
        Args:
            score_range (tuple): range of score of holes
            gest_range (tuple): range of gestation of holes
            lt_range (tuple): range of lifetime of holes
            
        Returns:
            Hole: a Hole object with a random position, gestation and lifetime
        """
        time = 0
        holes = []
        while time < self.max_time:
            hole = self._gen_hole(score_range, gest_range, lt_range, time)
            time = hole.start_time
            holes.append(hole)
        return holes
            
    def _gen_hole(self, score_range, gest_range, lt_range, time):
        pos = (random.randint(0, self.size-1), random.randint(0, self.size-1))
        # print(f'self.grid[{pos}] is {self.grid[pos]}')
        while self.grid[pos] != 0 :
            pos = (random.randint(0, self.size-1), random.randint(0, self.size-1))
        score = random.randint(score_range[0], score_range[1])
        lifetime = random.randint(lt_range[0], lt_range[1])
        gestation = random.randint(gest_range[0], gest_range[1])
        return Hole(pos, score, time + gestation, time + gestation + lifetime)
    
    def _set_holes(self):
        """Set alive and waiting holes in the grid according to the current time
        """
        for hole in self.dead_holes:
            self.grid[hole.pos] = 0
        self.dead_holes.clear()
        for hole in self.waiting_holes:
            if hole not in self.alive_holes and hole.start_time <= self.time <= hole.end_time:
                self.grid[hole.pos] = HOLE
                self.alive_holes.append(hole)
                self.waiting_holes.remove(hole)
        for hole in self.alive_holes:
            if self.time > hole.end_time:
                self.grid[hole.pos] = 0
                self.alive_holes.remove(hole)
    
    def update(self, step_time):
        """Update the grid of each step

        Args:
            step_time (float): step time for the agent
        """
        self.time += step_time
        self._set_holes()
    
class Agent:
    def __init__(self, args):
        random.seed(args.seed)
        np.random.seed(args.seed)
        self.pos = (args.grid_size//2, args.grid_size//2)
        self.gamma = args.gamma
        self.planning_time = args.planning_time
        self.unit_time = args.unit_time
        self.boldness = args.boldness
        self.step_time = self.planning_time/self.boldness + self.unit_time
        self.reaction_strategy = args.reaction_strategy
        self.grid = Grid(args)
        self.hole_pic = self.grid.alive_holes
        self.target = None
        self.score = 0
        self.max_time = self.grid.max_time
        self.history = []
        
        assert self.reaction_strategy in ['blind', 'disappear', 'new_holes', 'nearer_holes'], f'Invalid reaction strategy {self.reaction_strategy}'
    
    def run(self):
        # for hole in self.grid.waiting_holes:
        #     print(f'hole: {hole.pos}, {hole.start_time}, {hole.end_time}')
        # for obstacle in self.grid.obstacles:
        #     print(f'obstacle: {obstacle.pos}')
        while self.grid.time <= self.max_time:
            # 1. if target is not set, randomly choose a hole
            # print(not self.target, not self.hole_pic)
            self.target = self._utility_func() if not self.target else self.target
            # print(iter_num, self.pos, self.target.pos if self.target else None)
            
            # 2. find the optimal path to the target, move 'boldness' steps
            if self.target:
                path = Dijkstra(self.grid, self.pos, self.target.pos).path
                if not path:
                    self.target = None
                    continue
                self._step(path[0])
                self.hole_pic = [hole for hole in self.grid.alive_holes]
                for i in range(1, min(self.boldness+1, len(path))):
                    self._step(path[i])
                    self.grid.update(self.step_time)
                    # print(iter_num, self.pos, self.target.pos if self.target else None)
                    if not self.target:
                        break
                # print(self.score)
                continue
            else:
                self.grid.update(self.step_time)      
        # print(self.score)
        np.save('history.npy', np.array(self.history))
        return self.score, self.grid.total_scores
    
    def _reaction_strategy(self):
        def _disappear():
            """Whether the target has disappeared
            """
            return self.target not in self.grid.alive_holes
        
        def _new_hole_appear():
            """Whether any hole appears
            """
            print(self.grid.time)
            for hole in self.grid.alive_holes:
                print(hole.pos, end=' ')
            print('')
            for hole in self.hole_pic:
                print(hole.pos, end=' ')
            print('----------------')
            if self.grid.alive_holes != self.hole_pic:
                print(len(self.grid.alive_holes), len(self.hole_pic))
                return True
            return False
        
        def _nearer_hole_appear():
            """Whether any nearer hole appears
            """
            for hole in self.grid.alive_holes:
                if self._manhanttan_dist(hole) < self._manhanttan_dist(self.target):
                    return True
            return False
        
        # print(_disappear(), _new_hole_appear(), _nearer_hole_appear())
            
        if not self.target or self.target.pos == self.pos:
            return None
            
        if self.reaction_strategy == 'blind':
            pass
        
        elif self.reaction_strategy == 'disappear':
            if _disappear():
                # print(1)
                return None
        
        elif self.reaction_strategy == 'new_holes':
            if _disappear() or _new_hole_appear():
                # print(self.grid.time, 2, _disappear(), _new_hole_appear())
                return None
        
        elif self.reaction_strategy == 'nearer_holes':
            if _disappear() or _nearer_hole_appear():
                # print(3)
                return None
        
        return self.target
    
        
    def _utility_func(self, dist_weight=-10, age_weight=1):
        """Utility function for plan selection, i.e., which target to choose

        Args:
            dist_weight (int, optional): Weight of distance score. Defaults to 1.
            age_weight (int, optional): Age of distance score. Defaults to 1.

        Returns:
            max_target (Hole): The target with the highest score in all alive holes
        """
        if not self.grid.alive_holes:
            return None
        
        max_score = -math.inf
        max_target = None
        for hole in self.grid.alive_holes:
            dist_score = self._manhanttan_dist(hole)
            age_score = self._age(hole)
            score = (dist_score * dist_weight + age_score * age_weight) * hole.score
            if score > max_score:
                max_score = score
                max_target = hole
                
        return max_target
    
    def _manhanttan_dist(self, hole):
        """Calculate the distance score (Manhanttan) of a hole
        
        Args:
            hole (Hole): a Hole object
        
        Returns:
            int: the distance score of the hole
        """
        return abs(self.pos[0] - hole.pos[0]) + abs(self.pos[1] - hole.pos[1])
    
    def _age(self, hole):
        """Calculate the age score of a hole

        Args:
            hole (Hole): a Hole object
            
        Returns:
            int: the age score of the hole
        """
        assert self.grid.time >= hole.start_time, f'grid time {self.grid.time} is earlier than hole start time {hole.start_time}'
        return self.grid.time - hole.start_time
                
            
    def _step(self, pos):
        """Move one step to the given position

        Args:
            pos (tuple): the position to move to
        """
        self.pos = pos
        for hole in self.grid.alive_holes:
            if self.pos == hole.pos:
                self.score += hole.score
                self.grid.dead_holes.append(hole)
                self.grid.alive_holes.remove(hole)
        # if self.pos in self.grid.alive_holes:
        #     self.score += 1
            
        self.hole_pic = self.grid.alive_holes
        self.target = self._reaction_strategy()
        self._save_history()
        
    def _save_history(self):
        pic = self.grid.grid.copy()
        pic[self.pos] = AGENT
        self.history.append(pic)
        
        
        
        
            
            
            
        
        
        
        




    
    
    
        
    
    
    
        
        