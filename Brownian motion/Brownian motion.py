# GIOVANNI NATALE 70949169
# Plots of trajectory of a grain in brownian motion and
# square distance from initial position against time

import numpy as np
import matplotlib.pyplot as plt

npoint = 4000  # number of molecules
nframe = 15000  # number of steps
xmin, xmax, ymin, ymax = 0, 1, 0, 1
Dt = 0.001  # time step


def update_grid(num):  # updates the animation
    global x, y, vx, vy, xG, yG, vxG, vyG
# inverts velocity when molecules collide with box
    indx = np.where((x < xmin) | (x > xmax))
    indy = np.where((y < ymin) | (y > ymax))
    vx[indx] = -vx[indx]
    vy[indy] = -vy[indy]
# inverts velocity when grain collides with box
    if not(xmin + .03 <= xG <= xmax - .03):
        vxG = - vxG
    if not(ymin + .03 <= yG <= ymax - .03):
        vyG = - vyG
    ind = np.where((x-xG)**2+(y-yG)**2 <= .03**2)  # when mols collide with grain
    # cos and sin of the angle of the radius to the point of collision
    cos = (x[ind] - xG)/.03
    sin = (y[ind] - yG)/.03
    nind = np.where(cos*vx[ind]+sin*vy[ind] < 0)  # checks mol is outside grain
# change in velocity for molecules
    dvx, dvy = -2*cos[nind]*(cos[nind]*vx[ind][nind]+sin[nind]*vy[ind][nind]), -2*sin[nind]*(cos[nind]*vx[ind][nind]+sin[nind]*vy[ind][nind])
    newvx, newvy = vx[ind], vy[ind]
    newvx[nind] += dvx
    newvy[nind] += dvy
    vx[ind], vy[ind] = newvx, newvy
# change in velocity for grain, sum of all mols' contributions *mass ratio
    vxG, vyG = vxG - dvx.sum()/20, vyG - dvy.sum()/20
# change in mols' position
    dx = Dt*vx
    dy = Dt*vy
# new grain position
    xG, yG = xG + Dt*vxG, yG + Dt*vyG
# new mols' position
    x = x + dx
    y = y + dy

# initial sum of square distance over time
sumsqdist = np.full(nframe + 1, 0.)
for i in range(20):  # runs 20 times
# initial position of grain
    xG, yG = .5, .5
# initial velocity of grain
    vxG, vyG = 0, 0
# initial position of molecules
    x = np.random.random(npoint)
    y = np.random.random(npoint)
# takes molecules inside the grain out of it
    ind0 = np.where((x-xG)**2+(y-yG)**2 < .03**2)
    while len(ind0[0]) != 0:
        x[ind0], y[ind0] = np.random.random(len(ind0[0])), np.random.random(len(ind0[0]))
        ind0 = np.where((x-xG)**2+(y-yG)**2 <= .03**2)
# initial velocity of molecules
    vx = np.random.randn(npoint)
    vy = np.random.randn(npoint)
# array containing x and y position over time
    xtraj, ytraj = np.array([xG]), np.array([yG])
    for j in range(nframe):  # iterates over all frames
        update_grid(j)
# appends new position of grain
        xtraj = np.append(xtraj, xG)
        ytraj = np.append(ytraj, yG)
    if i == 0:  # plots trajectory for the first cycle
        plt.plot(xtraj, ytraj)
        plt.title('Trajectory of the grain')
        plt.xlabel('x [m]')
        plt.ylabel('y [m]')
        plt.xlim(xmin, xmax)
        plt.ylim(ymin, ymax)
        #.plt.savefig('brownianpath.pdf')
        plt.show()
# sums value of square distance for each cycle
    sumsqdist += (.5 - xtraj)**2 + (.5 - ytraj)**2

# time array
t = np.linspace(0, nframe*Dt, nframe + 1)
# average square distance
avsqdist = sumsqdist/20

plt.clf()
# plot of average square distance against time
plt.plot(t, avsqdist)
plt.title('Square distance to initial position vs. time')
plt.xlabel('Time [s]')
plt.xlim(0, 15)
plt.ylabel(r'Square distance [$m^2$]')
plt.show()
#plt.savefig('brownianscatter.pdf')