#%%

from nbtschematic import SchematicFile
sf = SchematicFile.load('test3.schematic')
from obj import *
worldGrid = WorldGrid(280,32)
name = ["emptqef"]

for x in range(200):
    for y in range(50):
        for z in range(50):
            tmp = sf.blocks[x, y, z]
            if tmp == 166 or tmp == 0:
                #print("x = ",x)
                pass
            else:
                if tmp in name:
                    worldGrid[x, y, z] = name.index(tmp)
                else:
                    name.append(tmp)
                    worldGrid[x, y, z] = name.index(tmp)
    print("x = ",x)
    
write("bighouse.obj",worldGrid.obj())

# %%
