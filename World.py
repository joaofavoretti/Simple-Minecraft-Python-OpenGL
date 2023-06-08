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
    
        self.sendVerticesAndTexture(self.program)

    def defineChunks(self, central_chunk_coord):
        """
            Define the chunks of the world
        """
        chunks = []
        last_vertice_index = 0
        central_chunk_x, central_chunk_z = central_chunk_coord
        for x in range(-1, 1):
            for z in range(-1, 1):
                c = Chunk((central_chunk_x + x, central_chunk_z + z))
                c.setVerticeIndex(last_vertice_index)
                last_vertice_index = c.getLastVerticeIndex()
                chunks.append(c)
        return chunks
    
    def sendVerticesAndTexture(self, program):
        """
            Send the vertices to the GPU

            program(OpenGL.GL.shaders.ShaderProgram) - Shader program
            vertices(numpy.ndarray) - Vertices to be sent to the GPU
            texture(numpy.ndarray) - Texture to be sent to the GPU
        """

        # TODO: Testar usar o comando glGenBuffers 2 vezes (Para separar essa funcao em duas. sendVertices() e sendTexture())

        if not hasattr(self, 'buffer'):
            self.vertice_buffer, self.texture_buffer = glGenBuffers(2)
        
        vertices = self.getVertices()
        texture = self.getTexture()

        # Vertices
        glBindBuffer(GL_ARRAY_BUFFER, self.vertice_buffer)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        loc = glGetAttribLocation(program, "position")
        glEnableVertexAttribArray(loc)

        stride = vertices.strides[0]
        offset = ctypes.c_void_p(0)

        glVertexAttribPointer(loc, 3, GL_FLOAT, False, stride, offset)

        # Texture
        glBindBuffer(GL_ARRAY_BUFFER, self.texture_buffer)
        glBufferData(GL_ARRAY_BUFFER, texture.nbytes, texture, GL_STATIC_DRAW)

        loc = glGetAttribLocation(program, "texture")
        glEnableVertexAttribArray(loc)

        stride = texture.strides[0]
        offset = ctypes.c_void_p(0)

        glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride, offset)

    def reDefineChunks(self, central_chunk_coord):
        """
            Re-define the chunks of the world using the near chunks that are already defined
        """
        new_chunks = []
        last_vertice_index = 0
        for chunk in self.chunks:
            if chunk.isNear(central_chunk_coord):
                new_chunks.append(chunk)
                chunk.setVerticeIndex(last_vertice_index)
                last_vertice_index = chunk.getLastVerticeIndex()
        
        central_chunk_x, central_chunk_z = central_chunk_coord
        for x in range(-1, 1):
            for z in range(-1, 1):
                if not self.isChunkDefined(new_chunks, (central_chunk_x + x, central_chunk_z + z)):
                    c = Chunk((central_chunk_x + x, central_chunk_z + z))
                    c.setVerticeIndex(last_vertice_index)
                    last_vertice_index = c.getLastVerticeIndex()
                    new_chunks.append(c)

        return new_chunks

    def isChunkDefined(self, chunks, chunk_coord):
        """
            Check if the chunk is already defined
        """
        for chunk in chunks:
            if chunk.getPosition() == chunk_coord:
                return True
        return False

    def updateChunks(self, new_central_chunk_coord):
        self.central_chunk_coord = new_central_chunk_coord

        self.chunks = self.reDefineChunks(self.central_chunk_coord)
    
        self.sendVerticesAndTexture(self.program)


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

