# voxel_obj_lib_in_python
This is a simple libary for creating voxel obj files in python. There is another implementation in cpp https://github.com/martinpflaum/voxel_obj_lib_in_cpp

WorldGrid takes as first parameter the worldgridsize meaning x,y,z coordinates of 3Dworld. The second parameter of WorldGrid is the size of the colorpallete x,y. so with a colorpallete of size 8 the textures you want to apply onto the object should be in a 8x8 grid. A 8x8 grid is for example 64x64 - each texture is 8x8 pixel. Its not that complicated just try some textures with same width and hight out.

in setitem the first 3 arguments are the x,y,z coordinate of the cube you want to change. the 4th argument of setitem is the colorvalue of the voxel. -1 stands for void. the obj() function returns the string that contains the objfile
```python
worldGrid = WorldGrid(4,8)
worldGrid[1,1,1] = 1
worldGrid[0,1,1] = -1
worldGrid[1,0,1] = -1
worldGrid[1,1,0] = -1
worldGrid[2,1,1] = -1
worldGrid[1,2,1] = -1
worldGrid[1,1,2] = -1
write("ariba.obj",worldGrid.obj())
```


in convert_minecraft_schematic.py is an example how to convert minecraft worlds into obj files using mcedit schematics. With mcedit you can export regions as schematics.
