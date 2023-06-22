import glfw
import glm
from OpenGL.GL import *
import numpy as np
from perlin_noise import PerlinNoise

from Block import Block
from Grass import Grass
from Dirt import Dirt
from Stone import Stone
from Leaves import Leaves
from Wood import Wood

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
                    if y == height - 1:
                        blocks[(x,y,z)] = Grass((chunk_pos_x * 16 + x, chunk_pos_y + y, chunk_pos_z * 16 + z))
                        blocks[(x,y,z)].setVerticeIndex(self.chunk_vertice_index + len(blocks) - 1)
                    elif y == height - 2:
                        blocks[(x,y,z)] = Dirt((chunk_pos_x * 16 + x, chunk_pos_y + y, chunk_pos_z * 16 + z))
                        blocks[(x,y,z)].setVerticeIndex(self.chunk_vertice_index + len(blocks) - 1)
                    else:
                        blocks[(x,y,z)] = Stone((chunk_pos_x * 16 + x, chunk_pos_y + y, chunk_pos_z * 16 + z))
                        blocks[(x,y,z)].setVerticeIndex(self.chunk_vertice_index + len(blocks) - 1)

                
                if x == 0 and z == 0:
                    print("ZERO NO CHUNK", chunk_pos_x, chunk_pos_z)
                    for h in range(3):
                        blocks[(x,height + h,z)] = Wood((chunk_pos_x * 16, chunk_pos_y + height + h, chunk_pos_z * 16))
                        blocks[(x,height + h,z)].setVerticeIndex(self.chunk_vertice_index + len(blocks) - 1)
                    
                    for i in range(-1,2):
                        for j in range(-1,2):
                            blocks[(i, height + 3, j)] = Leaves((chunk_pos_x * 16 + i, chunk_pos_y + height + 3, chunk_pos_z * 16 + j))
                            
                            if i == 0 or j == 0:
                                blocks[(i, height + 4, j)] = Leaves((chunk_pos_x * 16 + i, chunk_pos_y + height + 4, chunk_pos_z * 16 + j))
                        
                            if i == 0 and j == 0:
                                blocks[(i, height + 5, j)] = Leaves((chunk_pos_x * 16 + i, chunk_pos_y + height + 5, chunk_pos_z * 16 + j))

        return blocks

    def setVerticeIndex(self, index):
        """
            Set the vertice index of the chunk
        """
        self.chunk_vertice_index = index

        # Update block vertice index
        for i, block in enumerate(self.blocks.values()):
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
        vertices = np.empty((0, 3), dtype=np.float16)
        for block in self.blocks.values():
            vertices = np.vstack((vertices, block.getVertices()))
        return vertices
    
    def getTexture(self):
        """
            Get the texture of the chunk
        """
        texture = np.empty((0, 2), dtype=np.float16)
        for block in self.blocks.values():
            texture = np.vstack((texture, block.getTexture()))
        return texture
 
    def getNormals(self):
        """
            Get the normals of the chunk
        """
        normals = np.empty((0, 3), dtype=np.float16)
        for block in self.blocks.values():
            normals = np.vstack((normals, block.getNormals()))
        return normals
 

    def draw(self, program, camera):
        """
            Draw the chunk
        """
        for block in self.blocks.values():
            block.draw(program, camera.view, camera.proj)
