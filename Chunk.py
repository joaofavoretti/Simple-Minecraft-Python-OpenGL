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
        self.hasTree = pos[0] % 2 == 0 and pos[1] % 2 == 0
        self.hasHouse = pos[0] % 5 == 0 and pos[1] % 5 == 0 and pos[0] % 2 == 1

        self.chunk_vertice_index = 0

        self.noise = PerlinNoise(octaves=4, seed=hash(str(self.pos)))

        self.blocks = self.defineBlocks()
        self.update()

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
                    elif y == height - 2:
                        blocks[(x,y,z)] = Dirt((chunk_pos_x * 16 + x, chunk_pos_y + y, chunk_pos_z * 16 + z))
                    else:
                        blocks[(x,y,z)] = Stone((chunk_pos_x * 16 + x, chunk_pos_y + y, chunk_pos_z * 16 + z))

                
        if self.hasTree:
            height = int(self.noise([1 / 50.0, 1 / 50.0]) * 5 + 2) + 1
            for h in range(3):
                blocks[(1,height + h,1)] = Wood((chunk_pos_x * 16 + 1, chunk_pos_y + height + h, chunk_pos_z * 16 + 1))

            for i in range(3):
                for j in range(3):
                    blocks[(i, height + 3, j)] = Leaves((chunk_pos_x * 16 + i, chunk_pos_y + height + 3, chunk_pos_z * 16 + j))
                    if i == 1 or j == 1:
                        blocks[(i, height + 4, j)] = Leaves((chunk_pos_x * 16 + i, chunk_pos_y + height + 4, chunk_pos_z * 16 + j))
                 
                    if i == 1 and j == 1:
                        blocks[(i, height + 5, j)] = Leaves((chunk_pos_x * 16 + i, chunk_pos_y + height + 5, chunk_pos_z * 16 + j))
         
        if self.hasHouse:
            height = int(self.noise([1 / 50.0, 1 / 50.0]) * 5 + 2) + 1
            for i in range(5):
                for j in range(5):
                    blocks[(i, height - 1, j)] = Stone((chunk_pos_x * 16 + i, chunk_pos_y + height - 1, chunk_pos_z * 16 + j))
                    blocks[(i, height + 5, j)] = Stone((chunk_pos_x * 16 + i, chunk_pos_y + height + 5, chunk_pos_z * 16 + j))
                    if i == 0 or j == 0 or i == 4 or j == 4:
                        for h in range(5):
                            if i == 2 and j == 0 and (h == 0 or h == 1):
                                continue
                            blocks[(i, height + h, j)] = Stone((chunk_pos_x * 16 + i, chunk_pos_y + height + h, chunk_pos_z * 16 + j))
                    
            blocks[(1, height, 3)] = Dirt((chunk_pos_x * 16 + 1, chunk_pos_y + height, chunk_pos_z * 16 + 3))
            blocks[(2, height, 3)] = Dirt((chunk_pos_x * 16 + 2, chunk_pos_y + height, chunk_pos_z * 16 + 3))
            blocks[(3, height, 3)] = Dirt((chunk_pos_x * 16 + 3, chunk_pos_y + height, chunk_pos_z * 16 + 3))
            blocks[(1, height + 1, 3)] = Dirt((chunk_pos_x * 16 + 1, chunk_pos_y + height + 1, chunk_pos_z * 16 + 3))

        return blocks

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
        return abs(central_chunk_x - chunk_x) <= 5 and abs(central_chunk_z - chunk_z) <= 5

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
    
    def update(self):
        self.vertices = self.getVertices()
        self.texture = self.getTexture()
        self.normals = self.getNormals()
 
    def setVerticesAndTexture(self, program):
        if not hasattr(self, 'vertice_buffer'):
            self.vertice_buffer, self.texture_buffer, self.normal_buffer = glGenBuffers(3)
        
        # Vertices
        glBindBuffer(GL_ARRAY_BUFFER, self.vertice_buffer)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        loc = glGetAttribLocation(program, "position")
        glEnableVertexAttribArray(loc)

        stride = self.vertices.strides[0]
        offset = ctypes.c_void_p(0)

        glVertexAttribPointer(loc, 3, GL_FLOAT, False, stride, offset)

        # Texture
        glBindBuffer(GL_ARRAY_BUFFER, self.texture_buffer)
        glBufferData(GL_ARRAY_BUFFER, self.texture.nbytes, self.texture, GL_STATIC_DRAW)

        loc = glGetAttribLocation(program, "texture")
        glEnableVertexAttribArray(loc)

        stride = self.texture.strides[0]
        offset = ctypes.c_void_p(0)

        glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride, offset)
        
        # Normals
        glBindBuffer(GL_ARRAY_BUFFER, self.normal_buffer)
        glBufferData(GL_ARRAY_BUFFER, self.normals.nbytes, self.normals, GL_STATIC_DRAW)

        loc = glGetAttribLocation(program, "normal")
        glEnableVertexAttribArray(loc)

        stride = self.normals.strides[0]
        offset = ctypes.c_void_p(0)

        glVertexAttribPointer(loc, 3, GL_FLOAT, False, stride, offset)

    def draw(self, program, camera):
        """
            Draw the chunk
        """
        loc_model = glGetUniformLocation(program, "model")
        model_array = np.array(glm.mat4(1.0), dtype=np.float32)
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, model_array)

        loc_view = glGetUniformLocation(program, "view")
        view_array = np.array(camera.view, dtype=np.float32)
        glUniformMatrix4fv(loc_view, 1, GL_TRUE, view_array)

        self.setVerticesAndTexture(program)
        glDrawArrays(GL_QUADS, 0, 24 * len(self.blocks))


