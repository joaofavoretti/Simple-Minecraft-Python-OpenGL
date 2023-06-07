import glfw
import glm
from OpenGL.GL import *
import numpy as np

from Chunk import Chunk

class World:
    def __init__(self):
        """
            Initialize the world
        """

        self.chunks = self.defineChunks()

    def defineChunks(self):
        """
            Define the chunks of the world
        """
        chunks = []
        last_vertice_index = 0
        for x in range(1):
            for z in range(1):
                c = Chunk((x, z))
                c.setVerticeIndex(last_vertice_index)
                last_vertice_index = c.getLastVerticeIndex()
                chunks.append(c)
        return chunks
    
    def getVertices(self):
        """
            Get the vertices of the world
        """
        vertices = np.empty((0, 3), dtype=np.float32)
        for chunk in self.chunks:
            vertices = np.vstack((vertices, chunk.getVertices()))
        return vertices
    
    def getTexture(self):
        """
            Get the texture of the world
        """
        texture = np.empty((0, 2), dtype=np.float32)
        for chunk in self.chunks:
            texture = np.vstack((texture, chunk.getTexture()))
        return texture
    
    def draw(self, program, camera):
        """
            Draw the world
        """
        for chunk in self.chunks:
            chunk.draw(program, camera)

