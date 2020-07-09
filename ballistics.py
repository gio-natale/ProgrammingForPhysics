#GIOVANNI NATALE 70919469
#This code plots the numerically computed distance to impact, maximum height, time of flight and velocity at the impact at different launch angles (0 to pi/2) for the projectile motion of an object with mass 1 kg in a fluid with a friction coefficient 0.1 kg/s and Earth gravity. The three plots represent respectively initial velocity of 1, 10, 80 m/s.

import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages #imports library to save PDFs with multiple pages

g = 9.8 #Earth gravity acceleration
vT = g/0.1 #constant for the mass*gravity/(friction coefficient)
v0 = [1, 10, 80] #list with the three initial speeds
theta = np.arange(0, np.pi/2, np.pi/200) #array with 100 values for launch angles ranging from 0 to pi/2

def x(t, theta, i): #horizontal position as a function of time t, launch angle theta and index for the list of initial velocities
    return vT/g*v0[i]*np.cos(theta)*(1-np.e**(-g*t/vT))

def y(t, theta, i): #vertical position as a function of time t, launch angle theta and index for the list of initial velocities
    return vT/g*(v0[i]*np.sin(theta)+vT)*(1-np.e**(-g*t/vT))-vT*t

def deriv(x, f, f_args, h=0.01): #finds the numerical derivative of the function f at x with increasing step h (0.01 default), f_args is a tuple with further constant parameters for the parameter function f
    return (f(x+h, *f_args)-f(x, *f_args))/h

with PdfPages('project1.pdf') as pdf: #saves each plot as a page of the file project1.pdf, each page contains the plots for the four quantities with one of the initial velocities
    for i in range(3): #for each of the initial velocities in the list
        plt.suptitle('Plots for initial speed {} m/s'.format(v0[i]), weight = 'bold') #general title for the page
        ttot = opt.fsolve(y, np.full(100, 100, dtype = 'float64'), args = (theta, i)) #finds values of time when y = 0 for each theta in the array, the initial guess is 100, i.e. an arbitrary high value so that the solution for the equation is not 0
#plotting and settings for the plot of the distance to impact D
        plt.subplot(221) #first plot
        plt.plot(theta, x(ttot, theta, i), color = 'r') #x(ttot) gives the distance to impact
        plt.title(r'Distance $D$ against launch angle $\theta$', size = 'small') #uses LaTex for the title
        plt.tick_params(labelsize = '6')
        plt.xlabel(r"$\theta$ [rad]", size = 'small')
        plt.ylabel(r'$D$ [m]', size = 'small')
#plotting and settings for the plot of the time of flight ttot
        plt.subplot(223) #third plot
        plt.plot(theta, ttot, color = 'g')
        plt.title(r'Time of flight $t_{total}$ against launch angle $\theta$', size = 'small')
        plt.tick_params(labelsize = '6')
        plt.xlabel(r"$\theta$ [rad]", size = 'small')
        plt.ylabel(r'$t_{total}$ [s]', size = 'small')

        vx = deriv(ttot, x, (theta, i)) #finds x component of the velocity at the impact v_impact
        vy = deriv(ttot, y, (theta, i)) #finds y component of the velocity at the impact v_impact
#plotting and settings for the plot of v_impact
        plt.subplot(224) #fourth plot
        plt.plot(theta, np.sqrt(vx**2+vy**2), color = 'c') #the magnitude of the velocity of v_impact is found by Pythagoras theorem
        plt.title(r'Speed $V_{impact}$ against launch angle $\theta$', size = 'small')
        plt.tick_params(labelsize = '6')        
        plt.xlabel(r"$\theta$ [rad]", size = 'small')
        plt.ylabel(r'$V_{impact}$ [m/s]', size = 'small')

        tH = opt.fsolve(deriv, ttot, args = (y, (theta, i))) #finds the time when the derivative of y = 0, i.e. when the height is maximum
#plotting and settings for the plot of maximum height H
        plt.subplot(222) #second plot
        plt.plot(theta, y(tH, theta, i)) #y(tH) is the maximum height
        plt.title(r'Maximum height $H$ against launch angle $\theta$', size = 'small')
        plt.axis(ymin = 0)
        plt.tick_params(labelsize = '6')
        plt.xlabel(r"$\theta$ [rad]", size = 'small')
        plt.ylabel(r'$H$ [m]', size = 'small')
#layout adjusting for the subplots not to overlap
        plt.tight_layout()
        plt.subplots_adjust(hspace = .45, top = .88)
#saving plots
        pdf.savefig()
        plt.clf() #clears the current figure for the new plots to be drawn
