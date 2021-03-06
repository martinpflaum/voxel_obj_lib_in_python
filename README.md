# voxel_obj_lib_in_python
This is a simple libary for creating voxel 3D-obj files in python. There is another implementation in cpp (link: https://github.com/martinpflaum/voxel_obj_lib_in_cpp)

```WorldGrid``` takes as first parameter the 3d grid size of the world. In our example the grid would be of size 4x4x4. The second parameter of ```WorldGrid``` is the size of the colorpallete. With a colorpallete of size 8, the textures you want to apply onto the object should be in a 8x8 grid. A 8x8 grid is for example 64x64 - each texture is then 8x8 pixel large. Its not that complicated just try some textures with same width and hight out.

In ```__setitem__``` the first argument are the x,y,z coordinate of the cube you want to change. The second argument of ```__setitem__``` is the colorvalue of the voxel. -1 stands for void. The colorvalue 0 corresponds to the pixel value at point 0,0 in texture palette. The obj() function returns the string that contains the objfile
```python
from voxelobj import *
worldGrid = WorldGrid(4,8)
worldGrid[1,1,1] = 1
worldGrid[0,1,1] = -1
worldGrid[1,0,1] = -1
worldGrid[1,1,0] = -1
worldGrid[2,1,1] = -1
worldGrid[1,2,1] = -1
worldGrid[1,1,2] = -1
write("output.obj",worldGrid.obj())
```
