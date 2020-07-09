import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.integrate import odeint
from matplotlib.backends.backend_pdf import PdfPages

g = 9.8
F = .1
b = .15
t = np.linspace(0, 50, 10000)
omega0 = np.sqrt(g)
omegas = np.linspace(.1, 8, 500)

def theta_derivs(deriv, tF):
    theta, dtheta = deriv[0], deriv[1]
    return [dtheta, -b*dtheta-g*np.sin(theta)+F*np.cos(omega*tF)*np.cos(theta)]

maxampl = np.array([])
for omega in omegas:
    thetafuncs = odeint(theta_derivs, [0, 0], t)
    maxampl = np.append(maxampl, (np.abs(thetafuncs[:, 0])).max())        
plt.plot(omegas, maxampl, lw=1.2)
plt.title('Maximum amplitude of the pendulum against frequency of the forced force', va='bottom')
plt.xlabel(r'Frequency of the forced force $\omega$ [rad/s]')
plt.ylabel(r'Maximum amplitude $max$ $\theta$ [rad]')
plt.axis(ymax = .22, xmin = .1)
plt.savefig('resonance.pdf')
plt.show()

omega = 3
thetafuncs = odeint(theta_derivs, [0, 0], np.linspace(0, 60, 1000))
angles = thetafuncs[:, 0]
fig = plt.figure()
plt.ylim(-1.2,.2)
plt.xlim(-1.2,1.2)
ims = []
for angle in angles:
    ims.append(plt.plot(np.array([0, np.sin(angle)]), np.array([0, -np.cos(angle)]), 'o-k', markeredgewidth=10))
imani = animation.ArtistAnimation(fig, ims, interval=60, repeat=False)
plt.show()

with PdfPages('phase_space.pdf') as pdf: 
    for i in range(3):
        omega = (omega0/10, omega0, omega0*10)[i]
        t = np.linspace(0, (60, 40, 7)[i], 10000)
        thetafuncs = odeint(theta_derivs, [0, 0], t)
        plt.suptitle(r'Plots for $\omega={:.3f}$'.format(omega), size='larger')
        plt.subplot(211)
        plt.plot(t, 1000*thetafuncs[:, 0], color='r')
        plt.xlabel(r'Time [s]')
        plt.ylabel(r'Angle to the vertical $\theta$ [mrad]')
        plt.subplot(212)
        plt.plot(t, 1000*thetafuncs[:, 1])
        plt.xlabel(r'Time [s]')
        plt.ylabel(r'Derivative of $\theta$ $d\theta/dt$ [mrad/s]')
        plt.tight_layout()
        plt.subplots_adjust(top = .91)
        pdf.savefig()
        plt.clf()