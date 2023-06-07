import glfw
import glm
from OpenGL.GL import *
import numpy as np

from Block import Block
from Grass import Grass

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
            Define the blocks of the chunk
        """
        blocks = []
        chunk_pos_x, chunk_pos_y, chunk_pos_z = self.pos
        for y in range(self.y_length):
            for x in range(self.x_length):
                for z in range(self.z_length):
                    blocks.append(Grass((chunk_pos_x * 16 + x, chunk_pos_y + y, chunk_pos_z * 16 + z)))
                    blocks[-1].setVerticeIndex(y * self.x_length * self.z_length + x * self.z_length + z)
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