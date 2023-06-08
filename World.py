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
        for x in range(-1, 1):
            for z in range(-1, 1):
                c = Chunk((x, z))
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

        # TODO: Testar usar o comando glGenBuffers 2 vezes (Para separar essa funcao em duas)

        buffer = glGenBuffers(2)
        
        vertices = self.getVertices()
        texture = self.getTexture()

        # Vertices
        glBindBuffer(GL_ARRAY_BUFFER, buffer[0])
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        loc = glGetAttribLocation(program, "position")
        glEnableVertexAttribArray(loc)

        stride = vertices.strides[0]
        offset = ctypes.c_void_p(0)

        glVertexAttribPointer(loc, 3, GL_FLOAT, False, stride, offset)

        # Texture
        glBindBuffer(GL_ARRAY_BUFFER, buffer[1])
        glBufferData(GL_ARRAY_BUFFER, texture.nbytes, texture, GL_STATIC_DRAW)

        loc = glGetAttribLocation(program, "texture")
        glEnableVertexAttribArray(loc)

        stride = texture.strides[0]
        offset = ctypes.c_void_p(0)

        glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride, offset)

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

