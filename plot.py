import matplotlib.pyplot as plt
from matplotlib import rc

rc('font',**{'family':'serif','serif':['Times']})
rc('text', usetex=True)
plt.plot([1,2,3,4], [5,6,7,8], linestyle='-',  marker='o', markersize=3)
plt.xlabel(r'$\log_{10}\epsilon$')
plt.show()