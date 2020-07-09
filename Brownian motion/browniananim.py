import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
npoint=400
nframe=5000
xmin,xmax,ymin,ymax=0,1,0,1
fig, ax = plt.subplots()
plt.xlim(xmin,xmax)
plt.ylim(ymin,ymax)
Dt=0.001
def update_point(num):
    global x,y,vx,vy,xG,yG,vxG,vyG
    indx=np.where((x < xmin) | (x > xmax))
    indy=np.where((y < ymin) | (y > ymax))
    ind = np.where((x-xG)**2+(y-yG)**2<.03**2)
    vx[indx]=-vx[indx]
    vy[indy]=-vy[indy]
    if not(xmin + .03 < xG < xmax - .03):
        vxG = - vxG
    if not(ymin + .03 < yG < ymax - .03):
        vyG = - vyG
    cos = (x[ind] - xG)/.03
    sin = (y[ind] - yG)/.03
    nind = np.where(cos*vx[ind]+sin*vy[ind] < 0)
    dvx, dvy = -2*cos[nind]*(cos[nind]*vx[ind][nind]+sin[nind]*vy[ind][nind]), -2*sin[nind]*(cos[nind]*vx[ind][nind]+sin[nind]*vy[ind][nind])
    newvx, newvy = vx[ind], vy[ind]
    newvx[nind] += dvx
    newvy[nind] += dvy
    vx[ind], vy[ind] = newvx, newvy
    vxG, vyG = vxG - dvx.sum()/20, vyG - dvy.sum()/20
    dx=Dt*vx
    dy=Dt*vy
    xG, yG = xG + Dt*vxG, yG + Dt*vyG
    x=x+dx
    y=y+dy
    data=np.stack((np.append(x, xG), np.append(y, yG)),axis=-1)
    im.set_offsets(data)
xG, yG = .5, .5
vxG, vyG = 0, 0
x = np.random.random(npoint)
y = np.random.random(npoint)
ind0 = np.where((x-xG)**2+(y-yG)**2<.03**2)
while len(ind0[0]) != 0:
    x[ind0], y[ind0] = np.random.random(len(ind0[0])), np.random.random(len(ind0[0]))
    ind0 = np.where((x-xG)**2+(y-yG)**2<=.03**2)
vx=np.random.randn(npoint)
vy=np.random.randn(npoint)
im = ax.scatter(np.append(x, xG), np.append(y, yG), np.append(np.full(npoint, 20.), 200))
animation = animation.FuncAnimation(fig, update_point,nframe,interval=1,repeat=False)
plt.show()
#animation.save(browniananim.mp4)