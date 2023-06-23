import glfw
import glm
from OpenGL.GL import *
import numpy as np

class Block:
    def __init__ (self, pos):
        """
            Initialize the block centered at (x, y, z)

            pos(glm.vec3) - Position of the block in the space. Must be integers, otherwise can cause interpolation problems.
        """

        self.size = 1.0

        self.block_index = 0

        # if attribute texture_indices is not defined, define it
        if not hasattr(self, "texture_indices"):
            self.texture_indices = {
                "top": (0, 0),
                "bottom": (0, 0),
                "left": (0, 1),
                "right": (0, 1),
                "front": (0, 2),
                "back": (0, 2),
            }
        
        self.vertices = self.defineVertices(pos, self.size)

        self.texture = self.defineTexture(self.texture_indices)

        self.model = glm.mat4(1.0)

    # TODO: Use a block.obj file to define the vertices
    def defineVertices(self, pos, size):
        """
            Define the vertices of the block

            pos(tuple(float, float, float)) - Position of the block in the world
            size(float) - Size of the block
        """
        # Define the vertices of a block using 6 vertices per face
        return np.array([

            (pos[0] - size/2, pos[1] - size/2, pos[2] + size/2),
            (pos[0] + size/2, pos[1] - size/2, pos[2] + size/2),
            (pos[0] + size/2, pos[1] + size/2, pos[2] + size/2),
            (pos[0] - size/2, pos[1] + size/2, pos[2] + size/2),

            (pos[0] + size/2, pos[1] - size/2, pos[2] + size/2),
            (pos[0] + size/2, pos[1] - size/2, pos[2] - size/2),
            (pos[0] + size/2, pos[1] + size/2, pos[2] - size/2),
            (pos[0] + size/2, pos[1] + size/2, pos[2] + size/2),

            (pos[0] + size/2, pos[1] - size/2, pos[2] - size/2),
            (pos[0] - size/2, pos[1] - size/2, pos[2] - size/2),
            (pos[0] - size/2, pos[1] + size/2, pos[2] - size/2),
            (pos[0] + size/2, pos[1] + size/2, pos[2] - size/2),

            (pos[0] - size/2, pos[1] - size/2, pos[2] - size/2),
            (pos[0] - size/2, pos[1] - size/2, pos[2] + size/2),
            (pos[0] - size/2, pos[1] + size/2, pos[2] + size/2),
            (pos[0] - size/2, pos[1] + size/2, pos[2] - size/2),

            (pos[0] - size/2, pos[1] - size/2, pos[2] - size/2),
            (pos[0] + size/2, pos[1] - size/2, pos[2] - size/2),
            (pos[0] + size/2, pos[1] - size/2, pos[2] + size/2),
            (pos[0] - size/2, pos[1] - size/2, pos[2] + size/2),

            (pos[0] - size/2, pos[1] + size/2, pos[2] + size/2),
            (pos[0] + size/2, pos[1] + size/2, pos[2] + size/2),
            (pos[0] + size/2, pos[1] + size/2, pos[2] - size/2),
            (pos[0] - size/2, pos[1] + size/2, pos[2] - size/2)
        ], dtype=np.float32)
        
            

    def defineTexture(self, texture_indices):
        """
            Define the texture of the block. Default texture
        """

        size = 0.0625

        # Define the texture of a block using 6 vertices per face
        return np.array([
            (texture_indices["front"][0] * size, texture_indices["front"][1] * size),
            (texture_indices["front"][0] * size + size, texture_indices["front"][1] * size),
            (texture_indices["front"][0] * size + size, texture_indices["front"][1] * size + size),
            (texture_indices["front"][0] * size, texture_indices["front"][1] * size + size),

            (texture_indices["left"][0] * size, texture_indices["left"][1] * size),
            (texture_indices["left"][0] * size + size, texture_indices["left"][1] * size),
            (texture_indices["left"][0] * size + size, texture_indices["left"][1] * size + size),
            (texture_indices["left"][0] * size, texture_indices["left"][1] * size + size),
            
            (texture_indices["back"][0] * size, texture_indices["back"][1] * size),
            (texture_indices["back"][0] * size + size, texture_indices["back"][1] * size),
            (texture_indices["back"][0] * size + size, texture_indices["back"][1] * size + size),
            (texture_indices["back"][0] * size, texture_indices["back"][1] * size + size),

            (texture_indices["right"][0] * size, texture_indices["right"][1] * size),
            (texture_indices["right"][0] * size + size, texture_indices["right"][1] * size),
            (texture_indices["right"][0] * size + size, texture_indices["right"][1] * size + size),
            (texture_indices["right"][0] * size, texture_indices["right"][1] * size + size),
            
            (texture_indices["bottom"][0] * size, texture_indices["bottom"][1] * size),
            (texture_indices["bottom"][0] * size + size, texture_indices["bottom"][1] * size),
            (texture_indices["bottom"][0] * size + size, texture_indices["bottom"][1] * size + size),
            (texture_indices["bottom"][0] * size, texture_indices["bottom"][1] * size + size),
            
            (texture_indices["top"][0] * size, texture_indices["top"][1] * size),
            (texture_indices["top"][0] * size + size, texture_indices["top"][1] * size),
            (texture_indices["top"][0] * size + size, texture_indices["top"][1] * size + size),
            (texture_indices["top"][0] * size, texture_indices["top"][1] * size + size)
        ], dtype=np.float32)

    def setVerticeIndex(self, index):
        """
            Set the block index
        """

        self.block_index = index

    def getVertices(self):
        """
            Return the vertices of the block
        """
        
        return self.vertices

    def getTexture(self):
        """
            Return the texture of the block
        """
        
        return self.texture

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

        for face in range(6):
            glDrawArrays(GL_TRIANGLES, self.block_index * 36 + face * 6, 6)
            
