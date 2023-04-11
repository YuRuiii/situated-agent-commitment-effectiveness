import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import math

rc('font',**{'family':'serif','serif':['Times']})
rc('text', usetex=True)

gamma_list = [1, 2, 3, 4, 6, 10, 12, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 80, 100]
log10gamma_list = [math.log10(gamma) for gamma in gamma_list]
epsilon_list = np.load('res/fig12.npy')
plt.figure(2)
plt.title('Figure 2: Effect of Rate of World Change (log x-scale)')
plt.xlabel(r'$\log_{10}\gamma$')
plt.xlim(0.4,2)
plt.ylabel(r'$\epsilon$')
plt.plot(log10gamma_list, epsilon_list, linestyle='-',  marker='o', markersize=4)
plt.savefig('fig/fig2.png')