#%%
import numpy as np

def splitt_face(face):
    lsg_left = np.zeros_like(face)
    lsg_up = np.zeros_like(face)
    is_end = np.zeros_like(face) + 1 #makes more sence

    for row in range(face.shape[0]):#row
        for col in range(face.shape[1]):
            if row == 0 and col == 0:
                is_end[row,col] = 1
            elif row == 0:
                if face[row,col-1]==face[row,col] and is_end[row,col - 1]:
                    is_end[row,col-1] = 0
                    is_end[row,col] = 1

                    lsg_left[row,col] = lsg_left[row,col-1] + 1
                else:
                    is_end[row,col] = 1
            elif col == 0:
                if face[row-1,col]==face[row,col] and is_end[row-1,col]:
                    is_end[row-1,col] = 0
                    is_end[row,col] = 1

                    lsg_up[row,col] = lsg_up[row-1,col] + 1
                else:
                    is_end[row,col] = 1
            else:
                if face[row-1,col]==face[row,col] and is_end[row-1,col] and face[row,col-1]==face[row,col] and is_end[row,col - 1] and lsg_left[row,col-1] + 1 == lsg_left[row -1,col]:
                    is_end[row-1,col] = 0
                    is_end[row,col-1] = 0
                    is_end[row,col] = 1

                    lsg_left[row,col] = lsg_left[row-1,col]
                    lsg_up[row,col] = lsg_up[row-1,col] + 1
                elif lsg_up[row,col-1] == 0 and face[row,col-1] == face[row,col] and is_end[row,col-1] == 1:
                    lsg_left[row,col] = lsg_left[row,col-1] + 1
                    is_end[row,col-1] = 0
                    is_end[row,col] = 1

                elif lsg_left[row - 1,col] == 0 and face[row - 1,col] == face[row,col] and is_end[row-1,col] == 1:
                    lsg_up[row,col] = lsg_up[row-1,col] + 1
                    is_end[row - 1,col] = 0
                    is_end[row,col] = 1

                else:
                    is_end[row,col] = 1
        #print(face[k])
    return lsg_left,lsg_up, is_end

def get_idx(lsg_left,lsg_up, is_end,face):
    out = []
    for row in range(face.shape[0]):
        for col in range(face.shape[1]):
            if is_end[row,col] == 1 and face[row,col] != 0:
                left_top_y = row - lsg_up[row,col]
                left_top_x = col - lsg_left[row,col]
                
                right_top_y = row - lsg_up[row,col] 
                right_top_x = col + 1
                
                right_down_y = row + 1
                right_down_x = col + 1

                left_down_y = row + 1
                left_down_x = col - lsg_left[row,col]
                
                points3d = [(int(left_top_y),int(left_top_x)),
                (int(right_top_y),int(right_top_x)),
                (int(right_down_y),int(right_down_x)),
                (int(left_down_y),int(left_down_x))]

                color = 0
                clockwise = True
                if face[row,col] < 0:
                    clockwise = True
                    color = (-face[row,col]) -1
                else:
                    clockwise = False
                    color = face[row,col] - 1
                out.append((points3d,int(color),clockwise))
    return out



class PolygonGrid():
    def __init__(self,size):
        self.dim = None
        self.dim_idx = None
        
        self.size = size
        self.edge_lines = np.zeros((size+1,size+1,size+1))-1
        self.out = ""
        self.current_line = 1
        self.mul = 50
    def get_edge_line(self,row,col):
        if self.dim == 0:
            return self.edge_lines[self.dim_idx,row,col]
        if self.dim == 1:
            return self.edge_lines[row,self.dim_idx,col]
        if self.dim == 2:
            return self.edge_lines[row,col,self.dim_idx]
    def set_edge_line(self,row,col,value):
        if self.dim == 0:
            self.out += f"v {self.dim_idx * self.mul} {row * self.mul} {col * self.mul}\n"
            self.edge_lines[self.dim_idx,row,col] = value
        if self.dim == 1:
            self.out += f"v {row * self.mul} {self.dim_idx * self.mul} {col *self.mul}\n"
            self.edge_lines[row,self.dim_idx,col] = value
        if self.dim == 2:
            self.out += f"v {row*self.mul} {col*self.mul} {self.dim_idx*self.mul}\n"
            self.edge_lines[row,col,self.dim_idx] = value

    def get_line(self,row,col):
        if self.get_edge_line(row,col) != -1:
            return int(self.get_edge_line(row,col))
        else:
            self.set_edge_line(row,col,self.current_line)
            self.current_line = self.current_line + 1 
            return int(self.get_edge_line(row,col))

