import argparse

def parse_args():
    parse = argparse.ArgumentParser()
    
    # game info
    parse.add_argument('--size', type=int, default=10, help='size of the board')
    parse.add_argument('--n_obstacle', type=int, default=10, help='number of obstacles')
    parse.add_argument('--n_hole', type=int, default=10, help='number of holes')
    parse.add_argument('--lifetime_range', type=tuple, default=(5, 10), help='range of lifetime of holes')
    parse.add_argument('--world_change_rate', type=float, default=0.1, help='world change rate')
    
    # agent info
    parse.add_argument('--agent_planning_time', type=float, default=0.1, help='agent planning time')
    parse.add_argument('--degree_of_commitment', type=float, default=0.1, help='degree of commitment')
    parse.add_argument('--reaction_strategy', type=str, default='random', help='reaction strategy')
    
if __name__ == '__main__':
    pass