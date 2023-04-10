import math
from main import parse_args, modify_args
from tileworld import Agent
import matplotlib.pyplot as plt

class AgentTest:
    def __init__(self):
        pass
    
    def test12(self):
        """Reproduce the result of Figure 1 and Figure 2 in the paper
        """
        epsilon_list = []
        gamma_list =  [1, 2, 3, 4, 6, 10, 12, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
        for gamma in gamma_list:
            args = parse_args()
            args.gamma = gamma
            args = modify_args(args)
            agent = Agent(args)
            agent_score, total_score = agent.run()
            print(f'test12, gamma = {gamma}, agent_score = {agent_score}, total_score = {total_score}, epsilon = {agent_score / total_score}')
            epsilon_list.append(agent_score / total_score)
        plt.figure(1)
        plt.plot(gamma_list, epsilon_list)
        plt.savefig('fig/fig1.png')
        
        log10gamma_list = [math.log10(gamma) for gamma in gamma_list]
        plt.figure(2)
        plt.plot(log10gamma_list, epsilon_list)
        plt.savefig('fig/fig2.png')
        
    def test3(self):
        """Reproduce the result of Figure 3 in the paper (effect of planning time, bold agent)
        """
        epsilon_lists = []
        gamma_list =  [1, 2, 3, 4, 6, 10, 12, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
        for planning_time in [0.5, 1, 2, 4]:
            epsilon_list = []
            for gamma in gamma_list:
                args = parse_args()
                args.boldness = math.inf
                args.gamma = gamma
                args.planning_time = planning_time
                args = modify_args(args)
                agent = Agent(args)
                agent_score, total_score = agent.run()
                print(f'test3, planning time = {planning_time}, gamma = {gamma}, agent_score = {agent_score}, total_score = {total_score}, epsilon = {agent_score / total_score}')
                epsilon_list.append(agent_score / total_score)
            epsilon_lists.append(epsilon_list)
        
        log10gamma_list = [math.log10(gamma) for gamma in gamma_list]
        plt.figure(3)
        for epsilon_list in epsilon_lists:
            plt.plot(log10gamma_list, epsilon_list)
        plt.savefig('fig/fig3.png')
        
    def test4(self):
        """Reproduce the result of Figure 3 in the paper (effect of planning time, bold agent)
        """
        epsilon_lists = []
        gamma_list =  [1, 2, 3, 4, 6, 10, 12, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
        for planning_time in [0.5, 1, 2, 4]:
            epsilon_list = []
            for gamma in gamma_list:
                args = parse_args()
                args.boldness = 1
                args.gamma = gamma
                args.planning_time = planning_time
                args = modify_args(args)
                agent = Agent(args)
                agent_score, total_score = agent.run()
                print(f'test4, planning time = {planning_time}, gamma = {gamma}, agent_score = {agent_score}, total_score = {total_score}, epsilon = {agent_score / total_score}')
                epsilon_list.append(agent_score / total_score)
            epsilon_lists.append(epsilon_list)
        
        log10gamma_list = [math.log10(gamma) for gamma in gamma_list]
        plt.figure(4)
        for epsilon_list in epsilon_lists:
            plt.plot(log10gamma_list, epsilon_list)
        plt.savefig('fig/fig4.png')


            
        
        
        
if __name__ == '__main__':
    test = AgentTest()
    test.test12()
    test.test3()
    test.test4()
