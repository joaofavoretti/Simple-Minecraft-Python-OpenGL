from OpenGL.GL import *
import numpy as np
import os
import pickle
from perlin_noise import PerlinNoise

from block_bind import BLOCK_BIND

from Grass import Grass
from Dirt import Dirt
from Stone import Stone

CHUNK_DB_DIR = os.path.join(os.getcwd(), 'db')

CHUNK_X_LENGTH = 16
CHUNK_Y_LENGTH = 16
CHUNK_Z_LENGTH = 16

class Chunk:
    def __init__ (self, chunk_coord):
        """
            Initialize the chunk centered at (x, y)

            Pos(glm.vec2) - Position of the chunk in the space. Must be integers, otherwise can cause interpolation problems.

        """

        self.chunk_coord = chunk_coord

        self.blocks = self.defineBlocks(self.chunk_coord)

    def defineBlocks(self, chunk_coord):
        """
            World generation function
        """

        blocks = None

        chunk_path = Chunk.getChunkPath(chunk_coord)

        if os.path.isfile(chunk_path):
            blocks = self.loadBlocks(chunk_path)
        else:
            blocks = Chunk.generateBlocks(chunk_coord)  
            Chunk.saveBlocks(chunk_path, blocks)          

        return blocks

    @staticmethod
    def generateBlocks(chunk_coord):
        blocks = {}

        chunk_coord_x, chunk_coord_z = chunk_coord
        chunk_coord_y = 0

        noise = PerlinNoise(octaves=4, seed=hash(str(chunk_coord)))
    
        for x in range(CHUNK_X_LENGTH):
            for z in range(CHUNK_Z_LENGTH):
                height = int(noise([x / 50.0, z / 50.0]) * 5 + 2) + CHUNK_Y_LENGTH

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
    
    @staticmethod
    def getChunkPath(chunk_coord):
        """
            Get the path of the chunk file
        """

        return os.path.join(CHUNK_DB_DIR, f"chunk_{chunk_coord[0]}_{chunk_coord[1]}.pkl")

    @staticmethod
    def saveBlocks(chunk_path, blocks):
        """
            Save the blocks in a file
            Format pickle
        """

        # Create all the directories if they don't exist
        os.makedirs(os.path.dirname(chunk_path), exist_ok=True)

        with open(chunk_path, 'wb') as f:
            pickle.dump(blocks, f)
            
    
    @staticmethod
    def generateChunkFile(chunk_coord):

        chunk_path = Chunk.getChunkPath(chunk_coord)
        if os.path.isfile(chunk_path):
            return
        
        blocks = Chunk.generateBlocks(chunk_coord)
        Chunk.saveBlocks(chunk_path, blocks)

    def loadBlocks(self, chunk_path):
        """
            Load the blocks from a file
            Format pickle
        """
            
        with open(chunk_path, 'rb') as f:
            blocks = pickle.load(f)
        
        return blocks
        
    

    def getLenBlocks(self):
        return len(self.blocks)

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
