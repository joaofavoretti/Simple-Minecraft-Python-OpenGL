import glfw
import glm
from OpenGL.GL import *
import numpy as np

class Sky:
    def __init__(self, theta):
        """
            Initialize the sky box centered around the light dir
        """

        self.vertices = self.defineVertices()
        self.texture = self.defineTexture()
        self.normals = self.defineNormals()
        
    def defineVertices(self):
        size = 400

        return np.array([
            (0 - size/2, 0 - size/2, 0 + size/2), # positive z face
            (0 + size/2, 0 - size/2, 0 + size/2),
            (0 + size/2, 0 + size/2, 0 + size/2),
            (0 - size/2, 0 + size/2, 0 + size/2),
            
            (0 + size/2, 0 - size/2, 0 + size/2), # positive x face
            (0 + size/2, 0 - size/2, 0 - size/2),
            (0 + size/2, 0 + size/2, 0 - size/2),
            (0 + size/2, 0 + size/2, 0 + size/2),

            (0 + size/2, 0 - size/2, 0 - size/2), # negative z face
            (0 - size/2, 0 - size/2, 0 - size/2),
            (0 - size/2, 0 + size/2, 0 - size/2),
            (0 + size/2, 0 + size/2, 0 - size/2),

            (0 - size/2, 0 - size/2, 0 - size/2), # negative x face
            (0 - size/2, 0 - size/2, 0 + size/2),
            (0 - size/2, 0 + size/2, 0 + size/2),
            (0 - size/2, 0 + size/2, 0 - size/2),

            (0 - size/2, 0 - size/2, 0 - size/2), # negative y face
            (0 + size/2, 0 - size/2, 0 - size/2),
            (0 + size/2, 0 - size/2, 0 + size/2),
            (0 - size/2, 0 - size/2, 0 + size/2),

            (0 - size/2, 0 + size/2, 0 + size/2), # positive y face
            (0 + size/2, 0 + size/2, 0 + size/2),
            (0 + size/2, 0 + size/2, 0 - size/2),
            (0 - size/2, 0 + size/2, 0 - size/2),
 

        ], dtype=np.float32)

    def defineTexture(self):
        """
            Define the texutre of the sky, using Sky texture
        """

        return np.array([
            (0, 0),
            (1, 0),
            (1, 1),
            (0, 1),
            (0, 0),
            (1, 0),
            (1, 1),
            (0, 1),
            (0, 0),
            (1, 0),
            (1, 1),
            (0, 1),
            (0, 0),
            (1, 0),
            (1, 1),
            (0, 1),
            (0, 0),
            (1, 0),
            (1, 1),
            (0, 1),
            (0, 0),
            (1, 0),
            (1, 1),
            (0, 1)
        ], dtype=np.float32)

    def defineNormals(self):
        """
            Define the normals as zero to eliminate illumination
        """

        return np.array([
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0)
        ], dtype=np.float32)

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

    def draw(self, program, camera, theta):
        """
            Draw the Sky
        """

        modelTemp = glm.rotate(glm.mat4(1.0), theta, glm.vec3(0,1,0))
        model = glm.rotate(modelTemp, glm.radians(45.0), (1, 0, 0))

        loc_model = glGetUniformLocation(program, "model")
        model_array = np.array(model, dtype=np.float32)
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, model_array)

        loc_view = glGetUniformLocation(program, "view")
        view_array = np.array(glm.mat4(glm.mat3(camera.view)), dtype=np.float32)
        glUniformMatrix4fv(loc_view, 1, GL_TRUE, view_array)
     
        self.setVerticesAndTexture(program)
        glDrawArrays(GL_QUADS, 0, 24)
