import random

class Hole:
    def __init__(self, pos, lifetime):
        self.pos = pos
        self.lifetime = lifetime
        
class Obstacle:
    def __init__(self, pos):
        self.pos = pos

class Board:
    def __init__(self, size, n_obstacles, n_holes, lt_range):
        self.agent_color = 1
        self.obstacle_color = 2
        self.hole_color = 3
        random.seed(0)
        
        self.size = size
        self.board = [[0 for i in range(size)] for j in range(size)]
        self.obstacles = [self._set_obstacles() for _ in range(n_obstacles)]
        self.holes = [self._set_holes(self.lt_range) for _ in range(n_holes)]
    
    def _set_obstacles(self):
        """
        Returns:
            Obstacle: an Obstacle object with a random position
        """
        pos = [random.randint(0, self.size-1), random.randint(0, self.size-1)]
        while self.board[pos[0]][pos[1]] != 0:
            pos = [random.randint(0, self.size-1), random.randint(0, self.size-1)]
        self.board[pos[0]][pos[1]] = self.obstacle_color
        return Obstacle(pos)
    
    def _set_holes(self, lt_range):
        """
        Args:
            lt_range (tuple, optional): range of lifetime of holes. Defaults to (5, 10).

        Returns:
            _type_: _description_
        """
        pos = [random.randint(0, self.size-1), random.randint(0, self.size-1)]
        while self.board[pos[0]][pos[1]] != 0:
            pos = [random.randint(0, self.size-1), random.randint(0, self.size-1)]
        self.board[pos[0]][pos[1]] = self.hole_color
        lifetime = random.randint(lt_range)
        return Hole(pos, lifetime)
    
    
    
class Agent:
    def __init__(self, args):
        self.pos = [0, 0]
        self.world_change_rate = args.world_change_rate
        self.agent_planning_time = args.agent_planning_time
        self.degree_of_commitment = args.degree_of_commitment
        self.reaction_strategy = args.reaction_strategy
        self.board = Board(args.size, args.n_obstacle, args.n_holes, args.lifetime_range)
        self.hole_pic = self.board.holes
        self.target = None
        
        assert self.reaction_strategy in ['blind', 'disappear', 'new_hole', 'nearer_hole'], 'Invalid reaction strategy'
    
    def get_action(self):
        
        
        
        




    
    
    
        
    
    
    
        
        