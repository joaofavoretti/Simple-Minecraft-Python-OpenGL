import glfw
import glm
from OpenGL.GL import *
import numpy as np
from Block import Block

class Moon:
    
    def __init__(self, pos):

        self.texture_indices = {
            "top": (5, 2),
            "bottom": (5, 2),
            "left": (5, 2),
            "right": (5, 2),
            "front": (5, 2),
            "back": (5, 2),
        }

        self.size = 4
        self.nSquares = 1
        self.squareSize = self.size / self.nSquares
        
        self.vertices = self.defineVertices(pos, self.size)
        self.texture = self.defineTexture(self.texture_indices)
        self.normals = self.defineNormals()


    # TODO: Use a block.obj file to define the vertices
    def defineVertices(self, pos, size):
        """
            Define the vertices of the block

            pos(tuple(float, float, float)) - Position of the block in the world
            size(float) - Size of the block
        """
            
        array_vertices = []

        for i in range(self.nSquares):
            for j in range(self.nSquares):
                array_vertices.append((pos[0] - size/2 + self.squareSize*i ,    pos[1] - size/2 + self.squareSize*j,    pos[2] + size/2)), # positive z face
                array_vertices.append((pos[0] - size/2 + self.squareSize*(i+1), pos[1] - size/2 + self.squareSize*j,    pos[2] + size/2)),
                array_vertices.append((pos[0] - size/2 + self.squareSize*i ,    pos[1] - size/2 + self.squareSize*(j+1),pos[2] + size/2)),
                array_vertices.append((pos[0] - size/2 + self.squareSize*i ,    pos[1] - size/2 + self.squareSize*(j+1),pos[2] + size/2)),
                array_vertices.append((pos[0] - size/2 + self.squareSize*(i+1), pos[1] - size/2 + self.squareSize*j,    pos[2] + size/2)),
                array_vertices.append((pos[0] - size/2 + self.squareSize*(i+1), pos[1] - size/2 + self.squareSize*(j+1),pos[2] + size/2)),
        
                array_vertices.append((pos[0] + size/2, pos[1] - size/2 + self.squareSize*j,    pos[2] - size/2 + self.squareSize*(i+1))), # positive x face
                array_vertices.append((pos[0] + size/2, pos[1] - size/2 + self.squareSize*j,    pos[2] - size/2 + self.squareSize*i)),
                array_vertices.append((pos[0] + size/2, pos[1] - size/2 + self.squareSize*(j+1),pos[2] - size/2 + self.squareSize*(i+1))),
                array_vertices.append((pos[0] + size/2, pos[1] - size/2 + self.squareSize*(j+1),pos[2] - size/2 + self.squareSize*(i+1))),
                array_vertices.append((pos[0] + size/2, pos[1] - size/2 + self.squareSize*j,    pos[2] - size/2 + self.squareSize*i)),
                array_vertices.append((pos[0] + size/2, pos[1] - size/2 + self.squareSize*(j+1),pos[2] - size/2 + self.squareSize*i)),
        
                array_vertices.append((pos[0] - size/2 + self.squareSize*i,     pos[1] - size/2 + self.squareSize*j,    pos[2] - size/2)), # negative z face
                array_vertices.append((pos[0] - size/2 + self.squareSize*(i+1), pos[1] - size/2 + self.squareSize*j,    pos[2] - size/2)),
                array_vertices.append((pos[0] - size/2 + self.squareSize*i,     pos[1] - size/2 + self.squareSize*(j+1),pos[2] - size/2)),
                array_vertices.append((pos[0] - size/2 + self.squareSize*i,     pos[1] - size/2 + self.squareSize*(j+1),pos[2] - size/2)),
                array_vertices.append((pos[0] - size/2 + self.squareSize*(i+1), pos[1] - size/2 + self.squareSize*j,    pos[2] - size/2)),
                array_vertices.append((pos[0] - size/2 + self.squareSize*(i+1), pos[1] - size/2 + self.squareSize*(j+1),pos[2] - size/2)),
            
                array_vertices.append((pos[0] - size/2, pos[1] - size/2 + self.squareSize*j,    pos[2] - size/2 + self.squareSize*(i+1))), # negative x face
                array_vertices.append((pos[0] - size/2, pos[1] - size/2 + self.squareSize*j,    pos[2] - size/2 + self.squareSize*i)),
                array_vertices.append((pos[0] - size/2, pos[1] - size/2 + self.squareSize*(j+1),pos[2] - size/2 + self.squareSize*(i+1))),
                array_vertices.append((pos[0] - size/2, pos[1] - size/2 + self.squareSize*(j+1),pos[2] - size/2 + self.squareSize*(i+1))),
                array_vertices.append((pos[0] - size/2, pos[1] - size/2 + self.squareSize*j,    pos[2] - size/2 + self.squareSize*i)),
                array_vertices.append((pos[0] - size/2, pos[1] - size/2 + self.squareSize*(j+1),pos[2] - size/2 + self.squareSize*i)),

                array_vertices.append((pos[0] - size/2 + self.squareSize*j,     pos[1] - size/2, pos[2] - size/2 + self.squareSize*i)), # negative y face
                array_vertices.append((pos[0] - size/2 + self.squareSize*(j+1), pos[1] - size/2, pos[2] - size/2 + self.squareSize*i)),
                array_vertices.append((pos[0] - size/2 + self.squareSize*j,     pos[1] - size/2, pos[2] - size/2 + self.squareSize*(i+1))),
                array_vertices.append((pos[0] - size/2 + self.squareSize*j,     pos[1] - size/2, pos[2] - size/2 + self.squareSize*(i+1))),
                array_vertices.append((pos[0] - size/2 + self.squareSize*(j+1), pos[1] - size/2, pos[2] - size/2 + self.squareSize*i)),
                array_vertices.append((pos[0] - size/2 + self.squareSize*(j+1), pos[1] - size/2, pos[2] - size/2 + self.squareSize*(i+1))),

                array_vertices.append((pos[0] - size/2 + self.squareSize*j,     pos[1] + size/2, pos[2] - size/2 + self.squareSize*i)), # positive y face
                array_vertices.append((pos[0] - size/2 + self.squareSize*(j+1), pos[1] + size/2, pos[2] - size/2 + self.squareSize*i)),
                array_vertices.append((pos[0] - size/2 + self.squareSize*j,     pos[1] + size/2, pos[2] - size/2 + self.squareSize*(i+1))),
                array_vertices.append((pos[0] - size/2 + self.squareSize*j,     pos[1] + size/2, pos[2] - size/2 + self.squareSize*(i+1))),
                array_vertices.append((pos[0] - size/2 + self.squareSize*(j+1), pos[1] + size/2, pos[2] - size/2 + self.squareSize*i)),
                array_vertices.append((pos[0] - size/2 + self.squareSize*(j+1), pos[1] + size/2, pos[2] - size/2 + self.squareSize*(i+1))),
            
        # Define the vertices of a block using 6 vertices per face
        return np.array(array_vertices, dtype=np.float32)
            
                

    def defineTexture(self, texture_indices):
        """
            Define the texture of the block. Default texture
        """

        textures = []
        size = 0.0625

        for i in range(self.nSquares):
            for j in range(self.nSquares):
                textures.append((texture_indices["front"][0] * size, texture_indices["front"][1] * size)),
                textures.append((texture_indices["front"][0] * size + size, texture_indices["front"][1] * size)),
                textures.append((texture_indices["front"][0] * size, texture_indices["front"][1] * size + size)),
                textures.append((texture_indices["front"][0] * size, texture_indices["front"][1] * size + size)),
                textures.append((texture_indices["front"][0] * size + size, texture_indices["front"][1] * size)),
                textures.append((texture_indices["front"][0] * size + size, texture_indices["front"][1] * size + size)),

                textures.append((texture_indices["left"][0] * size, texture_indices["left"][1] * size)),
                textures.append((texture_indices["left"][0] * size + size, texture_indices["left"][1] * size)),
                textures.append((texture_indices["left"][0] * size, texture_indices["left"][1] * size + size)),
                textures.append((texture_indices["left"][0] * size, texture_indices["left"][1] * size + size)),
                textures.append((texture_indices["left"][0] * size + size, texture_indices["left"][1] * size)),
                textures.append((texture_indices["left"][0] * size + size, texture_indices["left"][1] * size + size)),
                
                textures.append((texture_indices["back"][0] * size, texture_indices["back"][1] * size)),
                textures.append((texture_indices["back"][0] * size + size, texture_indices["back"][1] * size)),
                textures.append((texture_indices["back"][0] * size, texture_indices["back"][1] * size + size)),
                textures.append((texture_indices["back"][0] * size, texture_indices["back"][1] * size + size)),
                textures.append((texture_indices["back"][0] * size + size, texture_indices["back"][1] * size)),
                textures.append((texture_indices["back"][0] * size + size, texture_indices["back"][1] * size + size)),

                textures.append((texture_indices["right"][0] * size, texture_indices["right"][1] * size)),
                textures.append((texture_indices["right"][0] * size + size, texture_indices["right"][1] * size)),
                textures.append((texture_indices["right"][0] * size, texture_indices["right"][1] * size + size)),
                textures.append((texture_indices["right"][0] * size, texture_indices["right"][1] * size + size)),
                textures.append((texture_indices["right"][0] * size + size, texture_indices["right"][1] * size)),
                textures.append((texture_indices["right"][0] * size + size, texture_indices["right"][1] * size + size)),
                
                textures.append((texture_indices["bottom"][0] * size, texture_indices["bottom"][1] * size)),
                textures.append((texture_indices["bottom"][0] * size + size, texture_indices["bottom"][1] * size)),
                textures.append((texture_indices["bottom"][0] * size, texture_indices["bottom"][1] * size + size)),
                textures.append((texture_indices["bottom"][0] * size, texture_indices["bottom"][1] * size + size)),
                textures.append((texture_indices["bottom"][0] * size + size, texture_indices["bottom"][1] * size)),
                textures.append((texture_indices["bottom"][0] * size + size, texture_indices["bottom"][1] * size + size)),
                
                textures.append((texture_indices["top"][0] * size, texture_indices["top"][1] * size)),
                textures.append((texture_indices["top"][0] * size + size, texture_indices["top"][1] * size)),
                textures.append((texture_indices["top"][0] * size, texture_indices["top"][1] * size + size)),
                textures.append((texture_indices["top"][0] * size, texture_indices["top"][1] * size + size)),
                textures.append((texture_indices["top"][0] * size + size, texture_indices["top"][1] * size)),
                textures.append((texture_indices["top"][0] * size + size, texture_indices["top"][1] * size + size))
        # Define the texture of a block using 6 vertices per face
        return np.array(textures, dtype=np.float32)

    def defineNormals(self):
        """
            Defines the normals of the block
        """
        norms = []
        for i in range(self.nSquares):
            for j in range(self.nSquares):
                norms.append((0.0, 0.0, 1.0)),
                norms.append((0.0, 0.0, 1.0)),
                norms.append((0.0, 0.0, 1.0)),
                norms.append((0.0, 0.0, 1.0)),
                norms.append((0.0, 0.0, 1.0)),
                norms.append((0.0, 0.0, 1.0)),

                norms.append((1.0, 0.0, 0.0)),
                norms.append((1.0, 0.0, 0.0)),
                norms.append((1.0, 0.0, 0.0)),
                norms.append((1.0, 0.0, 0.0)),
                norms.append((1.0, 0.0, 0.0)),
                norms.append((1.0, 0.0, 0.0)),

                norms.append((0.0, 0.0, -1.0)),
                norms.append((0.0, 0.0, -1.0)),
                norms.append((0.0, 0.0, -1.0)),
                norms.append((0.0, 0.0, -1.0)),
                norms.append((0.0, 0.0, -1.0)),
                norms.append((0.0, 0.0, -1.0)),

                norms.append((-1.0, 0.0, 0.0)),
                norms.append((-1.0, 0.0, 0.0)),
                norms.append((-1.0, 0.0, 0.0)),
                norms.append((-1.0, 0.0, 0.0)),
                norms.append((-1.0, 0.0, 0.0)),
                norms.append((-1.0, 0.0, 0.0)),

                norms.append((0.0, -1.0, 0.0)),
                norms.append((0.0, -1.0, 0.0)),
                norms.append((0.0, -1.0, 0.0)),
                norms.append((0.0, -1.0, 0.0)),
                norms.append((0.0, -1.0, 0.0)),
                norms.append((0.0, -1.0, 0.0)),

                norms.append((0.0, 1.0, 0.0)),
                norms.append((0.0, 1.0, 0.0)),
                norms.append((0.0, 1.0, 0.0)),
                norms.append((0.0, 1.0, 0.0)),
                norms.append((0.0, 1.0, 0.0)),
                norms.append((0.0, 1.0, 0.0))

        return np.array(norms, dtype=np.float32)
    

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


    def draw(self, program, view, proj, light_theta):

        modelTemp = glm.rotate(glm.mat4(1.0), light_theta, (0, 1, 0) )
        model = glm.rotate(modelTemp, glm.radians(45.0), glm.vec3(1,0,0))
        
        loc_model = glGetUniformLocation(program, "model")
        model_array = np.array(model, dtype=np.float32)
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, model_array)

        loc_view = glGetUniformLocation(program, "view")
        view_array = np.array(view, dtype=np.float32)
        glUniformMatrix4fv(loc_view, 1, GL_TRUE, view_array)

        loc_projection = glGetUniformLocation(program, "projection")
        projection_array = np.array(proj, dtype=np.float32)
        glUniformMatrix4fv(loc_projection, 1, GL_TRUE, projection_array)

        self.setVerticesAndTexture(program)

        glDrawArrays(GL_TRIANGLES, 0, self.nSquares*self.nSquares*36)
