from cycler import cycler
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.integrate import odeint

UA = 149597e+6  # distance Earth-Sun in m
G = 6.67e-11  # gravitational constant
# mass of Sun and planets
M = [1.989e+30, 5.972e24, 6.39e23, 3.3e23, 4.8675e24, 1.90e27, 5.68e26, 8.68e25, 1.02e26]
# initial condition in the form x, y, v_x, v_y for each body
# positions in m, velocities in m/s
initialcond = [0, 0, 0, 0, UA, 0, 0, 29.78e3, 1.523679*UA, 0, 0, 24.077e+3,  .387*UA, 0, 0, 47.362e3, .723*UA, 0, 0, 35.02e3, 5.202*UA, 0, 0, 13.07e3, 9.554*UA, 0, 0, 9.69e3, 19.218*UA, 0, 0, 6.80e3, 30.11*UA, 0, 0, 5.43e3]


def derivs(derivlist, t):  # derivation function
    r = [derivlist[::4], derivlist[1::4]]  # list with all x's and all y's
    # copies derivlist with velocity in place of position
    result = np.append(derivlist[2:], derivlist[:2])
    for i in range(len(r[0])):  # for each body
        # initialises deriv of velocity at 0
        result[4*i+2:4*i+4] = [0, 0]
        # array with position of i-th body
        ri = np.array([r[0][i], r[1][i]])
        for j in range(len(r)):
            if j != i:
                # array with position of j-th body
                rj = np.array([r[0][j], r[1][j]])
                aij = G*M[j]*(rj-ri)/(np.sum((rj-ri)**2))**(3/2)
                # sums contribution from attraction with j-th body
                result[4*i+2] += aij[0]
                result[4*i+3] += aij[1]
    return result


def update(i):
    plt.clf()  # clears figure
    plt.rc('axes', prop_cycle=(cycler('color', col)))  # determines colours
    # prints time flow
    plt.text(.95*axlim[1], axlim[3]-.05*axlim[1], 'Day '+str(i), fontsize=20, ha='right', va='top', color='w')
    # draws trajectory
    plt.plot(r[:i, ::4], r[:i, 1::4], zorder=-1, lw=2.5)
    # plots the planet
    plt.scatter(r[i, ::4], r[i, 1::4], size, col)
    # equals x- and y-axis scale
    plt.axes().set_aspect('equal', 'box')
    # sets background colour to black
    plt.axes().set_axis_bgcolor('k')
    # sets axes limits
    plt.axis(axlim)
    # adds legend
    plt.legend(labels, fontsize='x-small', loc=8, ncol=3)


nframe = 2*687  # number of steps in integration routine
Dt = 24*3600  # time step in seconds
t = Dt*np.arange(0, nframe+1)  # time array
r = odeint(derivs, initialcond[:12], t)  # integrates for Sun, Earth and Mars

r12 = np.array([r[:, 4]-r[:, 0], r[:, 5]-r[:, 1]])  # vector Sun-Earth
r23 = np.array([r[:, 8]-r[:, 4], r[:, 9]-r[:, 5]])  # vector Earth-Mars
# angle between vectors
theta = np.arccos(np.sum(r12*r23, axis=0)/(np.linalg.norm(r12, axis=0)*np.linalg.norm(r23, axis=0)))
# plots theta against time
plt.plot(t, theta)
plt.xlabel(r'$t$ [s]')
plt.ylabel(r'$\theta$ [rad]')
plt.title('Retrograde motion')
plt.savefig('retrograde.pdf')  # saves plot

fig = plt.figure()
# sets axes limits to slightly bigger than the extreme values
axlim = 1.1*np.array([np.amin(r[:, ::4]), np.amax(r[:, ::4]), np.amin(r[:, 1::4]), np.amax(r[:, 1::4])])
# size of planets
size = [1000, 100, 65]
# colour of planets
col = ['OrangeRed', 'DodgerBlue', 'DarkRed']
labels = ['Sun', 'Earth', 'Mars']  # labels
# creates animation
animation1 = animation.FuncAnimation(fig, update, nframe+1, interval=20, repeat=False)
plt.show()
#animation1.save('solarsystem.mp4')  # save animation

r = odeint(derivs, initialcond, t)  # integrates for full Solar System
fig = plt.figure()
# sets axes limits to slightly bigger than the extreme values
axlim = 1.03*np.array([np.amin(r[:, ::4]), np.amax(r[:, ::4]), -np.amax(r[:, 1::4]), np.amax(r[:, 1::4])])
# size of planets
size = 15
# labels
labels = ['Sun', 'Earth', 'Mars', 'Mercury', 'Venus', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
# colour of planets
col = ['OrangeRed', 'DodgerBlue', 'DarkRed', 'LightSlateGray', 'Chocolate', 'BurlyWood', 'Tan', 'LightSkyBlue', 'BlueViolet']
# creates animation
animation2 = animation.FuncAnimation(fig, update, nframe+1, interval=20, repeat=False)
plt.show()
#animation2.save('solarsystem_complete.mp4')  # save animation