def create_color_line(vecs): 
    out = ""
    for x,y in vecs:
        out += f"vt {x} {y}\n"
    return out

class ColorGrid():
    def __init__(self,size,current_line = 0):
        self.size = size
        self.color_lines = np.zeros((size,size))-1
        self.current_line = current_line
        self.out = ""
    def get_line(self,idx,edge):
        #print("self.color_lines ",self.color_lines.shape)
        if self.color_lines[idx % self.size,idx//self.size] == -1:
            y,x = idx % self.size,idx//self.size

            left_top = ((x/self.size),(y/self.size))
            right_top = ((x/self.size) + 1/self.size,(y/self.size))
            
            right_bot = ((x/self.size) + 1/self.size,(y/self.size) + 1/self.size)
            left_bot = ((x/self.size),(y/self.size) + 1/self.size)
            
            self.out += create_color_line([left_top,right_top,right_bot,left_bot])
            
            #print("type(idx self.color_lines) ",idx % self.size)
            self.color_lines[idx % self.size,idx//self.size] = self.current_line
            
            self.current_line = self.current_line + 1
            return int(self.color_lines[idx % self.size,idx//self.size] * 4 + edge + 1)
        else:
            return int(self.color_lines[idx % self.size,idx//self.size]* 4 + edge + 1)

def createfaces(polygonGrid,colorGrid,idxtmp):
    group = polygonGrid.dim
    out = ""
    for elem in idxtmp:
        points3d,color,clockwise = elem
        

        finalGroup = 0

        if clockwise:
            finalGroup = 2*group + 1
        else:
            finalGroup = 2*group + 2
        
        #f v1/vt1 v2/vt2 v3/vt3 ...
        fline = []
        for k,edge in enumerate(points3d):
            wline = polygonGrid.get_line(edge[0],edge[1])
            cline = colorGrid.get_line(color,k)
            fline.append((wline,cline))
        
        if clockwise:
            fline = fline[::-1]
            #3 2 1 0
            #2 1 3 0
            #3 1 2 0
            #3 0 1 2
            #fline = [fline[0],fline[2],fline[1],fline[3]]

        out += f"s {finalGroup}\nf "
        for wline,cline in fline:
            out += f"{wline}/{cline}/{finalGroup} "
        out += "\n"
    return out

def cube_valid(size,x,y,z):
    if x >= size or y >= size or z >= size:
        return False
    if x < 0 or y < 0 or z < 0:
        return False
    return True
    

class WorldGrid():
    def __init__(self,size,color_size = 8):
        self.color_size = color_size
        self.voxel = np.zeros((size,size,size)) - 1
        self.xfaces = np.zeros((size +1,size,size))
        self.yfaces = np.zeros((size,size+1,size))
        self.zfaces = np.zeros((size,size,size + 1))
        self.size = size
    def cube_not_empty(self,x,y,z):
        if not cube_valid(self.size,x,y,z):
            return False
        else:
            return (self.voxel[x,y,z] > 0)
    def __setitem__(self, idx, item):
        x,y,z = idx
        self.voxel[x,y,z] = item
        if item == -1:
            if self.cube_not_empty(x-1,y,z):
                self.xfaces[x,y,z] = self.voxel[x-1,y,z] * (-1)
            if self.cube_not_empty(x+1,y,z):
                self.xfaces[x+1,y,z] = self.voxel[x+1,y,z] * (1)
            
            if self.cube_not_empty(x,y-1,z):
                #print("cube_valid(self.size,x,y-1,z)")
                self.yfaces[x,y,z] = self.voxel[x,y-1,z] * (1)
            if self.cube_not_empty(x,y+1,z):
                #print("cube_valid(self.size,x,y-1,z)")
                self.yfaces[x,y+1,z] = self.voxel[x,y+1,z] * (-1)

            if self.cube_not_empty(x,y,z-1):
                self.zfaces[x,y,z] = self.voxel[x,y,z-1] * (-1)
            if self.cube_not_empty(x,y,z+1):
                self.zfaces[x,y,z+1] = self.voxel[x,y,z+1] * (1)
        else:
            if not cube_valid(self.size,x-1,y,z) or self.voxel[x-1,y,z] == -1:
                self.xfaces[x,y,z] = item * (1)
            else:
                self.xfaces[x,y,z] = 0
            
            if not cube_valid(self.size,x+1,y,z) or self.voxel[x+1,y,z] == -1:
                self.xfaces[x+1,y,z] = item * (-1)
            else:
                self.xfaces[x + 1 ,y,z] = 0

            if not cube_valid(self.size,x,y-1,z) or self.voxel[x,y-1,z] == -1:
                #print("facey set ",self.voxel[x,y-1,z] )
                self.yfaces[x,y,z] = item * (-1)
            else:
                self.yfaces[x,y,z] = 0
        
            if not cube_valid(self.size,x,y+1,z) or self.voxel[x,y+1,z] == -1:
                self.yfaces[x,y+1,z] = item * (1)
            else:
                self.yfaces[x,y+1,z] = 0
            
            if not cube_valid(self.size,x,y,z-1) or self.voxel[x,y,z-1] == -1:
                self.zfaces[x,y,z] = item * (1)
            else: 
                self.zfaces[x,y,z] = 0

            if not cube_valid(self.size,x,y,z+1) or self.voxel[x,y,z+1] == -1:
                self.zfaces[x,y,z+1] = item * (-1)
            else:
                self.zfaces[x,y,z+1] = 0
    def obj(self):
        polygonGrid = PolygonGrid(self.size)
        colorGrid = ColorGrid(self.color_size)
        out_faces = ""

        polygonGrid.dim = 0
        for k in range(self.size + 1):
            face = self.xfaces[k,:,:]
            polygonGrid.dim_idx = k
            tmp = splitt_face(face)
            idxtmp = get_idx(*tmp,face)
            #print("face x ",face)
            out_faces += createfaces(polygonGrid,colorGrid,idxtmp)
        
        polygonGrid.dim = 1
        for k in range(self.size + 1):
            face = self.yfaces[:,k,:]
            polygonGrid.dim_idx = k
            tmp = splitt_face(face)
            idxtmp = get_idx(*tmp,face)
            #print("face y ",face)
            out_faces += createfaces(polygonGrid,colorGrid,idxtmp)
        
        polygonGrid.dim = 2
        for k in range(self.size + 1):
            face = self.zfaces[:,:,k]
            polygonGrid.dim_idx = k
            tmp = splitt_face(face)
            idxtmp = get_idx(*tmp,face)
            #print("face z ",face)
            out_faces += createfaces(polygonGrid,colorGrid,idxtmp)

        out = ""
        out += polygonGrid.out
        out += colorGrid.out
        out += "vn 1.000000 0.000000 0.000000\n"
        out += "vn -1.000000 0.000000 0.000000\n"
        out += "vn 0.000000 1.000000 0.000000\n"
        out += "vn 0.000000 -1.000000 0.000000\n"
        out += "vn 0.000000 0.000000 1.000000\n"
        out += "vn 0.000000 0.000000 -1.000000\n"
        out += out_faces
        return out
    def __getitem__(self,idx):
        return self.voxel[idx]

#worldGrid = WorldGrid(5)

def write(filename,input):
    file1 = open(filename,"w") 
    file1.write(input) 
    file1.close()



"""worldGrid = WorldGrid(4)
worldGrid[1,1,1] = 1
worldGrid[0,1,1] = -1
worldGrid[1,0,1] = -1
worldGrid[1,1,0] = -1
worldGrid[2,1,1] = -1
worldGrid[1,2,1] = -1
worldGrid[1,1,2] = -1
write("ariba.obj",worldGrid.obj())
"""


#%%

