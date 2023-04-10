import math
import numpy as np

class Dijkstra:
    def __init__(self, grid, pos1, pos2):
        init_pos = pos1
        goal_pos = pos2
        self.grid = grid
        self.grid_size = grid.size
        self.obstacles = grid.obstacles
        self.cost = np.ones([self.grid_size, self.grid_size])
        for obstacle in self.obstacles:
            self.cost[obstacle.pos] = math.inf
        
        self.distances = np.ones([self.grid_size, self.grid_size]) * math.inf
        self.distances[init_pos] = 0
        
        self.visited = np.zeros([self.grid_size, self.grid_size], bool)
        self.path = self._dijkstra(init_pos, goal_pos)
        
    def _up(self, pos):
        return (pos[0]-1, pos[1])
    
    def _down(self, pos):
        return (pos[0]+1, pos[1])
    
    def _left(self, pos):
        return (pos[0], pos[1]-1)
    
    def _right(self, pos):
        return (pos[0], pos[1]+1)
    
    def _is_valid(self, pos):
        return pos[0] >= 0 and pos[0] < self.grid_size and pos[1] >= 0 and pos[1] < self.grid_size
    
    def _backtrack(self, init_pos, goal_pos):
        """Backtrack procedure for Dijkstra's algorithm.

        Args:
            init_pos (tuple: (x, y)): initial position
            goal_pos (tuple: (x, y)): goal position

        Returns:
            list: path from the initial position to the goal position
        """
        # print(self.cost)
        # print(self.distances)
        path = [goal_pos]
        cur_pos = goal_pos
        visited = []
        while cur_pos != init_pos:
            visited.append(cur_pos)
            last_pos = [direction(cur_pos) for direction in [self._up, self._down, self._left, self._right] if self._is_valid(direction(cur_pos))]
            min_distance = math.inf
            min_pos = None
            for pos in last_pos:
                if pos not in visited:
                    if self.distances[pos] <= min_distance:
                        min_distance = self.distances[pos]
                        min_pos = pos
            # print(cur_pos, min_distance)
            cur_pos = min_pos
            # cur_pos = [pos for pos in last_pos if self.cost[pos] == min([self.cost[pos] and pos not in visited])][0]
            path.append(cur_pos)
            # print(f'path {path}')
            # assert 0
        # print(path)
        return list(reversed(path))
        
    def _dijkstra(self, init_pos, goal_pos):
        """Dijsktra's algorithm to find the shortest path avoiding obstacles.

        Args:
            grid_size (int): size of grid
            obstacles (tuple: (x, y)): a list of positions of obstacles 
            init_pos (tuple: (x, y)): initial position
            goal_pos (tuple: (x, y)): goal position

        Returns:
            list[list]: a list of shortest paths from the initial position to the goal position
        """
        
        cur_pos = init_pos
        while cur_pos != goal_pos:
            for direction in [self._up, self._down, self._left, self._right]:
                next_pos = direction(cur_pos)
                if self._is_valid(next_pos) and not self.visited[next_pos]:
                    self.distances[next_pos] = min(self.distances[next_pos], self.distances[cur_pos] + self.cost[next_pos])
            self.visited[cur_pos] = True
        
            min_pos = None
            min_dist = math.inf
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    if not self.visited[i][j]:
                        if self.distances[i][j] <= min_dist:
                            min_pos = (i, j)
                            min_dist = self.distances[i][j]
            cur_pos = min_pos
            # cur_pos = np.unravel_index(distances.argmin(), distances.shape)
            # print(init_pos, cur_pos, goal_pos)
        # print('done')
        return self._backtrack(init_pos, goal_pos)
        
        
# import numpy as np
# def valid_node(node, size_of_grid):
#     """Checks if node is within the grid boundaries."""
#     if node[0] < 0 or node[0] >= size_of_grid:
#         return False
#     if node[1] < 0 or node[1] >= size_of_grid:
#         return False
#     return True

