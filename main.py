import math
import argparse
from tileworld import Agent

def parse_args():
    parse = argparse.ArgumentParser()
    
    # game info
    parse.add_argument('--grid_size', type=int, default=15, help='size of the tile world grid')
    parse.add_argument('--obstacles', type=list, default=None, help='list of obstacles position')
    parse.add_argument('--n_obstacle', type=int, default=10, help='number of obstacles')
    parse.add_argument('--n_hole', type=int, default=20, help='number of holes')
    parse.add_argument('--gamma', type=float, default=1, help='world change rate')
    parse.add_argument('--score_range', type=tuple, default=(1, 5), help='range of score of holes')
    parse.add_argument('--gest_range', type=tuple, default=(60, 240), help='range of gestation of holes')
    parse.add_argument('--lt_range', type=tuple, default=(240, 960), help='range of lifetime of holes')
    parse.add_argument('--boldness', type=float, default=math.inf, help='boldness of agent')
    parse.add_argument('--planning_time', type=float, default=4, help='agent planning time')
    parse.add_argument('--unit_time', type=float, default=1, help='time to move one step for the agent')
    parse.add_argument('--reaction_strategy', type=str, default='blind', help='reaction strategy')
    parse.add_argument('--max_time', type=int, default=1000, help='maximum number of iterations')
    return parse.parse_args()
    
def modify_args(args):
    args.gest_range = (int(args.gest_range[0]/args.gamma), int(args.gest_range[1]/args.gamma))
    args.lt_range = (int(args.lt_range[0]/args.gamma), int(args.lt_range[1]/args.gamma))
    return args
   
if __name__ == '__main__':
    args = parse_args()
    args = modify_args(args)
    agent = Agent(args)
    agent.run()
    