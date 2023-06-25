import glfw
import glm
from OpenGL.GL import *
import numpy as np
import threading
import multiprocessing
from PIL import Image

from Chunk import Chunk
from Moon import Moon
from Sky import Sky
from Cloud import Cloud

TEXTURE_ATLAS = './assets/texture_atlas.png'
TEXTURE_SKY = './assets/Starred_Sky.png'

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
        self.clouds_to_produce = multiprocessing.Queue()
        self.clouds_to_render = multiprocessing.Queue()

        self.chunks, self.clouds = self.defineChunks(self.central_chunk_coord)

        self.start_worker()

        self.light_theta = 0
        self.sky = Sky(self.light_theta)

        self.moon = Moon((0, 200, 0))
 
    def loadTexture(self, texture_file):
        """
            Load the texture file. Texture is 16x16. Pixelation is intentional
    
            texture_file(str) - Texture file path
        """
        glEnable(GL_TEXTURE_2D)

        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, 0)
    
        # Set the texture wrapping parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)	
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    
        # Set texture filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)	
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    
        # Load image
        image = Image.open(texture_file)
        img_data = image.tobytes("raw", "RGB", 0, -1)
    
        # Generate texture
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.size[0], image.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

    def __del__(self):
        self.chunks_to_produce.put(-1)
        self.p.join()

    def create_chunks(self, to_produce, to_render, clouds_to_produce, clouds_to_render):
        while True:
            c = to_produce.get()
            #cl = clouds_to_produce.get()
            if c == -1:
                return
            if(c != -1):
                to_render.put(Chunk(c))
            """ if(cl != -1):
                clouds_to_render.put(Cloud(cl)) """

    def start_worker(self):
        self.p = multiprocessing.Process(target = self.create_chunks, args = (self.chunks_to_produce, self.chunks_to_render, self.clouds_to_produce, self.clouds_to_render))
        self.p.start()

    def defineChunks(self, central_chunk_coord):
        """
            Define the chunks of the world
        """
        chunks = []
        clouds = []
        central_chunk_x, central_chunk_z = central_chunk_coord
        for x in range(-5, 6):
            for z in range(-5, 6):
                self.chunks_to_produce.put((central_chunk_x + x, central_chunk_z + z))
                #self.clouds_to_produce.put((central_chunk_x + x, 90,central_chunk_z + z))
        
        return chunks, clouds
    
    def reDefineChunks(self, central_chunk_coord):
        """
            Re-define the chunks of the world using the near chunks that are already defined
        """
        new_chunks = []
        new_clouds = []
        for chunk, cloud in zip(self.chunks, self.clouds):
            if chunk.isNear(central_chunk_coord):
                new_chunks.append(chunk)
                #new_clouds.append(cloud)
        
        central_chunk_x, central_chunk_z = central_chunk_coord
        for x in range(-5, 6):
            for z in range(-5, 6):
                if not self.isChunkDefined(new_chunks, (central_chunk_x + x, central_chunk_z + z)):
                    self.chunks_to_produce.put((central_chunk_x + x, central_chunk_z + z))
                    #self.clouds_to_produce.put((central_chunk_x + x, 90,central_chunk_z + z))


        return new_chunks, new_clouds

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

        self.chunks, self.clouds = self.reDefineChunks(self.central_chunk_coord)

        self.sky = Sky((16 * new_central_chunk_coord[0], 10, 16 * new_central_chunk_coord[1]))
        self.moon = Moon((16 * new_central_chunk_coord[0] , 200, 16 * new_central_chunk_coord[1]))
    
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

        self.light_theta += 0.01
        lightdir = (np.sin(self.light_theta), 1.0, np.cos(self.light_theta))
        loc_light_dir = glGetUniformLocation(program, "lightDir")
        glUniform3f(loc_light_dir, lightdir[0], lightdir[1], lightdir[2])

        loc_model = glGetUniformLocation(program, "model")
        model_array = np.array(glm.mat4(1.0), dtype=np.float32)
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, model_array)

        loc_view = glGetUniformLocation(program, "view")
        view_array = np.array(camera.view, dtype=np.float32)
        glUniformMatrix4fv(loc_view, 1, GL_TRUE, view_array)

        loc_projection = glGetUniformLocation(program, "projection")
        projection_array = np.array(camera.proj, dtype=np.float32)
        glUniformMatrix4fv(loc_projection, 1, GL_TRUE, projection_array)
        
        self.loadTexture(TEXTURE_SKY)
        self.sky.draw(program, camera, self.light_theta)
    
        self.loadTexture(TEXTURE_ATLAS)
        while not self.chunks_to_render.empty():
            self.chunks.append(self.chunks_to_render.get())
        
        """ while not self.clouds_to_render.empty():
            self.clouds.append(self.chunks_to_render.get()) """
        
        for chunk in self.chunks:
            chunk.draw(program, camera)
        """ for cloud in self.clouds:
            cloud.draw(program, camera) """

        self.moon.draw(program, camera.view, camera.proj, self.light_theta)
