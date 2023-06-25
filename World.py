import glfw
import glm
from OpenGL.GL import *
import numpy as np
import os
import multiprocessing
import threading

from Chunk import Chunk

CHUNK_DELTA = 3

class World:
    def __init__(self, program):
        """
            Initialize the world
        """


        self.program = program

        self.central_chunk_coord = (0, 0)

        self.chunks = {}
        self.chunk_vertices = {}
        self.chunk_textures = {}

        self.vertice_buffer = None
        self.texture_buffer = None

        self.vertices = np.empty((0, 3), dtype=np.float32)
        self.textures = np.empty((0, 2), dtype=np.float32)
        self.lenVertices = 0

        self.worldGeneratioProcess, \
        self.worldGenerationRequestQueue, \
        self.worldGenerationResponseQueue = World.initializeWorldGenerationProcess()

        self.updateBuffersProcess, \
        self.updateBuffersRequestQueue, \
        self.updateBuffersResponseQueue = World.initializeUpdateBuffersProcess()

        chunk_coord_set = World.getNearestChunks(self.central_chunk_coord)
        self.parallelGenerateChunkFiles(chunk_coord_set)

    def __del__(self):
        """
            Delete the world
        """

        self.worldGeneratioProcess.terminate()
        self.updateBuffersProcess.terminate()

    @staticmethod
    def getNearestChunks(central_chunk_coord):
        """
            Get the nearest chunks to the central chunk

            central_chunk_coord(tuple) - Central chunk coordinate
        """
        chunk_coord_set = set()

        central_chunk_x, central_chunk_z = central_chunk_coord
        for x in range(-CHUNK_DELTA, CHUNK_DELTA):
            for z in range(-CHUNK_DELTA, CHUNK_DELTA):
                _x = central_chunk_x + x
                _z = central_chunk_z + z

                chunk_coord_set.add((_x, _z))
        
        return chunk_coord_set

    @staticmethod
    def generateChunkFiles(worldGenerationRequestQueue, worldGenerationResponseQueue):
        """
            Generate the chunks

            chunk_coord_set(list) - List of chunk coordinates
        """

        while True:
            chunk_coord = worldGenerationRequestQueue.get(block=True)

            chunk = Chunk(chunk_coord)
            chunk_vertices = chunk.getVertices()
            chunk_textures = chunk.getTexture()
            
            worldGenerationResponseQueue.put((chunk_coord, chunk, chunk_vertices, chunk_textures))

    @staticmethod
    def initializeWorldGenerationProcess():
        """
            Initialize the world generation process
        """

        worldGenerationRequestQueue = multiprocessing.Queue()
        worldGenerationResponseQueue = multiprocessing.Queue()
        worldGeneratioProcess = multiprocessing.Process(target=World.generateChunkFiles, args=(worldGenerationRequestQueue, worldGenerationResponseQueue))

        worldGeneratioProcess.start()

        return worldGeneratioProcess, worldGenerationRequestQueue, worldGenerationResponseQueue

    @staticmethod
    def updateBuffers(updateBuffersRequestQueue, updateBuffersResponseQueue):
        """
            Update the buffers

            updateBuffersRequestQueue(multiprocessing.Queue) - Request queue
            updateBuffersResponseQueue(multiprocessing.Queue) - Response queue
        """

        while True:
            chunk_vertices, chunk_textures = updateBuffersRequestQueue.get(block=True)

            vertices = np.empty((0, 3), dtype=np.float32)
            textures = np.empty((0, 2), dtype=np.float32)

            for chunk_coord in chunk_vertices:
                vertices = np.vstack((vertices, chunk_vertices[chunk_coord]))
                textures = np.vstack((textures, chunk_textures[chunk_coord]))

            updateBuffersResponseQueue.put((vertices, textures, len(vertices)))


    @staticmethod
    def initializeUpdateBuffersProcess():
        """
            Initialize the update buffers process
        """

        updateBuffersRequestQueue = multiprocessing.Queue()
        updateBuffersResponseQueue = multiprocessing.Queue()
        updateBuffersProcess = multiprocessing.Process(target=World.updateBuffers, args=(updateBuffersRequestQueue, updateBuffersResponseQueue))
        updateBuffersProcess.start()

        return updateBuffersProcess, updateBuffersRequestQueue, updateBuffersResponseQueue

    def parallelGenerateChunkFiles(self, chunk_coord_set):
        """
            Generate the chunks in parallel

            chunk_coord_set(list) - List of chunk coordinates
        """

        for chunk_coord in chunk_coord_set:
            self.worldGenerationRequestQueue.put(chunk_coord)

    def sendVertices(self, program):
        """
            Send the vertices to the GPU

            program(OpenGL.GL.shaders.ShaderProgram) - Shader program
            vertices(numpy.ndarray) - Vertices to be sent to the GPU
        """

        if self.vertice_buffer == None:
            self.vertice_buffer = glGenBuffers(1)

        glBindBuffer(GL_ARRAY_BUFFER, self.vertice_buffer)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        loc = glGetAttribLocation(program, "position")
        glEnableVertexAttribArray(loc)

        stride = self.vertices.strides[0]
        offset = ctypes.c_void_p(0)

        glVertexAttribPointer(loc, 3, GL_FLOAT, False, stride, offset)

    def sendTextures(self, program):
        """
            Send the texture to the GPU

            program(OpenGL.GL.shaders.ShaderProgram) - Shader program
            texture(numpy.ndarray) - Texture to be sent to the GPU
        """

        if self.texture_buffer == None:
            self.texture_buffer = glGenBuffers(1)
        

        glBindBuffer(GL_ARRAY_BUFFER, self.texture_buffer)
        glBufferData(GL_ARRAY_BUFFER, self.textures.nbytes, self.textures, GL_STATIC_DRAW)

        loc = glGetAttribLocation(program, "texture")
        glEnableVertexAttribArray(loc)

        stride = self.textures.strides[0]
        offset = ctypes.c_void_p(0)

        glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride, offset)

    def updateChunks(self, new_central_chunk_coord):
        self.central_chunk_coord = new_central_chunk_coord

        new_chunk_coord_set = World.getNearestChunks(new_central_chunk_coord)
        chunk_coord_set = set(self.chunks.keys())

        chunks_to_remove = chunk_coord_set - new_chunk_coord_set
        chunks_to_add = new_chunk_coord_set - chunk_coord_set

        for chunk in chunks_to_remove:
            del self.chunks[chunk]

        self.parallelGenerateChunkFiles(chunks_to_add)

    def getVertices(self):
        """
            Get the vertices of the world
        """
        vertices = np.empty((0, 3), dtype=np.float32)
        # Iterate through all the chunks in the chunks dictionary
        for chunk in self.chunks:
            # Add the vertices of the chunk to the vertices array
            vertices = np.vstack((vertices, self.chunk_vertices[chunk]))

        return vertices
    
    def getTexture(self):
        """
            Get the texture of the world
        """
        texture = np.empty((0, 2), dtype=np.float32)
        for chunk in self.chunks:
            texture = np.vstack((texture, self.chunk_textures[chunk]))

        return texture
    
    def getLenBlocks(self):
        """
            Get the number of blocks in the world
        """
        len_blocks = 0
        for chunk in self.chunks:
            len_blocks += self.chunks[chunk].getLenBlocks()
        return len_blocks

    def lookForNewlyCreatedChunks(self):
        
        if not self.updateBuffersResponseQueue.empty():
            self.vertices, self.textures, self.lenVertices = self.updateBuffersResponseQueue.get(block=False)

            self.sendVertices(self.program)
            self.sendTextures(self.program)

        elif not self.worldGenerationResponseQueue.empty():
            chunk_coord, chunk, chunk_vertices, chunk_textures = self.worldGenerationResponseQueue.get(block=False)

            if chunk_coord in self.chunks:
                return

            self.chunks[chunk_coord] = chunk
            self.chunk_vertices[chunk_coord] = chunk_vertices
            self.chunk_textures[chunk_coord] = chunk_textures

            self.updateBuffersRequestQueue.put((self.chunk_vertices, self.chunk_textures))


    def draw(self, program, camera):
        """
            Draw the world.

            Draw all the vertices at once to avoid multiple calls to the GPU.
            Optimization over readability.
        """

        self.lookForNewlyCreatedChunks()

        # Draw vertices routines
        loc_model = glGetUniformLocation(program, "model")
        model_array = np.array(glm.mat4(1.0), dtype=np.float32)
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, model_array)

        loc_view = glGetUniformLocation(program, "view")
        view_array = np.array(camera.view, dtype=np.float32)
        glUniformMatrix4fv(loc_view, 1, GL_TRUE, view_array)

        loc_projection = glGetUniformLocation(program, "projection")
        projection_array = np.array(camera.proj, dtype=np.float32)
        glUniformMatrix4fv(loc_projection, 1, GL_TRUE, projection_array)

        # TODO: Check if the function draw works without any chunks
        glDrawArrays(GL_QUADS, 0, self.lenVertices)


