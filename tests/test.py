#%%
from voxelobj import *
worldGrid = WorldGrid(4,8)
worldGrid[1,1,1] = 1
worldGrid[0,1,1] = -1
worldGrid[1,0,1] = 1
worldGrid[1,1,0] = 1
worldGrid[2,1,1] = -1
worldGrid[1,2,1] = -1
worldGrid[1,1,2] = -1
write("output.obj",worldGrid.obj())

# %%
