# transcendental.py
# Adrian Del Maestro 
# 09.13.2012 

# A graphical solution of a transcendental equation

import matplotlib.pyplot as plt
import numpy as np
plt.style.use('notebook');

x_sol = []

# ----------------------------------------------------------------------------
def trans(x,a):
    ''' A transcendental equation. '''
    return np.tanh(x/a)

def onclick(event):
    x_sol.append(event.xdata)

# ----------------------------------------------------------------------------
# main program
# ----------------------------------------------------------------------------
def main():

    a = np.linspace(0.1,1.0,6)
    x = np.arange(0.0,1.21,0.01)

    # Show the graphical solution
    fig = plt.figure(1)
    plt.plot(x,x,'k-', label='_nolegend_')
    for i,ca in enumerate(a):
        label = 'a = %5.3f' % ca
        plt.plot(x,trans(x,ca),'-', label=label)

    plt.legend(prop={'size':14}, ncol=3, loc='lower right')
    plt.axis([-0.2,1.2,-0.2,1.2])

    # Determine the graphical solution
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()

    # visually identifying the solution
    sol = np.array(x_sol)

    # plot the identified solution
    plt.figure(2)
    plt.plot(a,sol,'o-', linewidth=1, markersize=5, markeredgecolor='gray')
    plt.xlabel(r'$a$')
    plt.ylabel(r'$x$')
    plt.ylim(0,1.1)

    plt.show()
        
if __name__ == '__main__':
    main()
