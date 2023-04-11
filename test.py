import os
import math
import numpy as np
from main import parse_args, modify_args
from tileworld import Agent
from statistics import mean
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rc, rcParams

seed_list = range(10)
gamma_list = [1, 2, 3, 4, 6, 10, 12, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 80, 100]
planning_time_list = [0.5, 1, 2, 4]
boldness_list = [1, 4, 30]
reaction_strategy_list = ['blind', 'disappear', 'new_holes', 'nearer_holes']

RED = '#B22C33'
YELLOW = '#E67125'
GREEN = '#00804B'
BLUE = '#2A4D80'
color_list = [BLUE, RED, GREEN, YELLOW]
marker_list = ['o', 's', 'v', '*']

class AgentTest:
    def __init__(self):
        self.just_plot = False
    
    def test12(self):
        """Reproduce the result of Figure 1 and Figure 2 in the paper (effect of world change rate)
        """
        if self.just_plot and os.path.exists('res/fig12.npy'):
            epsilon_list = np.load('res/fig12.npy')
        else:
            epsilon_list = []
            for gamma in gamma_list:
                epsilon = self._gen_epsilon(task_id=12,
                                            seed=0,
                                            gamma=gamma,
                                            planning_time=1,
                                            boldness=30,
                                            reaction_strategy='blind')
                epsilon_list.append(epsilon)
            np.save('res/fig12.npy', epsilon_list)
        plt.figure(1)
        plt.title('Figure 1: Effect of Rate of World Change')
        plt.xlabel(r'$\gamma$')
        plt.xlim(0, 100)
        plt.ylabel(r'$\epsilon$')
        plt.plot(gamma_list, epsilon_list, linestyle='-',  marker='o', markersize=4, color=BLUE)
        plt.savefig('fig/fig1.png')
        
        log10gamma_list = [math.log10(gamma) for gamma in gamma_list]
        plt.figure(2)
        plt.title('Figure 2: Effect of Rate of World Change (log x-scale)')
        plt.xlabel(r'$\log_{10}\gamma$')
        plt.xlim(0.4, 2)
        plt.ylabel(r'$\epsilon$')
        plt.plot(log10gamma_list, epsilon_list, linestyle='-',  marker='o', markersize=4, color=BLUE)
        plt.savefig('fig/fig2.png')
        
    def test3(self):
        """Reproduce the result of Figure 3 in the paper (effect of planning time, bold agent)
        """
        if self.just_plot and os.path.exists('res/fig3.npy'):
            epsilon_lists = np.load('res/fig3.npy')
        else:
            epsilon_lists = []
            for planning_time in planning_time_list:
                epsilon_list = []
                for gamma in gamma_list:
                    epsilon = self._gen_epsilon(task_id=3,
                                                seed=0,
                                                gamma=gamma,
                                                planning_time=planning_time,
                                                boldness=30,
                                                reaction_strategy='blind')
                    epsilon_list.append(epsilon)
                epsilon_lists.append(epsilon_list)
            np.save('res/fig3.npy', epsilon_lists)
        
        log10gamma_list = [math.log10(gamma) for gamma in gamma_list]
        
        plt.figure(3)
        plt.title('Figure 3: Effect of Planning Time (bold agent)')
        plt.xlabel(r'$\log_{10}\gamma$')
        plt.xlim(0.4, 2)
        plt.ylabel(r'$\epsilon$')
        for i, (epsilon_list, planning_time) in enumerate(zip(epsilon_lists, planning_time_list)):
            plt.plot(log10gamma_list, epsilon_list, linestyle='-',  marker=marker_list[i], markersize=4, color=color_list[i] ,label=f'p = {planning_time}')
        plt.legend()
        plt.savefig('fig/fig3.png')
        
    def test4(self):
        """Reproduce the result of Figure 4 in the paper (effect of planning time, cautious agent)
        """
        if self.just_plot and os.path.exists('res/fig4.npy'):
            epsilon_lists = np.load('res/fig4.npy')
        else:
            epsilon_lists = []
            for planning_time in planning_time_list:
                epsilon_list = []
                for gamma in gamma_list:
                    epsilon = self._gen_epsilon(task_id=4,
                                                seed=0,
                                                gamma=gamma,
                                                planning_time=planning_time,
                                                boldness=1,
                                                reaction_strategy='blind')
                    epsilon_list.append(epsilon)
                epsilon_lists.append(epsilon_list)
            np.save('res/fig4.npy', epsilon_lists)
        
        log10gamma_list = [math.log10(gamma) for gamma in gamma_list]
        plt.figure(4)
        plt.title('Figure 4: Effect of Planning Time (cautious agent)')
        plt.xlabel(r'$\log_{10}\gamma$')
        plt.xlim(0.4, 2)
        plt.ylabel(r'$\epsilon$')
        for i, (epsilon_list, planning_time) in enumerate(zip(epsilon_lists, planning_time_list)):
            plt.plot(log10gamma_list, epsilon_list, linestyle='-',  marker=marker_list[i], markersize=4, color=color_list[i] ,label=f'p = {planning_time}')
        plt.legend()
        plt.savefig('fig/fig4.png')

    def test5(self):
        """Reproduce the result of Figure 5 in the paper (effect of degree of boldness, p = 4)
        """
        if self.just_plot and os.path.exists('res/fig5.npy'):
            epsilon_lists = np.load('res/fig5.npy')
        else:
            epsilon_lists = []
            for boldness in boldness_list:
                epsilon_list = []
                for gamma in gamma_list:
                    epsilon = self._gen_epsilon(task_id=5,
                                                seed=0,
                                                gamma=gamma,
                                                planning_time=4,
                                                boldness=boldness,
                                                reaction_strategy='blind')
                    epsilon_list.append(epsilon)
                epsilon_lists.append(epsilon_list)
            np.save('res/fig5.npy', epsilon_lists)
        
        log10gamma_list = [math.log10(gamma) for gamma in gamma_list]
        plt.figure(5)
        plt.title(r'Figure 5: Effect of Degree of Boldness ($p = 4$)')
        plt.xlabel(r'$\log_{10}\gamma$')
        plt.xlim(0.4, 2)
        plt.ylabel(r'$\epsilon$')
        label = ['cautious', 'normal', 'bold']
        for i, epsilon_list in enumerate(epsilon_lists):
            plt.plot(log10gamma_list, epsilon_list, linestyle='-',  marker=marker_list[i], markersize=4, color=color_list[i], label=label[i])
        plt.legend()
        plt.savefig('fig/fig5.png')
    
    def test6(self):
        """Reproduce the result of Figure 6 in the paper (effect of degree of boldness, p = 2)
        """
        if self.just_plot and os.path.exists('res/fig6.npy'):
            epsilon_lists = np.load('res/fig6.npy')
        else:
            epsilon_lists = []
            for boldness in boldness_list:
                epsilon_list = []
                for gamma in gamma_list:
                    epsilon = self._gen_epsilon(task_id=6,
                                                seed=0,
                                                gamma=gamma,
                                                planning_time=2,
                                                boldness=boldness,
                                                reaction_strategy='blind')
                    epsilon_list.append(epsilon)
                epsilon_lists.append(epsilon_list)
            np.save('res/fig6.npy', epsilon_lists)
        
        log10gamma_list = [math.log10(gamma) for gamma in gamma_list]
        plt.figure(6)
        plt.title(r'Figure 6: Effect of Degree of Boldness ($p = 2$)')
        plt.xlabel(r'$\log_{10}\gamma$')
        plt.xlim(0.4, 2)
        plt.ylabel(r'$\epsilon$')
        label = ['cautious', 'normal', 'bold']
        for i, epsilon_list in enumerate(epsilon_lists):
            plt.plot(log10gamma_list, epsilon_list, linestyle='-',  marker=marker_list[i], markersize=4, color=color_list[i], label=label[i])
        plt.legend()
        plt.savefig('fig/fig6.png')
        
    def test7(self):
        """Reproduce the result of Figure 7 in the paper (effect of degree of boldness, p = 1)
        """
        if self.just_plot and os.path.exists('res/fig7.npy'):
            epsilon_lists = np.load('res/fig7.npy')
        else:
            epsilon_lists = []
            for boldness in boldness_list:
                epsilon_list = []
                for gamma in gamma_list:
                    epsilon = self._gen_epsilon(task_id=7,
                                                seed=0,
                                                gamma=gamma,
                                                planning_time=1,
                                                boldness=boldness,
                                                reaction_strategy='blind')
                    epsilon_list.append(epsilon)
                epsilon_lists.append(epsilon_list)
        np.save('res/fig7.npy', epsilon_lists)
        
        log10gamma_list = [math.log10(gamma) for gamma in gamma_list]
        plt.figure(7)
        plt.title(r'Figure 7: Effect of Degree of Boldness ($p = 1$)')
        plt.xlabel(r'$\log_{10}\gamma$')
        plt.xlim(0.4, 2)
        plt.ylabel(r'$\epsilon$')
        label = ['cautious', 'normal', 'bold']
        for i, epsilon_list in enumerate(epsilon_lists):
            plt.plot(log10gamma_list, epsilon_list, linestyle='-',  marker=marker_list[i], markersize=4, color=color_list[i], label=label[i])
        plt.legend()
        plt.savefig('fig/fig7.png')
        
    def test8(self):
        """Reproduce the result of Figure 8 in the paper (effect of reaction strategy, p = 2)
        """
        if self.just_plot and os.path.exists('res/fig8.npy'):
            epsilon_lists = np.load('res/fig8.npy')
        else:
            epsilon_lists = []
            for reaction_strategy in reaction_strategy_list:
                epsilon_list = []
                for gamma in gamma_list:
                    epsilon = self._gen_epsilon(task_id=8,
                                                seed=0,
                                                gamma=gamma,
                                                planning_time=2,
                                                boldness=30,
                                                reaction_strategy=reaction_strategy)
                    epsilon_list.append(epsilon)
                epsilon_lists.append(epsilon_list)
            np.save('res/fig8.npy', epsilon_lists)
        
        log10gamma_list = [math.log10(gamma) for gamma in gamma_list]
        plt.figure(8)
        plt.title(r'Figure 8: Effect of Reaction Strategy ($p = 2$)')
        plt.xlabel(r'$\log_{10}\gamma$')
        plt.xlim(0.4, 2)
        plt.ylabel(r'$\epsilon$')
        label = ['blind commitment', 'notices target disappearance', 'target dis. or any new hole', 'target dis. or nearer hole']
        for i, epsilon_list in enumerate(epsilon_lists):
            plt.plot(log10gamma_list, epsilon_list, linestyle='-',  marker=marker_list[i], markersize=4, color=color_list[i], label=label[i])
        plt.legend()
        plt.savefig('fig/fig8.png')
        
    def test9(self):
        """Reproduce the result of Figure 9 in the paper (effect of reaction strategy, p = 1)
        """
        if self.just_plot and os.path.exists('res/fig9.npy'):
            epsilon_lists = np.load('res/fig9.npy')
        else:
            epsilon_lists = []
            for reaction_strategy in reaction_strategy_list:
                epsilon_list = []
                for gamma in gamma_list:
                    epsilon = self._gen_epsilon(task_id=9,
                                                seed=0,
                                                gamma=gamma,
                                                planning_time=1,
                                                boldness=30,
                                                reaction_strategy=reaction_strategy)
                    epsilon_list.append(epsilon)
                epsilon_lists.append(epsilon_list)
            np.save('res/fig9.npy', epsilon_lists)
        
        log10gamma_list = [math.log10(gamma) for gamma in gamma_list]
        plt.figure(9)
        plt.title(r'Figure 9: Effect of Reaction Strategy ($p = 1$)')
        plt.xlabel(r'$\log_{10}\gamma$')
        plt.xlim(0.4, 2)
        plt.ylabel(r'$\epsilon$')
        label = ['blind commitment', 'notices target disappearance', 'target dis. or any new hole', 'target dis. or nearer hole']
        for i, epsilon_list in enumerate(epsilon_lists):
            plt.plot(log10gamma_list, epsilon_list, linestyle='-',  marker=marker_list[i], markersize=4, color=color_list[i], label=label[i])
        plt.legend()
        plt.savefig('fig/fig9.png')
        
    def test10(self):
        """Reproduce the result of Figure 10 in the paper (effect of degree of boldness, reactive agent, p = 1)
        """
        if self.just_plot and os.path.exists('res/fig10.npy'):
            epsilon_lists = np.load('res/fig10.npy')
        else:
            epsilon_lists = []
            for boldness in boldness_list:
                epsilon_list = []
                for gamma in gamma_list:
                    epsilon = self._gen_epsilon(task_id=10,
                                                seed=0,
                                                gamma=gamma,
                                                planning_time=1,
                                                boldness=boldness,
                                                reaction_strategy='disappear')
                    epsilon_list.append(epsilon)
                epsilon_lists.append(epsilon_list)
            np.save('res/fig10.npy', epsilon_lists)
        
        log10gamma_list = [math.log10(gamma) for gamma in gamma_list]
        plt.figure(10)
        plt.title(r'Figure 10: Effect of Degree of Boldness (reactive agent, $p = 1$)')
        plt.xlabel(r'$\log_{10}\gamma$')
        plt.xlim(0.4, 2)
        plt.ylabel(r'$\epsilon$')
        label = ['cautious', 'normal', 'bold']
        for i, epsilon_list in enumerate(epsilon_lists):
            plt.plot(log10gamma_list, epsilon_list, linestyle='-',  marker=marker_list[i], markersize=4, color=color_list[i], label=label[i])
        plt.legend()
        plt.savefig('fig/fig10.png')
        
    
        
    def _gen_epsilon(self, task_id, seed, gamma, planning_time, boldness, reaction_strategy, print_res=True):
        epsilons = []
        for seed in seed_list:
            args = parse_args()
            args.seed = seed
            args.gamma = gamma
            args.planning_time = planning_time
            args.boldness = boldness
            args.reaction_strategy = reaction_strategy
            args = modify_args(args)
            agent = Agent(args)
            agent_score, total_score = agent.run()
            epsilon = agent_score / total_score
            epsilons.append(epsilon)
        epsilon = mean(epsilons)
        if print_res:
            print(f'task{task_id}, seed = {seed}, gamma = {gamma}, pt = {planning_time}, bold = {boldness}, rs = {reaction_strategy}, {agent_score}/{total_score}, epsilon = {epsilon}')
        return epsilon 
        
        
if __name__ == '__main__':
    # rcParams.update(matplotlib.rcParamsDefault)
    rcParams['font.family'] = 'serif'  # 字体类型
    rcParams['font.sans-serif'] = ['Times']  # 指定字体
    # rc('text', usetex=True)
    test = AgentTest()
    # test.just_plot = True
    # test.test12()
    # test.test3()
    # test.test4()
    # test.test5()
    # test.test6()
    # test.test7()
    # test.test8()
    test.test9()
    # test.test10()
    
