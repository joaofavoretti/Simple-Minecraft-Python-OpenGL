import glfw
import glm
from OpenGL.GL import *
import numpy as np

class Block:
    def __init__ (self, block_coord):
        """
            Initialize the block centered at (x, y, z)

            block_coord(glm.vec3) - Position of the block in the space. Must be integers, otherwise can cause interpolation problems.
        """

        self.size = 1.0

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

        self.vertices = self.defineVertices(block_coord, self.size)

        self.texture = self.defineTexture(self.texture_indices)

        self.model = glm.mat4(1.0)

    # TODO: Use a block.obj file to define the vertices
    def defineVertices(self, block_coord, size):
        """
            Define the vertices of the block

            block_coord(tuple(float, float, float)) - Position of the block in the world
            size(float) - Size of the block
        """
        # Define the vertices of a block using 6 vertices per face
        return np.array([

            (block_coord[0] - size/2, block_coord[1] - size/2, block_coord[2] + size/2),
            (block_coord[0] + size/2, block_coord[1] - size/2, block_coord[2] + size/2),
            (block_coord[0] + size/2, block_coord[1] + size/2, block_coord[2] + size/2),
            (block_coord[0] - size/2, block_coord[1] + size/2, block_coord[2] + size/2),

            (block_coord[0] + size/2, block_coord[1] - size/2, block_coord[2] + size/2),
            (block_coord[0] + size/2, block_coord[1] - size/2, block_coord[2] - size/2),
            (block_coord[0] + size/2, block_coord[1] + size/2, block_coord[2] - size/2),
            (block_coord[0] + size/2, block_coord[1] + size/2, block_coord[2] + size/2),

            (block_coord[0] + size/2, block_coord[1] - size/2, block_coord[2] - size/2),
            (block_coord[0] - size/2, block_coord[1] - size/2, block_coord[2] - size/2),
            (block_coord[0] - size/2, block_coord[1] + size/2, block_coord[2] - size/2),
            (block_coord[0] + size/2, block_coord[1] + size/2, block_coord[2] - size/2),

            (block_coord[0] - size/2, block_coord[1] - size/2, block_coord[2] - size/2),
            (block_coord[0] - size/2, block_coord[1] - size/2, block_coord[2] + size/2),
            (block_coord[0] - size/2, block_coord[1] + size/2, block_coord[2] + size/2),
            (block_coord[0] - size/2, block_coord[1] + size/2, block_coord[2] - size/2),

            (block_coord[0] - size/2, block_coord[1] - size/2, block_coord[2] - size/2),
            (block_coord[0] + size/2, block_coord[1] - size/2, block_coord[2] - size/2),
            (block_coord[0] + size/2, block_coord[1] - size/2, block_coord[2] + size/2),
            (block_coord[0] - size/2, block_coord[1] - size/2, block_coord[2] + size/2),

            (block_coord[0] - size/2, block_coord[1] + size/2, block_coord[2] + size/2),
            (block_coord[0] + size/2, block_coord[1] + size/2, block_coord[2] + size/2),
            (block_coord[0] + size/2, block_coord[1] + size/2, block_coord[2] - size/2),
            (block_coord[0] - size/2, block_coord[1] + size/2, block_coord[2] - size/2)
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

    def getType(self):
        """
            Return the type of the block
        """
        
        return self.type
