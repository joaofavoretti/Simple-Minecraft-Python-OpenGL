
from Block import Block
import numpy as np
import glm
from OpenGL.GL import *


class CloudBlock(Block):


    def __init__(self, pos):

        self.texture_indices = {
            "top": (6, 1),
            "bottom": (6, 1),
            "left": (6, 1),
            "right": (6, 1),
            "front": (6, 1),
            "back": (6, 1),
        }
        
        super().__init__(pos)



class Cloud:

    def __init__(self, pos):
        
        self.cloudBlocks = self.defineCloudBlocks(pos)

        self.vertices = self.getVertices()
        self.texture = self.getTexture()
        self.normals = self.getNormals()


    def defineCloudBlocks(self, pos):
        cloudBlocks = []

        cloudBlocks.append(CloudBlock(pos))
        for i in range(3):
            for j in range(5):
                cloudBlocks.append(CloudBlock((pos[0] + i, pos[1], pos[2]+j)))
                cloudBlocks.append(CloudBlock((pos[0] - i, pos[1], pos[2]-j)))
                cloudBlocks.append(CloudBlock((pos[0] - i, pos[1], pos[2]+j)))
                cloudBlocks.append(CloudBlock((pos[0] + i, pos[1], pos[2]-j)))

        return np.array(cloudBlocks)
    
    def getVertices(self):
        """
            Get the vertices of the chunk
        """
        vertices = np.empty((0, 3), dtype=np.float16)
        for block in self.cloudBlocks:
            vertices = np.vstack((vertices, block.getVertices()))
        return vertices
    
    def getTexture(self):
        """
            Get the texture of the chunk
        """
        texture = np.empty((0, 2), dtype=np.float16)
        for block in self.cloudBlocks:
            texture = np.vstack((texture, block.getTexture()))
        return texture
 
    def getNormals(self):
        """
            Get the normals of the chunk
        """
        normals = np.empty((0, 3), dtype=np.float16)
        for block in self.cloudBlocks:
            normals = np.vstack((normals, block.getNormals()))
        return normals
    

    def setVerticesAndTexture(self, program):
        if not hasattr(self, 'vertice_buffer'):
            self.vertice_buffer, self.texture_buffer, self.normal_buffer = glGenBuffers(3)
        
        # Vertices
        glBindBuffer(GL_ARRAY_BUFFER, self.vertice_buffer)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        loc = glGetAttribLocation(program, "position")
        glEnableVertexAttribArray(loc)

        stride = self.vertices.strides[0]
        offset = ctypes.c_void_p(0)

        glVertexAttribPointer(loc, 3, GL_FLOAT, False, stride, offset)

        # Texture
        glBindBuffer(GL_ARRAY_BUFFER, self.texture_buffer)
        glBufferData(GL_ARRAY_BUFFER, self.texture.nbytes, self.texture, GL_STATIC_DRAW)

        loc = glGetAttribLocation(program, "texture")
        glEnableVertexAttribArray(loc)

        stride = self.texture.strides[0]
        offset = ctypes.c_void_p(0)

        glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride, offset)
        
        # Normals
        glBindBuffer(GL_ARRAY_BUFFER, self.normal_buffer)
        glBufferData(GL_ARRAY_BUFFER, self.normals.nbytes, self.normals, GL_STATIC_DRAW)

        loc = glGetAttribLocation(program, "normal")
        glEnableVertexAttribArray(loc)

        stride = self.normals.strides[0]
        offset = ctypes.c_void_p(0)

        glVertexAttribPointer(loc, 3, GL_FLOAT, False, stride, offset)

    def draw(self, program, camera):
        """
            Draw the chunk
        """
        loc_model = glGetUniformLocation(program, "model")
        model_array = np.array(glm.mat4(1.0), dtype=np.float32)
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, model_array)

        loc_view = glGetUniformLocation(program, "view")
        view_array = np.array(camera.view, dtype=np.float32)
        glUniformMatrix4fv(loc_view, 1, GL_TRUE, view_array)

        self.setVerticesAndTexture(program)
        
        glDrawArrays(GL_QUADS, 0, 24 * len(self.cloudBlocks))
        