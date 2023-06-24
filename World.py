import glfw
import glm
from OpenGL.GL import *
import numpy as np

from Chunk import Chunk

class World:
    def __init__(self, program):
        """
            Initialize the world
        """


        self.program = program

        self.central_chunk_coord = (0, 0)

        self.chunks = self.defineChunks(self.central_chunk_coord)

        self.sendVertices(self.program)
        self.sendTextures(self.program)

    def defineChunks(self, central_chunk_coord):
        """
            Define the chunks of the world
        """
        chunks = {}
        central_chunk_x, central_chunk_z = central_chunk_coord
        for x in range(-2, 2):
            for z in range(-2, 2):
                _x = central_chunk_x + x
                _y = 0
                _z = central_chunk_z + z

                chunks[(_x, _y, _z)] = Chunk((_x, _z))

        return chunks
    
    def sendVertices(self, program):
        """
            Send the vertices to the GPU

            program(OpenGL.GL.shaders.ShaderProgram) - Shader program
            vertices(numpy.ndarray) - Vertices to be sent to the GPU
        """

        if not hasattr(self, 'vertice_buffer'):
            self.vertice_buffer = glGenBuffers(1)
        
        vertices = self.getVertices()

        glBindBuffer(GL_ARRAY_BUFFER, self.vertice_buffer)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        loc = glGetAttribLocation(program, "position")
        glEnableVertexAttribArray(loc)

        stride = vertices.strides[0]
        offset = ctypes.c_void_p(0)

        glVertexAttribPointer(loc, 3, GL_FLOAT, False, stride, offset)

    def sendTextures(self, program):
        """
            Send the texture to the GPU

            program(OpenGL.GL.shaders.ShaderProgram) - Shader program
            texture(numpy.ndarray) - Texture to be sent to the GPU
        """

        if not hasattr(self, 'texture_buffer'):
            self.texture_buffer = glGenBuffers(1)
        
        texture = self.getTexture()

        glBindBuffer(GL_ARRAY_BUFFER, self.texture_buffer)
        glBufferData(GL_ARRAY_BUFFER, texture.nbytes, texture, GL_STATIC_DRAW)

        loc = glGetAttribLocation(program, "texture")
        glEnableVertexAttribArray(loc)

        stride = texture.strides[0]
        offset = ctypes.c_void_p(0)

        glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride, offset)

    def updateDefinedChunks(self, central_chunk_coord):
        """
            Re-define the chunks of the world using the near chunks that are already defined
        """
        new_chunks = {}
        for chunk in self.chunks:
            if self.chunks[chunk].isNear(central_chunk_coord):
                new_chunks[chunk] = self.chunks[chunk]
        
        central_chunk_x, central_chunk_z = central_chunk_coord
        for x in range(-2, 2):
            for z in range(-2, 2):
                _x = central_chunk_x + x
                _y = 0
                _z = central_chunk_z + z

                if not (_x, _y, _z) in new_chunks:
                    new_chunks[(_x, _y, _z)] = Chunk((_x, _z))

        return new_chunks

    def updateChunks(self, new_central_chunk_coord):
        self.central_chunk_coord = new_central_chunk_coord

        self.chunks = self.updateDefinedChunks(self.central_chunk_coord)
    
        self.sendVertices(self.program)
        self.sendTextures(self.program)


    def getVertices(self):
        """
            Get the vertices of the world
        """
        vertices = np.empty((0, 3), dtype=np.float32)
        # Iterate through all the chunks in the chunks dictionary
        for chunk in self.chunks:
            # Get the vertices of the chunk
            chunk_vertices = self.chunks[chunk].getVertices()
            # Add the vertices of the chunk to the vertices array
            vertices = np.vstack((vertices, chunk_vertices))

        return vertices
    
    def getTexture(self):
        """
            Get the texture of the world
        """
        texture = np.empty((0, 2), dtype=np.float32)
        for chunk in self.chunks:
            texture = np.vstack((texture, self.chunks[chunk].getTexture()))
        return texture
    
    def getLenBlocks(self):
        """
            Get the number of blocks in the world
        """
        len_blocks = 0
        for chunk in self.chunks:
            len_blocks += self.chunks[chunk].getLenBlocks()
        return len_blocks

    def draw(self, program, camera):
        """
            Draw the world.

            Draw all the vertices at once to avoid multiple calls to the GPU.
            Optimization over readability.
        """

        loc_model = glGetUniformLocation(program, "model")
        model_array = np.array(glm.mat4(1.0), dtype=np.float32)
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, model_array)

        loc_view = glGetUniformLocation(program, "view")
        view_array = np.array(camera.view, dtype=np.float32)
        glUniformMatrix4fv(loc_view, 1, GL_TRUE, view_array)

        loc_projection = glGetUniformLocation(program, "projection")
        projection_array = np.array(camera.proj, dtype=np.float32)
        glUniformMatrix4fv(loc_projection, 1, GL_TRUE, projection_array)

        glDrawArrays(GL_QUADS, 0, self.getLenBlocks() * 24)


