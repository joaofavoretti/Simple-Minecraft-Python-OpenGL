import glfw
import glm
from OpenGL.GL import *
import numpy as np
from perlin_noise import PerlinNoise

from Block import Block
from Grass import Grass
from Dirt import Dirt
from Stone import Stone

VERTICES_PER_BLOCK = 24

class Chunk:
    def __init__ (self, pos):
        """
            Initialize the chunk centered at (x, y)

            Pos(glm.vec2) - Position of the chunk in the space. Must be integers, otherwise can cause interpolation problems.

        """

        self.x_length = 16
        self.y_length = 1
        self.z_length = 16

        self.pos = (pos[0], 0, pos[1])

        self.noise = PerlinNoise(octaves=4, seed=hash(str(self.pos)))

        self.blocks = self.defineBlocks()

    def defineBlocks(self):
        """
            World generation function
        """
        blocks = {}

        chunk_pos_x, chunk_pos_y, chunk_pos_z = self.pos

        for x in range(self.x_length):
            for z in range(self.z_length):
                height = int(self.noise([x / 50.0, z / 50.0]) * 5 + 2) + 1

                for y in range(height):
                    _x = chunk_pos_x * 16 + x
                    _y = chunk_pos_y + y
                    _z = chunk_pos_z * 16 + z
                    if y == height - 1:
                        blocks[(_x, _y, _z)] = Grass((_x, _y, _z))
                    elif y == height - 2:
                        blocks[(_x, _y, _z)] = Dirt((_x, _y, _z))
                    else:
                        blocks[(_x, _y, _z)] = Stone((_x, _y, _z))
                        

        return blocks

    def getPosition(self):
        """
            Get the position of the chunk
        """

        return (self.pos[0], self.pos[2])

    def getLenBlocks(self):
        return len(self.blocks)

    def isNear(self, central_coord):
        """
            Check if the chunk is near the central chunk
        """
        central_chunk_x, central_chunk_z = central_coord
        chunk_x, chunk_z = self.pos[0], self.pos[2]
        return abs(central_chunk_x - chunk_x) <= 1 and abs(central_chunk_z - chunk_z) <= 1

    def getVertices(self):
        """
            Get the vertices of the chunk
        """
        vertices = np.empty((0, 3), dtype=np.float32)
        for block in self.blocks:
            vertices = np.vstack((vertices, self.blocks[block].getVertices()))
        return vertices
    
    def getTexture(self):
        """
            Get the texture of the chunk
        """
        texture = np.empty((0, 2), dtype=np.float32)
        for block in self.blocks:
            texture = np.vstack((texture, self.blocks[block].getTexture()))
        return texture