# def up(node):
#     return (node[0]-1,node[1])

# def down(node):
#     return (node[0]+1,node[1])

# def left(node):
#     return (node[0],node[1]-1)

# def right(node):
#     return (node[0],node[1]+1)

# def backtrack(initial_node, desired_node, distances):
#     # idea start at the last node then choose the least number of steps to go back
#     # last node
#     path = [desired_node]

#     size_of_grid = distances.shape[0]

#     while True:
#         # check up down left right - choose the direction that has the least distance
#         potential_distances = []
#         potential_nodes = []

#         directions = [up,down,left,right]

#         for direction in directions:
#             node = direction(path[-1])
#             if valid_node(node, size_of_grid):
#                 potential_nodes.append(node)
#                 potential_distances.append(distances[node[0],node[1]])

#         least_distance_index = np.argmin(potential_distances)
#         path.append(potential_nodes[least_distance_index])

#         if path[-1][0] == initial_node[0] and path[-1][1] == initial_node[1]:
#             break

#     return list(reversed(path))

# def dijkstra(initial_node, desired_node, obstacles):
    # """Dijkstras algorithm for finding the shortest path between two nodes in a graph.

    # Args:
    #     initial_node (list): [row,col] coordinates of the initial node
    #     desired_node (list): [row,col] coordinates of the desired node
    #     obstacles (array 2d): 2d numpy array that contains any obstacles as 1s and free space as 0s

    # Returns:
    #     list[list]: list of list of nodes that form the shortest path
    # """
    # # initialize cost heuristic map
    # obstacles = obstacles.copy()
    # # obstacles should have very high cost, so we avoid them.
    # obstacles *= 1000
    # # normal tiles should have 1 cost (1 so we can backtrack)
    # obstacles += np.ones(obstacles.shape)
    # # source and destination are free
    # obstacles[initial_node[0],initial_node[1]] = 0
    # obstacles[desired_node[0],desired_node[1]] = 0


    # # initialize maps for distances and visited nodes
    # size_of_floor = obstacles.shape[0]

    # # we only want to visit nodes once
    # visited = np.zeros([size_of_floor,size_of_floor],bool)

    # # initiate matrix to keep track of distance to source node
    # # initial distance to nodes is infinity so we always get a lower actual distance
    # distances = np.ones([size_of_floor,size_of_floor]) * np.inf
    # # initial node has a distance of 0 to itself
    # distances[initial_node[0],initial_node[1]] = 0

    # # start algorithm
    # current_node = [initial_node[0], initial_node[1]]
    # while True:
    #     directions = [up, down, left, right]
    #     for direction in directions:
    #         potential_node = direction(current_node)
    #         if valid_node(potential_node, size_of_floor): # boundary checking
    #             if not visited[potential_node[0],potential_node[1]]: # check if we have visited this node before
    #                 # update distance to node
    #                 distance = distances[current_node[0], current_node[1]] + obstacles[potential_node[0],potential_node[1]]

    #                 # update distance if it is the shortest discovered
    #                 if distance < distances[potential_node[0],potential_node[1]]:
    #                     distances[potential_node[0],potential_node[1]] = distance


    #     # mark current node as visited
    #     visited[current_node[0]  ,current_node[1]] = True

    #     # select next node
    #     # by choosing the the shortest path so far
    #     t=distances.copy()
    #     # we don't want to visit nodes that have already been visited
    #     t[np.where(visited)]=np.inf
    #     # choose the shortest path
    #     node_index = np.argmin(t)

    #     # convert index to row,col.
    #     node_row = node_index//size_of_floor
    #     node_col = node_index%size_of_floor
    #     # update current node.
    #     current_node = (node_row, node_col)

    #     # stop if we have reached the desired node
    #     if current_node[0] == desired_node[0] and current_node[1]==desired_node[1]:
    #         break

    # # backtrack to construct path
    # return backtrack(initial_node,desired_node,distances)