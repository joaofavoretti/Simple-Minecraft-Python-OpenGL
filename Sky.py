import glfw
import glm
from OpenGL.GL import *
import numpy as np
from Block import Block

class Sky (Block):
    
    def __init__(self, pos):

        self.texture_indices = {
            "top": (5, 1),
            "bottom": (5, 1),
            "left": (5, 1),
            "right": (5, 1),
            "front": (5, 1),
            "back": (5, 1),
        }

        self.size = 180
        self.nSquares = 20
        self.squareSize = self.size / self.nSquares
        
        super().__init__(pos)


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


    def draw(self, program, view, proj):
        
        loc_model = glGetUniformLocation(program, "model")
        model_array = np.array(self.model, dtype=np.float32)
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, model_array)

        loc_view = glGetUniformLocation(program, "view")
        view_array = np.array(view, dtype=np.float32)
        glUniformMatrix4fv(loc_view, 1, GL_TRUE, view_array)

        loc_projection = glGetUniformLocation(program, "projection")
        projection_array = np.array(proj, dtype=np.float32)
        glUniformMatrix4fv(loc_projection, 1, GL_TRUE, projection_array)

        for index in range(self.nSquares*self.nSquares):
            glDrawArrays(GL_TRIANGLES, self.block_index * self.nSquares*self.nSquares + index*6, 6)

        
    

    

    