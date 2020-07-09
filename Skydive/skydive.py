import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

g = 9.8  # gravitational constant
m = 118  # mass of the jumper with equipment
t = np.linspace(0, 546, 100000)  # array with 100k moments in time between 0 and 546 s

def func_der_list1(deriv1, t1):  # function returning the derivative of the functions in deriv1 = [altitude, velocity] for phase 1
    z1, v1 = deriv1[0], deriv1[1]  # calls altitude z1 and velocity v1
    A = .85  # cross section
    C = .2  # drag coefficient
    rho = 1.22*np.e**(z1/10000-4)  # air density
    return [v1, g-1/2*rho*C*A*v1**2/m]

y = odeint(func_der_list1, [0, 0], t)  # performs the integration routine as if the whole flight were in phase 1

ind = y[:,0] >= 38000  # finds the Boolean array for the values of the altitude >= 38000, where phase 2 starts

def func_der_list2(deriv2, t2):  # function returning the derivative of the functions in deriv1 = [altitude, velocity] for phase 2
    v2 = deriv2[1]  # calls velocity v2
    A = 1+50*(1-np.e**(-(t2-tJ)/5))/(1+np.e**(-(t2-tJ)/5))  # cross section
    C = 1.5  # drag coefficient
    rho = 1.22  # air density
    return [v2, g-1/2*rho*C*A*v2**2/m]

tJ = t[ind][0]  # calls tJ the time where the first value of altitude >= 38000 is found
y[ind] = odeint(func_der_list2, [y[ind, 0][0], y[ind, 1][0]], t[ind])  # performs the integration routine for phase 2 and overwrites the previous values

z = y[:,0]  # calls altitude z
v = y[:,1]  # calls velocity v
plt.suptitle('Sky Dive', size='large', weight='bold')  # general title for the page

# first plot
plt.subplot(211)
plt.plot(t, z/1000, linewidth=2, color='c')
plt.title('Altitude as a function of time')
plt.xlabel('Time [s]', size='small')
plt.xlim(0, 546)
plt.ylabel('Altitude [km]', size='small')
plt.ylim(40, 0)  # reversed y to show that the jumper is falling

# second plot
plt.subplot(212)
plt.plot(t, v, linewidth=2)
plt.title('Fall velocity as a function of time')
plt.xlabel('Time [s]', size='small')
plt.xlim(0, 546)
plt.ylabel('Fall velocity [m/s]', size='small')

# layout adjusting for the subplots not to overlap
plt.tight_layout()
plt.subplots_adjust(top=.88)

# save plot
plt.savefig('skydive.pdf')

# the function returns a boolean array where the True values occur where there is a change in the sign of the function
def findrootindex(function):
    return [np.diff(np.sign(function)) != 0]  # use the result with [1:] slice of the initial array!

# maximum velocity
maxindex = findrootindex(np.diff(v))  # finds where sign of change in v changes sign, use with [2:] slice of the initial array!
print("The maximum velocity is {:.2f} km/h.".format(v[2:][maxindex][0]*3.6))  # finds max v: when change in v changes sign for the first time and converts into km/h
print("The maximum velocity is reached after {:.2f} s.".format(t[2:][maxindex][0]))  # finds time when max v is reached

# total duration of the flight
totflightindex = findrootindex(z - 40000)  # finds where z is first more than 40000
print("The total time of flight is {:.2f} s.".format(t[1:][totflightindex][0]))  # finds the total time of flight
print("The terminal velocity on the ground is {:.2f} m/s.".format(v[1:][totflightindex][0]))  # finds the velocity on the ground