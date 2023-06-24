from OpenGL.GL import *
import numpy as np
import os
from perlin_noise import PerlinNoise

from block_bind import BLOCK_BIND

from Grass import Grass
from Dirt import Dirt
from Stone import Stone

CHUNK_DB_DIR = os.path.join(os.getcwd(), 'db')

class Chunk:
    def __init__ (self, chunk_coord):
        """
            Initialize the chunk centered at (x, y)

            Pos(glm.vec2) - Position of the chunk in the space. Must be integers, otherwise can cause interpolation problems.

        """

        self.x_length = 16
        self.y_length = 1
        self.z_length = 16

        self.chunk_coord = (chunk_coord[0], 0, chunk_coord[1])

        self.noise = PerlinNoise(octaves=4, seed=hash(str(self.chunk_coord)))

        self.blocks = self.defineBlocks(self.chunk_coord)

    def defineBlocks(self, chunk_coord):
        """
            World generation function
        """
        
        blocks = None

        chunk_fname = f"chunk_{chunk_coord[0]}_{chunk_coord[2]}"
        chunk_path = os.path.join(CHUNK_DB_DIR, chunk_fname)

        if os.path.isfile(chunk_path):
            blocks = self.loadBlocks(chunk_path)
        else:
            blocks = self.generateBlocks(chunk_coord)  
            self.saveBlocks(chunk_path, blocks)          

        return blocks

    def generateBlocks(self, chunk_coord):
        blocks = {}

        chunk_coord_x, chunk_coord_y, chunk_coord_z = chunk_coord
    
        for x in range(self.x_length):
            for z in range(self.z_length):
                height = int(self.noise([x / 50.0, z / 50.0]) * 5 + 2) + 1

                for y in range(height):
                    _x = chunk_coord_x * 16 + x
                    _y = chunk_coord_y + y
                    _z = chunk_coord_z * 16 + z
                    if y == height - 1:
                        blocks[(_x, _y, _z)] = Grass((_x, _y, _z))
                    elif y == height - 2:
                        blocks[(_x, _y, _z)] = Dirt((_x, _y, _z))
                    else:
                        blocks[(_x, _y, _z)] = Stone((_x, _y, _z))

        return blocks
    
    def saveBlocks(self, chunk_path, blocks):
        """
            Save the blocks in a file
            Format
            x y z type
        """

        # Create all the directories if they don't exist
        os.makedirs(os.path.dirname(chunk_path), exist_ok=True)

        with open(chunk_path, 'w') as f:
            for block in blocks:
                f.write(f"b {block[0]} {block[1]} {block[2]} {BLOCK_BIND.inverse[type(blocks[block])]}\n")
    
    def loadBlocks(self, chunk_path):
        """
            Load the blocks from a file
            Format
            x y z type
        """
        blocks = {}
        with open(chunk_path, 'r') as f:
            for line in f:
                if line.startswith('b'):
                    _, x, y, z, block_type = line.split()
                    x, y, z = int(x), int(y), int(z)
                    blocks[(x, y, z)] = BLOCK_BIND[block_type]((x, y, z))
        return blocks

    def getPosition(self):
        """
            Get the position of the chunk
        """

        return (self.chunk_coord[0], self.chunk_coord[2])

    def getLenBlocks(self):
        return len(self.blocks)

    def isNear(self, central_coord):
        """
            Check if the chunk is near the central chunk
        """
        central_chunk_x, central_chunk_z = central_coord
        chunk_x, chunk_z = self.chunk_coord[0], self.chunk_coord[2]
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
