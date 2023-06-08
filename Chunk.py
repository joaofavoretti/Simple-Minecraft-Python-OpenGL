import glfw
import glm
from OpenGL.GL import *
import numpy as np

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

        self.chunk_vertice_index = 0

        self.blocks = self.defineBlocks()

    def defineBlocks(self):
        """
            World generation function
        """
        blocks = []

        chunk_pos_x, chunk_pos_y, chunk_pos_z = self.pos

        for x in range(self.x_length):
            for z in range(self.z_length):
                blocks.append(Dirt((chunk_pos_x * 16 + x, chunk_pos_y + z, chunk_pos_z * 16 + z)))
                blocks[-1].setVerticeIndex(self.chunk_vertice_index + len(blocks) - 1)

                blocks.append(Grass((chunk_pos_x * 16 + x, chunk_pos_y + z + 1, chunk_pos_z * 16 + z)))
                blocks[-1].setVerticeIndex(self.chunk_vertice_index + len(blocks) - 1)
        return blocks

    def setVerticeIndex(self, index):
        """
            Set the vertice index of the chunk
        """
        self.chunk_vertice_index = index

        # Update block vertice index
        for i, block in enumerate(self.blocks):
            block.setVerticeIndex(self.chunk_vertice_index + i)

    def getLastVerticeIndex(self):
        """
            Get the vertice index of the chunk
        """

        return self.chunk_vertice_index + len(self.blocks)

    def getPosition(self):
        """
            Get the position of the chunk
        """

        return (self.pos[0], self.pos[2])

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
            vertices = np.vstack((vertices, block.getVertices()))
        return vertices
    
    def getTexture(self):
        """
            Get the texture of the chunk
        """
        texture = np.empty((0, 2), dtype=np.float32)
        for block in self.blocks:
            texture = np.vstack((texture, block.getTexture()))
        return texture
    
    def draw(self, program, camera):
        """
            Draw the chunk
        """
        for block in self.blocks:
            block.draw(program, camera.view, camera.proj)