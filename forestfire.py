import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import matplotlib.colors as col
    
def changeprob(array, prob, val):
    array[np.random.random(array.shape) <= prob] = val
    return array

initial = .55
p = .01
f = .001

grid = np.zeros((100,100))
patterns = [(1,0,0,0), (0,1,0,0), (0,0,1,0), (0,0,0,1), (1,0,1,0), (1,0,0,1), (0,1,1,0), (0,1,0,1)]
grid = changeprob(grid, initial, 1)

forest = col.LinearSegmentedColormap.from_list("rgb",[(0,"w"),(.5,"r"),(1,"g")])
fig, ax = plt.subplots()
graph = ax.pcolormesh(grid, cmap=forest)

def update_grid(num):
    def neighbourburning():
        nbmatrix = np.full(grid.shape, 1.)
        l = len(grid) - 1  # assuming it is a square array
        for (a,b,c,d) in patterns:
            nbmatrix[b:l-a,d:l-c][oldgrid[a:l-b,c:l-d] == .5] = .5
        return nbmatrix[oldgrid == 1]
    oldgrid = np.copy(grid)
    grid[oldgrid == .5] = 0
    grid[oldgrid == 0] = changeprob(grid[oldgrid == 0], p, 1)
    grid[oldgrid == 1] = neighbourburning()
    grid[grid == 1] = changeprob(grid[grid == 1], f, .5)
    graph = ax.pcolormesh(grid, cmap=forest)
    return graph
    
animation = anim.FuncAnimation(fig, update_grid, 300, repeat=False)
#animation.save("forestfire.mp4")