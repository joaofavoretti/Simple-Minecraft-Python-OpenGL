import glfw
import glm
from OpenGL.GL import *
import numpy as np
import threading
import multiprocessing

from Chunk import Chunk
from Moon import Moon
from Sky import Sky

class World:
    def __init__(self, program, window):
        """
            Initialize the world
        """

        self.window = window

        self.program = program

        self.central_chunk_coord = (0, 0)

        self.chunks_to_produce = multiprocessing.Queue()
        self.chunks_to_render = multiprocessing.Queue()

        self.chunks = self.defineChunks(self.central_chunk_coord)

        self.start_worker()
 
    def __del__(self):
        self.chunks_to_produce.put(-1)
        self.p.join()

    def create_chunks(self, to_produce, to_render):
        while True:
            c = to_produce.get()
            if c == -1:
                return
            to_render.put(Chunk(c))

    def start_worker(self):
        self.p = multiprocessing.Process(target = self.create_chunks, args = (self.chunks_to_produce, self.chunks_to_render))
        self.p.start()

    def defineChunks(self, central_chunk_coord):
        """
            Define the chunks of the world
        """
        chunks = []
        central_chunk_x, central_chunk_z = central_chunk_coord
        for x in range(-5, 6):
            for z in range(-5, 6):
                self.chunks_to_produce.put((central_chunk_x + x, central_chunk_z + z))
        
        return chunks
    
    def reDefineChunks(self, central_chunk_coord):
        """
            Re-define the chunks of the world using the near chunks that are already defined
        """
        new_chunks = []
        for chunk in self.chunks:
            if chunk.isNear(central_chunk_coord):
                new_chunks.append(chunk)
        
        central_chunk_x, central_chunk_z = central_chunk_coord
        for x in range(-5, 6):
            for z in range(-5, 6):
                if not self.isChunkDefined(new_chunks, (central_chunk_x + x, central_chunk_z + z)):
                    self.chunks_to_produce.put((central_chunk_x + x, central_chunk_z + z))

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

        self.sky = Sky((16 * new_central_chunk_coord[0], 10, 16 * new_central_chunk_coord[1]))
        self.moon = Moon((16 * new_central_chunk_coord[0] , 90, 16 * new_central_chunk_coord[1]))
    
    def draw(self, program, camera):
        """
            Draw the world.

            Draw all the vertices at once to avoid multiple calls to the GPU.
            Optimization over readability.
        """
        # Version 1
        # for chunk in self.chunks:
        #     chunk.draw(program, camera)

        # Version 2 - Incomplete

        loc_model = glGetUniformLocation(program, "model")
        model_array = np.array(glm.mat4(1.0), dtype=np.float32)
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, model_array)

        loc_view = glGetUniformLocation(program, "view")
        view_array = np.array(camera.view, dtype=np.float32)
        glUniformMatrix4fv(loc_view, 1, GL_TRUE, view_array)

        loc_projection = glGetUniformLocation(program, "projection")
        projection_array = np.array(camera.proj, dtype=np.float32)
        glUniformMatrix4fv(loc_projection, 1, GL_TRUE, projection_array)
        
        while not self.chunks_to_render.empty():
            self.chunks.append(self.chunks_to_render.get())
        
        for chunk in self.chunks:
            chunk.draw(program, camera)
